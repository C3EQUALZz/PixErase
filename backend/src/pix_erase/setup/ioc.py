from typing import Final, Iterable

from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, WithParents
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from pix_erase.application.auth.log_in import LogInHandler
from pix_erase.application.auth.log_out import LogOutHandler
from pix_erase.application.auth.read_current_user import ReadCurrentUserHandler
from pix_erase.application.auth.sign_up import SignUpHandler
from pix_erase.application.commands.image.compress_image import CompressImageCommandHandler
from pix_erase.application.commands.image.create_image import CreateImageCommandHandler
from pix_erase.application.commands.image.grayscale_image import GrayscaleImageCommandHandler
from pix_erase.application.commands.image.remove_watermark_from_image import RemoveWatermarkFromImageCommandHandler
from pix_erase.application.commands.image.rotate_image import RotateImageCommandHandler
from pix_erase.application.commands.user.activate_user import ActivateUserCommandHandler
from pix_erase.application.commands.user.change_user_email import ChangeUserEmailCommandHandler
from pix_erase.application.commands.user.change_user_name import ChangeUserNameByIDCommandHandler
from pix_erase.application.commands.user.change_user_password import ChangeUserPasswordCommandHandler
from pix_erase.application.commands.user.create_user import CreateUserCommandHandler
from pix_erase.application.commands.user.delete_user_by_id import DeleteUserByIDCommandHandler
from pix_erase.application.commands.user.grant_admin_by_id import GrantAdminToUserByIDCommandHandler
from pix_erase.application.commands.user.revoke_admin_by_id import RevokeAdminByIDCommandHandler
from pix_erase.application.common.ports.access_revoker import AccessRevoker
from pix_erase.application.common.ports.event_bus import EventBus
from pix_erase.application.common.ports.identity_provider import IdentityProvider
from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.services.auth_session import AuthSessionService
from pix_erase.application.common.services.colorization_service import ColorizationService
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.application.common.services.image_transformation_service import ImageTransformationService
from pix_erase.application.queries.users.read_all import ReadAllUsersQueryHandler
from pix_erase.application.queries.users.read_by_id import ReadUserByIDQueryHandler
from pix_erase.domain.image.ports.id_generator import ImageIdGenerator
from pix_erase.domain.image.ports.image_color_to_gray_converter import ImageColorToCrayScaleConverter
from pix_erase.domain.image.ports.image_compress_converter import ImageCompressConverter
from pix_erase.domain.image.ports.image_crop_converter import ImageCropConverter
from pix_erase.domain.image.ports.image_rotation_converter import ImageRotationConverter
from pix_erase.domain.image.services.image_service import ImageService
from pix_erase.domain.user.ports.id_generator import UserIdGenerator
from pix_erase.domain.user.ports.password_hasher import PasswordHasher
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.infrastructure.adapters.auth.access_revoker import AuthSessionAccessRevoker
from pix_erase.infrastructure.adapters.auth.identity_provider import AuthSessionIdentityProvider
from pix_erase.infrastructure.adapters.auth.jwt_auth_session_transport import JwtCookieAuthSessionTransport
from pix_erase.infrastructure.adapters.auth.jwt_token_processor import JwtSecret, JwtAlgorithm, JwtAccessTokenProcessor
from pix_erase.infrastructure.adapters.auth.secrets_auth_session_generator import SecretsAuthSessionIdGenerator
from pix_erase.infrastructure.adapters.common.bazario_event_bus import BazarioEventBus
from pix_erase.infrastructure.adapters.common.password_hasher_bcrypt import PasswordPepper, BcryptPasswordHasher
from pix_erase.infrastructure.adapters.common.uuid4_image_id_generator import UUID4ImageIdGenerator
from pix_erase.infrastructure.adapters.common.uuid4_user_id_generator import UUID4UserIdGenerator
from pix_erase.infrastructure.adapters.image_converters.cv2_image_color_to_gray_converter import \
    Cv2ImageColorToCrayScaleConverter
from pix_erase.infrastructure.adapters.image_converters.cv2_image_compress_converter import Cv2ImageCompressConverter
from pix_erase.infrastructure.adapters.image_converters.cv2_image_crop_converter import Cv2ImageCropConverter
from pix_erase.infrastructure.adapters.image_converters.сv2_image_rotation_converter import Cv2ImageRotationConverter
from pix_erase.infrastructure.adapters.persistence.aiobotocore_file_storage import AiobotocoreS3ImageStorage
from pix_erase.infrastructure.adapters.persistence.alchemy_auth_session_command_gateway import (
    SQLAlchemyAuthSessionCommandGateway
)
from pix_erase.infrastructure.adapters.persistence.alchemy_auth_transaction_manager import (
    SqlaAuthSessionTransactionManager
)
from pix_erase.infrastructure.adapters.persistence.alchemy_main_transaction_manager import SqlAlchemyTransactionManager
from pix_erase.infrastructure.adapters.persistence.alchemy_user_command_gateway import SqlAlchemyUserCommandGateway
from pix_erase.infrastructure.adapters.persistence.alchemy_user_query_gateway import SqlAlchemyUserQueryGateway
from pix_erase.infrastructure.auth.cookie_params import CookieParams
from pix_erase.infrastructure.auth.session.id_generator import AuthSessionIDGenerator
from pix_erase.infrastructure.auth.session.ports.gateway import AuthSessionGateway
from pix_erase.infrastructure.auth.session.ports.transaction_manager import AuthSessionTransactionManager
from pix_erase.infrastructure.auth.session.ports.transport import AuthSessionTransport
from pix_erase.infrastructure.auth.session.timer_utc import (
    AuthSessionRefreshThreshold,
    AuthSessionTtlMin,
    UtcAuthSessionTimer
)
from pix_erase.infrastructure.cache.provider import get_redis_pool, get_redis
from pix_erase.infrastructure.persistence.provider import (
    get_engine,
    get_sessionmaker,
    get_session,
    get_s3_session,
    get_s3_client
)
from pix_erase.setup.config.asgi import ASGIConfig
from pix_erase.setup.config.database import PostgresConfig


