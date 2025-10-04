from pydantic import BaseModel, Field


class S3Config(BaseModel):
    host: str = Field(..., alias="MINIO_HOST")
    port: int = Field(..., alias="MINIO_PORT")
    aws_access_key_id: str = Field(..., alias="MINIO_ROOT_USER")
    aws_secret_access_key: str = Field(..., alias="MINIO_ROOT_PASSWORD")
    signature_version: str = "s3v4"
    region_name: str = "us-east-1"

    images_bucket_name: str = Field(..., alias="MINIO_IMAGES_BUCKET")

    @property
    def uri(self) -> str:
        return f"http://{self.host}/{self.port}"
