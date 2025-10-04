from pix_erase.application.errors.base import ApplicationError


class ImageNotFoundError(ApplicationError):
    ...


class ImageDoesntBelongToThisUserError(ApplicationError):
    ...
