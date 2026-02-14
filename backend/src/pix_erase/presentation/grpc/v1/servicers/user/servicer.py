from uuid import UUID

import grpc.aio
from dishka import FromDishka
from dishka.integrations.grpcio import inject

from pix_erase.application.queries.users.read_by_id import ReadUserByIDQuery, ReadUserByIDQueryHandler
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
