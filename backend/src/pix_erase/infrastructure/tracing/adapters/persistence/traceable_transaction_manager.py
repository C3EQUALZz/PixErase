from typing import Final

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode, Tracer
from typing_extensions import override

from pix_erase.application.common.ports.transaction_manager import TransactionManager

tracer: Final[Tracer] = trace.get_tracer(__name__)


class TraceableTransactionManager(TransactionManager):
    def __init__(self, transaction_manager: TransactionManager) -> None:
        self._transaction_manager: Final[TransactionManager] = transaction_manager

    @override
    async def commit(self) -> None:
        """
        Save all operations in database.
        :return: Nothing
        """
        span_name = "transaction_manager.commit"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.transaction.operation", "commit")
            try:
                await self._transaction_manager.commit()
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def flush(self) -> None:
        span_name = "transaction_manager.flush"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.transaction.operation", "flush")
            try:
                await self._transaction_manager.flush()
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def rollback(self) -> None:
        """
        Method that rolls back all operations.
        :return: Nothing
        """
        span_name = "transaction_manager.rollback"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("db.transaction.operation", "rollback")
            try:
                await self._transaction_manager.rollback()
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise
