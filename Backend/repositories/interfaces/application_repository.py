from abc import ABC, abstractmethod
from models.application import WriteApplication, UpdateApplication, ReadApplication


class ApplicationRepository(ABC):
    """Contract for storing/retrieving applications. No mention of sqlite,
    connections, or SQL anywhere in here - that's the whole point."""

    @abstractmethod
    def get_all(self) -> list[ReadApplication]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> ReadApplication | None: ...

    @abstractmethod
    def add(self, new_application: WriteApplication) -> ReadApplication: ...

    @abstractmethod
    def remove(self, id: int) -> bool: ...

    @abstractmethod
    def modify(
        self, id: int, updated_application: UpdateApplication
    ) -> ReadApplication | bool: ...
