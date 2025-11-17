import logging
from typing import TYPE_CHECKING, Final

from pix_erase.domain.common.services.base import DomainService
from pix_erase.domain.phone_number.entities.phone_number import PhoneNumber
from pix_erase.domain.phone_number.ports.phone_id_generator import PhoneIDGenerator
from pix_erase.domain.phone_number.ports.phone_info_service_port import PhoneInfoServicePort
from pix_erase.domain.phone_number.values.raw_phone_number import RawPhoneNumber

if TYPE_CHECKING:
    from pix_erase.domain.phone_number.values import (
        OperatorOfPhoneNumber,
        RegionOfPhoneNumber,
        TimezoneOfPhoneNumber,
        TypeOfPhoneNumber,
    )

logger: Final[logging.Logger] = logging.getLogger(__name__)


class PhoneService(DomainService):
    def __init__(
        self,
        phone_id_generator: PhoneIDGenerator,
        phone_info_service: PhoneInfoServicePort,
    ) -> None:
        super().__init__()
        self._phone_id_generator: Final[PhoneIDGenerator] = phone_id_generator
        self._phone_info_service: Final[PhoneInfoServicePort] = phone_info_service

    def create(
        self,
        raw_phone_number: RawPhoneNumber,
    ) -> PhoneNumber:
        logger.debug("Started processing raw phone number: %s", raw_phone_number)

        logger.debug("Started getting type number for raw phone number: %s", raw_phone_number)
        type_number: TypeOfPhoneNumber = self._phone_info_service.get_type_number(raw_phone_number)
        logger.debug("Got type number for raw phone number: %s", type_number)

        logger.debug("Started getting operator for raw phone number: %s", raw_phone_number)
        operator: OperatorOfPhoneNumber = self._phone_info_service.get_operator(raw_phone_number)
        logger.debug("Got operator for raw phone number: %s", operator)

        logger.debug("Started getting region for raw phone number: %s", raw_phone_number)
        region: RegionOfPhoneNumber = self._phone_info_service.get_region(raw_phone_number)
        logger.debug("Got region for raw phone number: %s", region)

        logger.debug("Started getting timezone for raw phone number: %s", raw_phone_number)
        timezone: TimezoneOfPhoneNumber = self._phone_info_service.get_timezone(raw_phone_number)
        logger.debug("Got timezone for raw phone number: %s", timezone)

        new_entity = PhoneNumber(
            id=self._phone_id_generator(),
            type_number=type_number,
            operator=operator,
            region=region,
            timezone=timezone,
            number=raw_phone_number,
        )

        logger.debug("Got info about raw number: %s, %s", raw_phone_number, new_entity)

        return new_entity
