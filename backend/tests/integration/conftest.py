import pytest
from testcontainers.minio import MinioContainer

from pix_erase.setup.config.s3 import S3Config


@pytest.fixture(scope="session")
def minio_container():
    minio_config = S3Config()

    with MinioContainer(
            "quay.io/minio/minio:RELEASE.2025-03-12T18-04-18Z",
            access_key=minio_config.aws_access_key_id,
            secret_key=minio_config.aws_secret_access_key,
            port=minio_config.port
    ) as minio:
        client = minio.get_client()
        client.make_bucket(BUCKET)
        yield minio
