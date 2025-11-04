from abc import abstractmethod
from typing import Protocol


class AuthSessionIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> str: ...
