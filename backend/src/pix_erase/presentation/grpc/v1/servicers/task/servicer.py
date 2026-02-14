import grpc.aio
from dishka import FromDishka
from dishka.integrations.grpcio import inject

from pix_erase.application.queries.tasks.read_task_by_id import ReadTaskByIDQuery, ReadTaskByIDQueryHandler
from pix_erase.presentation.grpc.v1.generated.v1 import task_pb2, task_pb2_grpc


class TaskServiceServicer(task_pb2_grpc.TaskServiceServicer):
    @inject
    async def ReadTaskByID(  # noqa: N802
        self,
        request: task_pb2.ReadTaskByIDRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ReadTaskByIDQueryHandler],
    ) -> task_pb2.ReadTaskByIDResponse:
        query = ReadTaskByIDQuery(task_id=request.task_id)
        view = await handler(query)
        return task_pb2.ReadTaskByIDResponse(
            status=view.status,
            description=view.description,
        )
