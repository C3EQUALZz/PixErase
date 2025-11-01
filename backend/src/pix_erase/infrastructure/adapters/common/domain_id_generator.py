from typing import cast
from uuid import uuid4

from typing_extensions import override

from pix_erase.domain.internet_protocol.ports.domain_id_generator import DomainIdGenerator
from pix_erase.domain.internet_protocol.values.domain_id import DomainID


class UUID4DomainIDGenerator(DomainIdGenerator):
    @override
    def __call__(self) -> DomainID:
        return cast("DomainID", uuid4())
