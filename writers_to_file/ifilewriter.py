from abc import ABCMeta, abstractmethod
from typing import AnyStr


class IFileWriter(metaclass=ABCMeta):
    @abstractmethod
    def write(self, data: AnyStr, path: str, format: str) -> None:
        pass
