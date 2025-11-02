from pydantic import BaseModel, Field, field_validator

from pix_erase.setup.config.consts import PORT_MAX, PORT_MIN


class S3Config(BaseModel):
    host: str = Field(..., alias="MINIO_HOST")
    port: int = Field(..., alias="MINIO_PORT")
    aws_access_key_id: str = Field(..., alias="MINIO_ROOT_USER")
    aws_secret_access_key: str = Field(..., alias="MINIO_ROOT_PASSWORD")
    signature_version: str = "s3v4"
    region_name: str = "us-east-1"

    images_bucket_name: str = Field(..., alias="MINIO_IMAGES_BUCKET")

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(
                f"MINIO_PORT must be between {PORT_MIN} and {PORT_MAX}, got {v}."
            )
        return v

    @property
    def uri(self) -> str:
        return f"http://{self.host}:{self.port}"
