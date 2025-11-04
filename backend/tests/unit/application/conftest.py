from typing import cast
from unittest.mock import AsyncMock, Mock, create_autospec

import pytest

from pix_erase.application.common.ports.event_bus import EventBus
from pix_erase.application.common.ports.transaction_manager import TransactionManager
from pix_erase.application.common.ports.user.command_gateway import UserCommandGateway
from pix_erase.application.common.ports.user.query_gateway import UserQueryGateway
from pix_erase.application.common.services.current_user import CurrentUserService
from pix_erase.domain.internet_protocol.services import InternetProtocolService
from pix_erase.domain.internet_protocol.services.internet_domain_service import InternetDomainService
from pix_erase.domain.user.ports.id_generator import UserIdGenerator
from pix_erase.domain.user.ports.password_hasher import PasswordHasher
from pix_erase.domain.user.services.access_service import AccessService
from pix_erase.domain.user.services.user_service import UserService
from pix_erase.domain.user.values.hashed_password import HashedPassword
from tests.unit.factories.user_entity import create_user
from tests.unit.factories.value_objects import create_user_id


@pytest.fixture
def fake_transaction() -> TransactionManager:
    fake = Mock()
    fake.commit = AsyncMock()
    fake.flush = AsyncMock()
    return cast("TransactionManager", fake)


@pytest.fixture
def fake_user_command_gateway() -> UserCommandGateway:
    fake = Mock()
    fake.add = AsyncMock()
    fake.read_by_id = AsyncMock()
    fake.read_by_email = AsyncMock()
    fake.delete_by_id = AsyncMock()
    fake.update = AsyncMock()
    return cast("UserCommandGateway", fake)


@pytest.fixture
def fake_current_user_service() -> CurrentUserService:
    fake = Mock()
    fake.get_current_user = AsyncMock(return_value=create_user())
    return cast("CurrentUserService", fake)


@pytest.fixture
def fake_event_bus() -> EventBus:
    fake = Mock()
    fake.publish = AsyncMock()
    return cast("EventBus", fake)


@pytest.fixture
def fake_password_hasher() -> PasswordHasher:
    fake = Mock()
    fake.hash = Mock(return_value=HashedPassword(b"hashed_password"))
    fake.verify = Mock(return_value=True)
    return cast("PasswordHasher", fake)


@pytest.fixture
def fake_user_id_generator() -> UserIdGenerator:
    fake = Mock()
    fake.return_value = create_user_id()
    return cast("UserIdGenerator", fake)


@pytest.fixture
def fake_user_service() -> UserService:
    fake = Mock()
    fake.create = Mock(return_value=create_user())
    fake.change_email = Mock()
    fake.change_name = Mock()
    fake.change_password = Mock()
    fake.pull_events = Mock(return_value=[])
    return cast("UserService", fake)


@pytest.fixture
def fake_access_service() -> AccessService:
    fake = Mock()
    fake.authorize = Mock()
    fake.toggle_user_admin_role = Mock()
    fake.toggle_user_activation = Mock()
    fake.pull_events = Mock(return_value=[])
    return cast("AccessService", fake)


@pytest.fixture
def fake_user_query_gateway() -> UserQueryGateway:
    fake = Mock()
    fake.read_user_by_id = AsyncMock()
    fake.read_all_users = AsyncMock()
    return cast("UserQueryGateway", fake)

@pytest.fixture
def fake_internet_service() -> InternetProtocolService:
    return cast("InternetProtocolService", create_autospec(InternetProtocolService))


@pytest.fixture
def fake_internet_domain_service() -> InternetDomainService:
    return cast("InternetDomainService", create_autospec(InternetDomainService))
