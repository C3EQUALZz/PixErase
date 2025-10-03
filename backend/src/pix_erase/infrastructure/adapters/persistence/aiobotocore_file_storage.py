import logging
from typing import Final, Any

from aiobotocore.client import AioBaseClient
from botocore.exceptions import EndpointConnectionError, ClientError
from typing_extensions import override

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.domain.image.values.image_name import ImageName
from pix_erase.domain.image.values.image_size import ImageSize
from pix_erase.infrastructure.adapters.persistence.constants import (
    UPLOAD_FILE_FAILED,
    DOWNLOAD_FILE_FAILED,
    DELETE_FILE_FAILED
)
from pix_erase.infrastructure.errors.file_storage import FileStorageError
from pix_erase.setup.config.s3 import S3Config

logger: Final[logging.Logger] = logging.getLogger(__name__)


class AiobotocoreS3ImageStorage(ImageStorage):
    def __init__(self, client: AioBaseClient, s3_config: S3Config) -> None:
        self._client: Final[AioBaseClient] = client
        self._bucket_name: Final[str] = s3_config.images_bucket_name

    @override
    async def add(self, image: Image) -> None:
        try:
            s3_key: str = f"images/{image.id!s}"
            logger.debug("Build s3 key for storage: %s", s3_key)

            await self._client.upload_fileobj(
                image.data,
                self._bucket_name,
                s3_key,
                ExtraArgs={
                    "Metadata": {
                        "original_filename": image.name.value,
                        "height": image.height.value,
                        "width": image.width.value,
                        "created_at": image.created_at,
                        "updated_at": image.updated_at,
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

    @override
    async def read_by_id(self, image_id: ImageID) -> Image | None:
        s3_key: str = f"images/{image_id!s}"

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
                created_at=metadata.get("created_at"),
                updated_at=metadata.get("updated_at"),
                width=ImageSize(metadata.get("width")),
                height=ImageSize(metadata.get("height")),
            )

    @override
    async def delete_by_id(self, image_id: ImageID) -> None:
        s3_key: str = f"images/{image_id}"

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
