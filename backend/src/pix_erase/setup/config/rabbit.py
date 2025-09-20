from pydantic import AmqpDsn, BaseModel, Field


class RabbitConfig(BaseModel):
    """Configuration container for RabbitMQ connection settings.

        Attributes:
            user: rabbitmq username.
            password: rabbitmq password.
            host: rabbitmq hostname or IP address.
            port: rabbitmq server port.

        Properties:
            uri: Complete RabbitMQ connection URI.
    """
    host: str = Field(
        alias="RABBITMQ_HOST",
        description="RabbitMQ host name or IP address.",
    )
    port: int = Field(
        alias="RABBITMQ_PORT",
        description="RabbitMQ server port.",
    )
    user: str = Field(
        alias="RABBITMQ_DEFAULT_USER",
        description="Default RabbitMQ username.",
    )
    password: str = Field(
        alias="RABBITMQ_DEFAULT_PASS",
        description="Default RabbitMQ password.",
    )

    @property
    def uri(self) -> str:
        """Generates a RabbitMQ connection URI.

        Returns:
            str: Connection string in format

        Note:
            - Includes all authentication credentials
        """
        return str(
            AmqpDsn.build(
                scheme="amqp",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            ),
        )