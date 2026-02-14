from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReadUserByIDRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class ReadUserByIDResponse(_message.Message):
    __slots__ = ("id", "email", "name", "role")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    name: str
    role: str
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., name: _Optional[str] = ..., role: _Optional[str] = ...) -> None: ...

class ReadAllUsersRequest(_message.Message):
    __slots__ = ("limit", "offset", "sorting_field", "sorting_order")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    SORTING_FIELD_FIELD_NUMBER: _ClassVar[int]
    SORTING_ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    sorting_field: str
    sorting_order: str
    def __init__(self, limit: _Optional[int] = ..., offset: _Optional[int] = ..., sorting_field: _Optional[str] = ..., sorting_order: _Optional[str] = ...) -> None: ...

class ReadAllUsersResponse(_message.Message):
    __slots__ = ("users",)
    USERS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[ReadUserByIDResponse]
    def __init__(self, users: _Optional[_Iterable[_Union[ReadUserByIDResponse, _Mapping]]] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("email", "name", "password", "role")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    password: str
    role: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ..., password: _Optional[str] = ..., role: _Optional[str] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class ActivateUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class ChangeUserEmailRequest(_message.Message):
    __slots__ = ("user_id", "new_email")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_EMAIL_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    new_email: str
    def __init__(self, user_id: _Optional[str] = ..., new_email: _Optional[str] = ...) -> None: ...

class ChangeUserNameRequest(_message.Message):
    __slots__ = ("user_id", "new_name")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    new_name: str
    def __init__(self, user_id: _Optional[str] = ..., new_name: _Optional[str] = ...) -> None: ...

class ChangeUserPasswordRequest(_message.Message):
    __slots__ = ("user_id", "password")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    password: str
    def __init__(self, user_id: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GrantAdminRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class RevokeAdminRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...
