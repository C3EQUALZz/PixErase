import secrets

from typing_extensions import override

from pix_erase.infrastructure.auth.session.id_generator import AuthSessionIDGenerator


class SecretsAuthSessionIdGenerator(AuthSessionIDGenerator):
    @override
    def __call__(self) -> str:
        return secrets.token_urlsafe(32)
