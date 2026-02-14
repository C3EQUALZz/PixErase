import grpc.aio
from dishka import FromDishka
from dishka.integrations.grpcio import inject
from google.protobuf.empty_pb2 import Empty

from pix_erase.application.auth.log_in import LogInData, LogInHandler
from pix_erase.application.auth.log_out import LogOutHandler
from pix_erase.application.auth.read_current_user import ReadCurrentUserHandler
from pix_erase.application.auth.sign_up import SignUpData, SignUpHandler
from pix_erase.infrastructure.adapters.auth.jwt_grpc_metadata_auth_session_transport import (
    JwtGrpcMetadataAuthSessionTransport,
)
from pix_erase.presentation.grpc.v1.generated.v1 import auth_pb2, auth_pb2_grpc


class AuthServiceServicer(auth_pb2_grpc.AuthServiceServicer):
    @inject
    async def SignUp(  # noqa: N802
        self,
        request: auth_pb2.SignUpRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[SignUpHandler],
    ) -> auth_pb2.SignUpResponse:
        data = SignUpData(email=request.email, name=request.name, password=request.password)
        view = await handler(data)
        return auth_pb2.SignUpResponse(user_id=str(view.user_id))

    @inject
    async def Login(  # noqa: N802
        self,
        request: auth_pb2.LoginRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[LogInHandler],
        transport: FromDishka[JwtGrpcMetadataAuthSessionTransport],
    ) -> auth_pb2.LoginResponse:
        data = LogInData(email=request.email, password=request.password)
        await handler(data)
        access_token = transport.last_access_token or ""
        return auth_pb2.LoginResponse(access_token=access_token)

    @inject
    async def Logout(  # noqa: N802
        self,
        request: Empty,  # noqa: ARG002
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[LogOutHandler],
    ) -> Empty:
        await handler()
        return Empty()

    @inject
    async def ReadMe(  # noqa: N802
        self,
        request: Empty,  # noqa: ARG002
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ReadCurrentUserHandler],
    ) -> auth_pb2.ReadUserResponse:
        view = await handler()
        return auth_pb2.ReadUserResponse(
            id=str(view.id),
            email=view.email,
            name=view.name,
            role=view.role,
        )
