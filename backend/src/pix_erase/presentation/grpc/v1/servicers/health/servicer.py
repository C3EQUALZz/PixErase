import grpc.aio

from pix_erase.presentation.grpc.v1.generated.v1 import health_pb2, health_pb2_grpc


class HealthServiceServicer(health_pb2_grpc.HealthServiceServicer):
    async def Check(  # noqa: N802
        self,
        request: health_pb2.HealthCheckRequest,  # noqa: ARG002
        context: grpc.aio.ServicerContext,  # noqa: ARG002
    ) -> health_pb2.HealthCheckResponse:
        return health_pb2.HealthCheckResponse(message="ok", status="success")
