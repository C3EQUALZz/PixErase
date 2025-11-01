from typing import Final

from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode, Tracer
from typing_extensions import override

from pix_erase.application.common.ports.image.storage import ImageStorage
from pix_erase.application.common.query_models.image import ImageStreamQueryModel
from pix_erase.domain.image.entities.image import Image
from pix_erase.domain.image.values.image_id import ImageID

tracer: Final[Tracer] = trace.get_tracer(__name__)


class TraceableFileStorage(ImageStorage):
    def __init__(self, image_storage: ImageStorage) -> None:
        self._image_storage: Final[ImageStorage] = image_storage

    @override
    async def add(self, image: Image) -> None:
        span_name = "image.storage.add"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            _set_image_attributes(span, image)
            span.set_attribute("image.storage.operation", "add")
            try:
                await self._image_storage.add(image)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def read_by_id(self, image_id: ImageID) -> Image:
        span_name = "image.storage.read_by_id"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("image.storage.operation", "read_by_id")
            span.set_attribute("image.id", str(image_id))
            try:
                image = await self._image_storage.read_by_id(image_id)
                _set_image_attributes(span, image)
                span.set_status(Status(StatusCode.OK))
                return image
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def delete_by_id(self, image_id: ImageID) -> None:
        span_name = "image.storage.delete_by_id"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("image.storage.operation", "delete_by_id")
            span.set_attribute("image.id", str(image_id))
            try:
                await self._image_storage.delete_by_id(image_id)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def update(self, image: Image) -> None:
        span_name = "image.storage.update"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            _set_image_attributes(span, image)
            span.set_attribute("image.storage.operation", "update")
            try:
                await self._image_storage.update(image)
                span.set_status(Status(StatusCode.OK))
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise

    @override
    async def stream_by_id(self, image_id: ImageID) -> ImageStreamQueryModel | None:
        span_name = "image.storage.stream_by_id"
        with tracer.start_as_current_span(span_name, kind=SpanKind.INTERNAL) as span:
            span.set_attribute("image.storage.operation", "stream_by_id")
            span.set_attribute("image.id", str(image_id))
            try:
                stream = await self._image_storage.stream_by_id(image_id)
                if stream is not None:
                    span.set_attribute("image.stream.exists", True)
                else:
                    span.set_attribute("image.stream.exists", False)
                span.set_status(Status(StatusCode.OK))
                return stream
            except Exception as exc:  # noqa: BLE001
                span.record_exception(exc)
                span.set_status(Status(StatusCode.ERROR))
                raise


def _set_image_attributes(span: trace.Span, image: Image) -> None:
    """Set image-related attributes on a span."""
    span.set_attribute("image.id", str(image.id))
    span.set_attribute("image.size", len(image.data))
    span.set_attribute("image.width", image.width.value)
    span.set_attribute("image.height", image.height.value)
    span.set_attribute("image.name", str(image.name))
