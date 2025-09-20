from pix_erase.application.errors.base import ApplicationError


class AlreadyAuthenticatedError(ApplicationError): ...


class AuthenticationError(ApplicationError): ...
