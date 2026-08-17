from abc import ABC, abstractmethod
from models.application_history_log import (
    BaseApplicationHistoryLog,
    ReadApplicationHistoryLog,
)


class ApplicationHistoryLogRepository(ABC):
    """Interfaces for storing/retrieving the history log of added/modified applications."""

    @abstractmethod
    def get_all(self) -> list[ReadApplicationHistoryLog]: ...

    @abstractmethod
    def add(
        self, new_history_log: BaseApplicationHistoryLog
    ) -> ReadApplicationHistoryLog: ...
