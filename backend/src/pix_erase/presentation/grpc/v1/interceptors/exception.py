import logging
from types import MappingProxyType
from typing import Any, Final

import grpc
import grpc.aio

from pix_erase.application.errors.auth import AlreadyAuthenticatedError, AuthenticationError
from pix_erase.application.errors.base import ApplicationError
from pix_erase.application.errors.user import UserNotFoundByEmailError, UserNotFoundByIDError
from pix_erase.domain.common.errors.base import AppError, DomainError, DomainFieldError
from pix_erase.domain.user.errors.access_service import AuthorizationError
from pix_erase.infrastructure.errors.base import InfrastructureError
from pix_erase.infrastructure.errors.transaction_manager import RepoError, RollbackError

logger: Final[logging.Logger] = logging.getLogger(__name__)

ERROR_TO_GRPC_STATUS: Final[MappingProxyType[type[Exception], grpc.StatusCode]] = MappingProxyType(
    {
        DomainFieldError: grpc.StatusCode.INVALID_ARGUMENT,
        AuthenticationError: grpc.StatusCode.UNAUTHENTICATED,
        AuthorizationError: grpc.StatusCode.PERMISSION_DENIED,
        AlreadyAuthenticatedError: grpc.StatusCode.PERMISSION_DENIED,
        UserNotFoundByIDError: grpc.StatusCode.NOT_FOUND,
        UserNotFoundByEmailError: grpc.StatusCode.NOT_FOUND,
        DomainError: grpc.StatusCode.INTERNAL,
        ApplicationError: grpc.StatusCode.INTERNAL,
        InfrastructureError: grpc.StatusCode.INTERNAL,
        AppError: grpc.StatusCode.INTERNAL,
        RepoError: grpc.StatusCode.UNAVAILABLE,
        RollbackError: grpc.StatusCode.UNAVAILABLE,
    }
)


def _resolve_status(exc: Exception) -> grpc.StatusCode:
    for exc_type, status_code in ERROR_TO_GRPC_STATUS.items():
        if isinstance(exc, exc_type):
            return status_code
    return grpc.StatusCode.INTERNAL


class ExceptionInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(
        self,
        continuation: Any,  # noqa: ANN401
        handler_call_details: grpc.HandlerCallDetails,
    ) -> Any:  # noqa: ANN401
        handler = await continuation(handler_call_details)
        if handler is None:
            return handler

        if handler.unary_unary:
            original = handler.unary_unary

            async def wrapped_unary_unary(request: Any, context: grpc.aio.ServicerContext) -> Any:  # noqa: ANN401
                try:
                    return await original(request, context)
                except Exception as exc:  # noqa: BLE001
                    await self._handle_exception(exc, handler_call_details, context)

            handler.unary_unary = wrapped_unary_unary

        if handler.unary_stream:
            original_stream = handler.unary_stream

            async def wrapped_unary_stream(
                request: Any,  # noqa: ANN401
                context: grpc.aio.ServicerContext,
            ) -> Any:  # noqa: ANN401
                try:
                    async for chunk in original_stream(request, context):
                        yield chunk
                except Exception as exc:  # noqa: BLE001
                    await self._handle_exception(exc, handler_call_details, context)

            handler.unary_stream = wrapped_unary_stream

        return handler

    @staticmethod
    async def _handle_exception(
        exc: Exception,
        handler_call_details: grpc.HandlerCallDetails,
        context: grpc.aio.ServicerContext,
    ) -> None:
        status_code = _resolve_status(exc)

        if status_code in {grpc.StatusCode.INTERNAL, grpc.StatusCode.UNAVAILABLE}:
            logger.exception(
                "gRPC exception '%s' in %s",
                type(exc).__name__,
                handler_call_details.method,
            )
            details = "Internal server error."
        else:
            logger.warning(
                "gRPC exception '%s' in %s: '%s'",
                type(exc).__name__,
                handler_call_details.method,
                exc,
            )
            details = str(exc)

        await context.abort(status_code, details)
