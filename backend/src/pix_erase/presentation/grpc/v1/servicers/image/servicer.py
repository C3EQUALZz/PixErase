from collections.abc import AsyncIterator
from uuid import UUID

import grpc.aio
from dishka import FromDishka
from dishka.integrations.grpcio import inject
from google.protobuf.empty_pb2 import Empty

from pix_erase.application.commands.image.compress_image import CompressImageCommand, CompressImageCommandHandler
from pix_erase.application.commands.image.create_image import CreateImageCommand, CreateImageCommandHandler
from pix_erase.application.commands.image.delete_image import DeleteImageCommand, DeleteImageCommandHandler
from pix_erase.application.commands.image.grayscale_image import (
    ConvertImageToGrayscaleCommand,
    GrayscaleImageCommandHandler,
)
from pix_erase.application.commands.image.remove_background_image import (
    RemoveBackgroundImageCommand,
    RemoveBackgroundImageCommandHandler,
)
from pix_erase.application.commands.image.rotate_image import RotateImageCommand, RotateImageCommandHandler
from pix_erase.application.commands.image.upscale_image import UpscaleImageCommand, UpscaleImageCommandHandler
from pix_erase.application.queries.images.read_by_id import ReadImageByIDQuery, ReadImageByIDQueryHandler
from pix_erase.application.queries.images.read_exif_from_image_by_id import (
    ReadExifFromImageByIDQuery,
    ReadExifFromImageByIDQueryHandler,
)
from pix_erase.presentation.grpc.v1.generated.v1 import image_pb2, image_pb2_grpc


class ImageServiceServicer(image_pb2_grpc.ImageServiceServicer):
    @inject
    async def CreateImage(  # noqa: N802
        self,
        request: image_pb2.CreateImageRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[CreateImageCommandHandler],
    ) -> image_pb2.CreateImageResponse:
        command = CreateImageCommand(data=request.image_data, filename=request.filename)
        view = await handler(command)
        return image_pb2.CreateImageResponse(image_id=str(view.image_id))

    @inject
    async def ReadImage(  # noqa: N802
        self,
        request: image_pb2.ReadImageRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ReadImageByIDQueryHandler],
    ) -> AsyncIterator[image_pb2.ReadImageChunk]:
        query = ReadImageByIDQuery(image_id=UUID(request.image_id))
        view = await handler(query)
        async for chunk in view.data:
            yield image_pb2.ReadImageChunk(data=chunk)

    @inject
    async def DeleteImage(  # noqa: N802
        self,
        request: image_pb2.DeleteImageRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[DeleteImageCommandHandler],
    ) -> Empty:
        command = DeleteImageCommand(image_id=UUID(request.image_id))
        await handler(command)
        return Empty()

    @inject
    async def ReadImageExif(  # noqa: N802
        self,
        request: image_pb2.ReadImageExifRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[ReadExifFromImageByIDQueryHandler],
    ) -> image_pb2.ReadImageExifResponse:
        query = ReadExifFromImageByIDQuery(image_id=UUID(request.image_id))
        view = await handler(query)
        return image_pb2.ReadImageExifResponse(
            width=view.width,
            height=view.height,
            format=view.format,
            is_animated=view.is_animated,
            camera_settings=image_pb2.CameraSettingsExif(
                make=view.camera_settings.make,
                model=view.camera_settings.model,
                orientation=view.camera_settings.orientation.value,
                focal_length=view.camera_settings.focal_length,
                focal_length_35mm=view.camera_settings.focal_length_35mm,
                max_aperture=view.camera_settings.max_aperture,
                aperture_value=view.camera_settings.aperture_value,
            ),
            exposure_settings=image_pb2.ExposureSettings(
                exposure_time=view.exposure_settings.exposure_time,
                aperture=view.exposure_settings.aperture,
                iso=view.exposure_settings.iso,
                exposure_bias=view.exposure_settings.exposure_bias,
                metering_mode=view.exposure_settings.metering_mode.value,
                white_balance=view.exposure_settings.white_balance.value,
            ),
            flash_info=image_pb2.FlashInfo(
                fired=view.flash_info.fired,
                mode=view.flash_info.mode.value,
                return_light=view.flash_info.return_light,
                function_present=view.flash_info.function_present,
                red_eye_reduction=view.flash_info.red_eye_reduction,
            ),
            gps_info=image_pb2.GPSInfo(
                latitude=view.gps_info.latitude,
                longitude=view.gps_info.longitude,
                altitude=view.gps_info.altitude,
                latitude_ref=view.gps_info.latitude_ref,
                longitude_ref=view.gps_info.longitude_ref,
            ),
            datetime_info=image_pb2.DateTimeInfo(
                created=view.datetime_info.created.isoformat(),
                digitized=view.datetime_info.digitized.isoformat(),
                original=view.datetime_info.original.isoformat(),
            ),
        )

    @inject
    async def CompressImage(  # noqa: N802
        self,
        request: image_pb2.CompressImageRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[CompressImageCommandHandler],
    ) -> image_pb2.TaskResponse:
        command = CompressImageCommand(image_id=UUID(request.image_id), quality=request.quality)
        task_id = await handler(command)
        return image_pb2.TaskResponse(task_id=str(task_id))

    @inject
    async def GrayscaleImage(  # noqa: N802
        self,
        request: image_pb2.GrayscaleImageRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[GrayscaleImageCommandHandler],
    ) -> image_pb2.TaskResponse:
        command = ConvertImageToGrayscaleCommand(image_id=UUID(request.image_id))
        task_id = await handler(command)
        return image_pb2.TaskResponse(task_id=str(task_id))

    @inject
    async def RemoveBackground(  # noqa: N802
        self,
        request: image_pb2.RemoveBackgroundRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[RemoveBackgroundImageCommandHandler],
    ) -> image_pb2.TaskResponse:
        command = RemoveBackgroundImageCommand(image_id=UUID(request.image_id))
        task_id = await handler(command)
        return image_pb2.TaskResponse(task_id=str(task_id))

    @inject
    async def RotateImage(  # noqa: N802
        self,
        request: image_pb2.RotateImageRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[RotateImageCommandHandler],
    ) -> image_pb2.TaskResponse:
        command = RotateImageCommand(image_id=UUID(request.image_id), angle=request.angle)
        task_id = await handler(command)
        return image_pb2.TaskResponse(task_id=str(task_id))

    @inject
    async def UpscaleImage(  # noqa: N802
        self,
        request: image_pb2.UpscaleImageRequest,
        context: grpc.aio.ServicerContext,  # noqa: ARG002
        handler: FromDishka[UpscaleImageCommandHandler],
    ) -> image_pb2.TaskResponse:
        command = UpscaleImageCommand(
            image_id=UUID(request.image_id),
            algorithm=request.algorithm,
            scale=request.scale,
        )
        task_id = await handler(command)
        return image_pb2.TaskResponse(task_id=str(task_id))
