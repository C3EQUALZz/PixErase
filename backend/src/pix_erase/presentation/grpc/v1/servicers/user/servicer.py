from uuid import UUID

import grpc.aio
from dishka import FromDishka
from dishka.integrations.grpcio import inject
from google.protobuf.empty_pb2 import Empty

from pix_erase.application.commands.user.activate_user import ActivateUserCommand, ActivateUserCommandHandler
from pix_erase.application.commands.user.change_user_email import ChangeUserEmailCommand, ChangeUserEmailCommandHandler
from pix_erase.application.commands.user.change_user_name import (
    ChangeUserNameByIDCommand,
    ChangeUserNameByIDCommandHandler,
)
from pix_erase.application.commands.user.change_user_password import (
    ChangeUserPasswordCommand,
    ChangeUserPasswordCommandHandler,
)
from pix_erase.application.commands.user.create_user import CreateUserCommand, CreateUserCommandHandler
from pix_erase.application.commands.user.delete_user_by_id import DeleteUserByIDCommand, DeleteUserByIDCommandHandler
from pix_erase.application.commands.user.grant_admin_by_id import (
    GrantAdminToUserByIDCommand,
    GrantAdminToUserByIDCommandHandler,
)
from pix_erase.application.commands.user.revoke_admin_by_id import (
    RevokeAdminByIDCommand,
    RevokeAdminByIDCommandHandler,
)
from pix_erase.application.queries.users.read_all import ReadAllUsersQuery, ReadAllUsersQueryHandler
from pix_erase.application.queries.users.read_by_id import ReadUserByIDQuery, ReadUserByIDQueryHandler
from pix_erase.domain.user.values.user_role import UserRole
from pix_erase.presentation.grpc.v1.generated.v1 import user_pb2, user_pb2_grpc


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    @inject
    async def ReadUserByID(  # noqa: N802
        self,
        request: user_pb2.ReadUserByIDRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ReadUserByIDQueryHandler],
    ) -> user_pb2.ReadUserByIDResponse:
        query = ReadUserByIDQuery(user_id=UUID(request.user_id))
        view = await handler(query)
        return user_pb2.ReadUserByIDResponse(
            id=str(view.id),
            email=view.email,
            name=view.name,
            role=view.role,
        )

    @inject
    async def ReadAllUsers(  # noqa: N802
        self,
        request: user_pb2.ReadAllUsersRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ReadAllUsersQueryHandler],
    ) -> user_pb2.ReadAllUsersResponse:
        query = ReadAllUsersQuery(
            limit=request.limit or 20,
            offset=request.offset,
            sorting_field=request.sorting_field or "email",
            sorting_order=request.sorting_order or "DESC",
        )
        views = await handler(query)
        users = [
            user_pb2.ReadUserByIDResponse(
                id=str(v.id),
                email=v.email,
                name=v.name,
                role=v.role,
            )
            for v in views
        ]
        return user_pb2.ReadAllUsersResponse(users=users)

    @inject
    async def CreateUser(  # noqa: N802
        self,
        request: user_pb2.CreateUserRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[CreateUserCommandHandler],
    ) -> user_pb2.CreateUserResponse:
        command = CreateUserCommand(
            email=request.email,
            name=request.name,
            password=request.password,
            role=UserRole(request.role) if request.role else UserRole.USER,
        )
        view = await handler(command)
        return user_pb2.CreateUserResponse(user_id=str(view.user_id))

    @inject
    async def ActivateUser(  # noqa: N802
        self,
        request: user_pb2.ActivateUserRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ActivateUserCommandHandler],
    ) -> Empty:
        command = ActivateUserCommand(user_id=UUID(request.user_id))
        await handler(command)
        return Empty()

    @inject
    async def ChangeUserEmail(  # noqa: N802
        self,
        request: user_pb2.ChangeUserEmailRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ChangeUserEmailCommandHandler],
    ) -> Empty:
        command = ChangeUserEmailCommand(user_id=UUID(request.user_id), new_email=request.new_email)
        await handler(command)
        return Empty()

    @inject
    async def ChangeUserName(  # noqa: N802
        self,
        request: user_pb2.ChangeUserNameRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ChangeUserNameByIDCommandHandler],
    ) -> Empty:
        command = ChangeUserNameByIDCommand(user_id=UUID(request.user_id), new_name=request.new_name)
        await handler(command)
        return Empty()

    @inject
    async def ChangeUserPassword(  # noqa: N802
        self,
        request: user_pb2.ChangeUserPasswordRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ChangeUserPasswordCommandHandler],
    ) -> Empty:
        command = ChangeUserPasswordCommand(user_id=UUID(request.user_id), password=request.password)
        await handler(command)
        return Empty()

    @inject
    async def DeleteUser(  # noqa: N802
        self,
        request: user_pb2.DeleteUserRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[DeleteUserByIDCommandHandler],
    ) -> Empty:
        command = DeleteUserByIDCommand(user_id=UUID(request.user_id))
        await handler(command)
        return Empty()

    @inject
    async def GrantAdmin(  # noqa: N802
        self,
        request: user_pb2.GrantAdminRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[GrantAdminToUserByIDCommandHandler],
    ) -> Empty:
        command = GrantAdminToUserByIDCommand(user_id=UUID(request.user_id))
        await handler(command)
        return Empty()

    @inject
    async def RevokeAdmin(  # noqa: N802
        self,
        request: user_pb2.RevokeAdminRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[RevokeAdminByIDCommandHandler],
    ) -> Empty:
        command = RevokeAdminByIDCommand(user_id=UUID(request.user_id))
        await handler(command)
        return Empty()
