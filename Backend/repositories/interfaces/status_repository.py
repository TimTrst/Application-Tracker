from abc import ABC, abstractmethod
from models.status import ReadStatus, WriteStatus, UpdateStatus


class StatusRepository(ABC):
    """Interface for storing/retrieving statuses"""

    @abstractmethod
    def get_all(self) -> list[ReadStatus]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> ReadStatus | None: ...

    @abstractmethod
    def add(self, new_status: WriteStatus) -> ReadStatus | None: ...

    @abstractmethod
    def remove(self, id: int) -> bool: ...

    @abstractmethod
    def modify(
        self, id: int, updated_status: UpdateStatus
    ) -> ReadStatus | None | bool: ...
