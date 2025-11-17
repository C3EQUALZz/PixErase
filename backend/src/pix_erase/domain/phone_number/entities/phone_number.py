from dataclasses import dataclass

from pix_erase.domain.common.entities.base_entity import BaseEntity
from pix_erase.domain.phone_number.values.operator_of_phone_number import OperatorOfPhoneNumber
from pix_erase.domain.phone_number.values.phone_id import PhoneID
from pix_erase.domain.phone_number.values.raw_phone_number import RawPhoneNumber
from pix_erase.domain.phone_number.values.region_of_phone_number import RegionOfPhoneNumber
from pix_erase.domain.phone_number.values.timezone_of_phone_number import TimezoneOfPhoneNumber
from pix_erase.domain.phone_number.values.type_of_phone_number import TypeOfPhoneNumber


@dataclass(eq=False, kw_only=True)
class PhoneNumber(BaseEntity[PhoneID]):
    type_number: TypeOfPhoneNumber
    operator: OperatorOfPhoneNumber
    region: RegionOfPhoneNumber
    timezone: TimezoneOfPhoneNumber
    number: RawPhoneNumber
