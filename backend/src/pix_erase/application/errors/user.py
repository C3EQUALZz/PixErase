from pix_erase.application.errors.base import ApplicationError


class UserAlreadyExistsError(ApplicationError): ...


class UserNotFoundByEmailError(ApplicationError): ...


class UserNotFoundByIDError(ApplicationError): ...