def configs_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.from_context(provides=ASGIConfig)
    provider.from_context(provides=PostgresConfig)
    provider.from_context(provides=JwtSecret)
    provider.from_context(provides=PasswordPepper)
    provider.from_context(provides=JwtAlgorithm)
    provider.from_context(provides=AuthSessionTtlMin)
    provider.from_context(provides=AuthSessionRefreshThreshold)
    provider.from_context(provides=CookieParams)
    return provider


def db_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AsyncSession)
    return provider


def s3_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(get_s3_session)
    provider.provide(get_s3_client)
    return provider


def cache_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(get_redis_pool, scope=Scope.APP)
    provider.provide(get_redis, provides=Redis)
    return provider


def auth_ports_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.from_context(provides=Request, scope=Scope.REQUEST)
    provider.provide_all(
        CurrentUserService,
        JwtAccessTokenProcessor,
        UtcAuthSessionTimer
    )
    provider.provide(source=SecretsAuthSessionIdGenerator, provides=AuthSessionIDGenerator)
    provider.provide(source=AuthSessionAccessRevoker, provides=AccessRevoker)
    provider.provide(source=AuthSessionIdentityProvider, provides=IdentityProvider)
    provider.provide(source=AuthSessionService)
    provider.provide(source=JwtCookieAuthSessionTransport, provides=AuthSessionTransport)
    return provider


def domain_ports_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=BcryptPasswordHasher, provides=PasswordHasher)
    provider.provide(source=UUID4UserIdGenerator, provides=UserIdGenerator)
    provider.provide(source=UUID4ImageIdGenerator, provides=ImageIdGenerator)
    provider.provide(source=Cv2ImageColorToCrayScaleConverter, provides=ImageColorToCrayScaleConverter)
    provider.provide(source=Cv2ImageCompressConverter, provides=ImageCompressConverter)
    provider.provide(source=Cv2ImageCropConverter, provides=ImageCropConverter)
    provider.provide(source=Cv2ImageRotationConverter, provides=ImageRotationConverter)
    provider.provide(source=UserService)
    provider.provide(source=AccessService)
    provider.provide(source=ImageService)
    return provider


def gateways_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(source=SQLAlchemyAuthSessionCommandGateway, provides=AuthSessionGateway)
    provider.provide(source=SqlaAuthSessionTransactionManager, provides=AuthSessionTransactionManager)
    provider.provide(source=SqlAlchemyTransactionManager, provides=TransactionManager)
    provider.provide(source=SqlAlchemyUserCommandGateway, provides=UserCommandGateway)
    provider.provide(source=SqlAlchemyUserQueryGateway, provides=UserQueryGateway)
    provider.provide(source=AiobotocoreS3ImageStorage, provides=ImageStorage)
    return provider


def registry_provider() -> Registry:
    registry: Final[Registry] = Registry()
    return registry


def event_bus_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)
    provider.provide(registry_provider)
    provider.provide(BazarioEventBus, provides=EventBus)
    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaResolver])
    return provider


def interactors_provider() -> Provider:
    provider: Final[Provider] = Provider(scope=Scope.REQUEST)

    provider.provide_all(
        LogInHandler,
        LogOutHandler,
        ReadCurrentUserHandler,
        SignUpHandler,
        ActivateUserCommandHandler,
        ChangeUserEmailCommandHandler,
        ChangeUserNameByIDCommandHandler,
        ChangeUserPasswordCommandHandler,
        CreateUserCommandHandler,
        DeleteUserByIDCommandHandler,
        GrantAdminToUserByIDCommandHandler,
        RevokeAdminByIDCommandHandler,
        GrayscaleImageCommandHandler,
        ReadAllUsersQueryHandler,
        ReadUserByIDQueryHandler,
        CompressImageCommandHandler,
        CreateImageCommandHandler,
        RemoveWatermarkFromImageCommandHandler,
        RotateImageCommandHandler
    )

    # application services
    provider.provide_all(
        ImageTransformationService,
        ColorizationService
    )

    return provider


def setup_providers() -> Iterable[Provider]:
    return (
        configs_provider(),
        db_provider(),
        cache_provider(),
        auth_ports_provider(),
        domain_ports_provider(),
        gateways_provider(),
        interactors_provider(),
        event_bus_provider(),
        s3_provider()
    )
