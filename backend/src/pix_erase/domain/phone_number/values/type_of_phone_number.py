from enum import StrEnum


class TypeOfPhoneNumber(StrEnum):
    FIXED_LINE = "fixed line phone number"
    MOBILE = "mobile phone number"
    FIXED_LINE_OR_MOBILE = "fixed line or mobile phone number"
    TOLL_FREE = "toll free phone number"
    PREMIUM_RATE = "premium rate phone number"
    SHARED_COST = "shared cost phone number"
    VOIP = "voice over IP numbers phone number"
    PERSONAL_NUMBER = "personal phone number"
    PAGER = "pager phone number"
    UAN = "company phone number"
    VOICEMAIL = "voice mail access number"
    UNKNOWN = "unknown phone number"
