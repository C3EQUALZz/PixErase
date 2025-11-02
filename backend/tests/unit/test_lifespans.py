from unittest import mock

from pix_erase.infrastructure.persistence.provider import get_engine
from pix_erase.web import lifespan


@mock.patch("pix_erase.infrastructure.persistence.provider.create_async_engine")
async def test_engine(fake_create_async_engine: mock.Mock) -> None:
    fake_create_async_engine.return_value.dispose = mock.AsyncMock()
    fake_database_config = mock.Mock()
    fake_alchemy_config = mock.Mock()

    async for _ in get_engine(fake_database_config, fake_alchemy_config):
        pass

    fake_create_async_engine.return_value.dispose.assert_called_once()


async def test_lifespan() -> None:
    fake_app = mock.Mock()
    fake_app.state.dishka_container.close = mock.AsyncMock()
    async with lifespan(fake_app):
        pass
    fake_app.state.dishka_container.close.assert_called_once()
