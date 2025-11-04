from typing import Final, override

from sqlalchemy import Select, and_, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pix_erase.application.common.ports.image.comparison_gateway import ImageComparisonGateway
from pix_erase.domain.image.entities.image_comparison import ImageComparison
from pix_erase.domain.image.values.comparison_id import ComparisonID
from pix_erase.domain.image.values.image_id import ImageID
from pix_erase.infrastructure.adapters.persistence.constants import DB_QUERY_FAILED
from pix_erase.infrastructure.errors.transaction_manager import RepoError


class SqlAlchemyImageComparisonGateway(ImageComparisonGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def add(self, comparison: ImageComparison) -> None:
        try:
            self._session.add(comparison)
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error

    @override
    async def read_by_id(self, comparison_id: ComparisonID) -> ImageComparison | None:
        select_stmt: Select[tuple[ImageComparison]] = select(ImageComparison).where(
            ImageComparison.id == comparison_id  # type: ignore
        )

        try:
            comparison: ImageComparison | None = (await self._session.execute(select_stmt)).scalar_one_or_none()
        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
        else:
            return comparison

    @override
    async def read_by_image_ids(
        self,
        first_image_id: ImageID,
        second_image_id: ImageID,
    ) -> ImageComparison | None:
        """Find comparison by image IDs (order-independent)."""
        select_stmt: Select[tuple[ImageComparison]] = select(ImageComparison).where(
            or_(
                and_(
                    ImageComparison.first_image_id == first_image_id,  # type: ignore
                    ImageComparison.second_image_id == second_image_id,  # type: ignore
                ),
                and_(
                    ImageComparison.first_image_id == second_image_id,  # type: ignore
                    ImageComparison.second_image_id == first_image_id,  # type: ignore
                ),
            )
        )

        try:
            comparison: ImageComparison | None = (await self._session.execute(select_stmt)).scalar_one_or_none()

        except SQLAlchemyError as error:
            raise RepoError(DB_QUERY_FAILED) from error
        else:
            return comparison
