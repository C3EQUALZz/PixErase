import logging
from typing import Any, Final

import grpc
import grpc.aio

logger: Final[logging.Logger] = logging.getLogger(__name__)


class LoggingInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Any,  # noqa: ANN401
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:  # noqa: ANN401
        method = handler_call_details.method
        logger.info("gRPC request: method=%s", method)

        response = await continuation(handler_call_details)

        logger.info("gRPC response: method=%s completed", method)
        return response
