import io
import logging
from datetime import datetime
from typing import Final, Any, AsyncGenerator

from aiobotocore.client import AioBaseClient
from botocore.exceptions import EndpointConnectionError, ClientError
from tenacity import retry, stop_after_attempt, wait_exponential
from typing_extensions import override

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.query_models.image import ImageStreamQueryModel
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize
from pix_erase.infrastructure.adapters.persistence.constants import (
    UPLOAD_FILE_FAILED,
    DOWNLOAD_FILE_FAILED,
    DELETE_FILE_FAILED, STREAM_FILE_FAILED
)
from pix_erase.infrastructure.errors.file_storage import FileStorageError
from pix_erase.setup.config.s3 import S3Config

logger: Final[logging.Logger] = logging.getLogger(__name__)


class AiobotocoreS3ImageStorage(ImageStorage):
    def __init__(self, client: AioBaseClient, s3_config: S3Config) -> None:
        self._client: Final[AioBaseClient] = client
        self._bucket_name: Final[str] = s3_config.images_bucket_name

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
    async def add(self, image: Image) -> None:
        try:
            s3_key: str = f"images/{image.id!s}"
            logger.debug("Build s3 key for storage: %s", s3_key)

            await self._client.upload_fileobj(
                io.BytesIO(image.data),
                self._bucket_name,
                s3_key,
                ExtraArgs={
                    "Metadata": {
                        "original_filename": image.name.value,
                        "height": str(image.height.value),
                        "width": str(image.width.value),
                        "created_at": image.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "updated_at": image.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    },
                    "ContentType": "application/octet-stream",
                }
            )

        except EndpointConnectionError as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

        except ClientError as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

        except Exception as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
    async def read_by_id(self, image_id: ImageID) -> Image | None:
        s3_key: str = f"images/{image_id!s}"
        logger.debug("Build s3 key for storage: %s", s3_key)

        try:
            response = await self._client.get_object(Bucket=self._bucket_name, Key=s3_key)
            metadata: dict[str, Any] = response.get("Metadata", {})
            original_filename: str = metadata.get("original_filename", s3_key.split("/")[-1])

            file_data = await response["Body"].read()

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.warning("File not found in S3: %s", s3_key)
                return None
            logger.exception(DOWNLOAD_FILE_FAILED)
            raise FileStorageError(DOWNLOAD_FILE_FAILED) from e
        except EndpointConnectionError as e:
            logger.exception(DOWNLOAD_FILE_FAILED)
            raise FileStorageError(DOWNLOAD_FILE_FAILED) from e
        except Exception as e:
            logger.exception(DOWNLOAD_FILE_FAILED)
            raise FileStorageError(DOWNLOAD_FILE_FAILED) from e
        else:
            return Image(
                id=image_id,
                name=ImageName(original_filename),
                data=file_data,
                created_at=datetime.strptime(metadata.get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ"),
                updated_at=datetime.strptime(metadata.get("updated_at"), "%Y-%m-%dT%H:%M:%S.%fZ"),
                width=ImageSize(int(metadata.get("width"))),
                height=ImageSize(int(metadata.get("height"))),
            )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
    async def delete_by_id(self, image_id: ImageID) -> None:
        s3_key: str = f"images/{image_id}"
        logger.debug("Build s3 key for storage: %s", s3_key)

        try:
            await self._client.delete_object(Bucket=self._bucket_name, Key=s3_key)
            logger.info("File successfully deleted from S3: %s", s3_key)

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.warning("File not found in S3: %s", s3_key)
                return
            logger.exception(DELETE_FILE_FAILED)
            raise FileStorageError(DELETE_FILE_FAILED) from e
        except EndpointConnectionError as e:
            logger.exception(DELETE_FILE_FAILED)
            raise FileStorageError(DELETE_FILE_FAILED) from e
        except Exception as e:
            logger.exception(DELETE_FILE_FAILED)
            raise FileStorageError(DELETE_FILE_FAILED) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
    async def update(self, image: Image) -> None:
        s3_key: str = f"images/{image.id}"
        logger.debug("Build s3 key for storage: %s", s3_key)

        try:
            await self._client.upload_fileobj(
                io.BytesIO(image.data),
                self._bucket_name,
                s3_key,
                ExtraArgs={
                    "Metadata": {
                        "original_filename": image.name.value,
                        "height": str(image.height.value),
                        "width": str(image.width.value),
                        "created_at": image.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        "updated_at": image.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    },
                    "ContentType": "application/octet-stream",
                }
            )

        except EndpointConnectionError as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.warning("File not found in S3: %s", s3_key)
                return
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

        except Exception as e:
            logger.exception(UPLOAD_FILE_FAILED)
            raise FileStorageError(UPLOAD_FILE_FAILED) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    @override
    async def stream_by_id(self, image_id: ImageID) -> ImageStreamQueryModel | None:
        """
        Получает изображение из S3 в виде стрима
        Возвращает DTO с генератором байтов и метаданными
        """
        s3_key: str = f"images/{image_id!s}"
        logger.debug("Build s3 key for storage: %s", s3_key)

        try:
            # Получаем объект из S3
            response = await self._client.get_object(
                Bucket=self._bucket_name,
                Key=s3_key
            )

            # Извлекаем метаданные
            metadata: dict[str, Any] = response.get("Metadata", {})
            original_filename: ImageName = ImageName(metadata.get("original_filename", str(image_id)))
            content_length = response['ContentLength']
            content_type = response.get('ContentType', 'application/octet-stream')
            etag = response.get('ETag')
            width = ImageSize(int(metadata.get("width")))
            height = ImageSize(int(metadata.get("height")))
            created_at = datetime.strptime(metadata.get("created_at"), "%Y-%m-%dT%H:%M:%S.%fZ")
            updated_at = datetime.strptime(metadata.get("updated_at"), "%Y-%m-%dT%H:%M:%S.%fZ")

            # Создаем асинхронный генератор для стриминга
            async def chunk_generator() -> AsyncGenerator[bytes, None]:
                """Генератор, отдающий файл по частям"""
                stream = response["Body"]
                try:
                    # Читаем файл chunks по 64KB (оптимально для сетевой передачи)
                    chunk_size = 64 * 1024
                    while True:
                        chunk = await stream.read(chunk_size)
                        if not chunk:
                            break
                        yield chunk
                except Exception as e:
                    logger.error("Error during streaming chunk: %s", e)
                    raise

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logger.warning("File not found in S3 for streaming: %s", s3_key)
                return None
            logger.exception(STREAM_FILE_FAILED)
            raise FileStorageError(STREAM_FILE_FAILED) from e
        except EndpointConnectionError as e:
            logger.exception(STREAM_FILE_FAILED)
            raise FileStorageError(STREAM_FILE_FAILED) from e
        except Exception as e:
            logger.exception(STREAM_FILE_FAILED)
            raise FileStorageError(STREAM_FILE_FAILED) from e

        else:
            return ImageStreamQueryModel(
                stream=chunk_generator(),
                content_type=content_type,
                content_length=content_length,
                filename=original_filename,
                etag=etag,
                created_at=created_at,
                updated_at=updated_at,
                width=width,
                height=height,
            )
