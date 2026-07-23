from abc import ABC, abstractmethod
from models.phase import ReadPhase, BasePhase, BasePhaseOptional


class PhaseRepository(ABC):
    """Interface for storing/retrieving statuses"""

    @abstractmethod
    def get_all(self) -> list[ReadPhase]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> ReadPhase: ...

    @abstractmethod
    def add(self, new_phase: BasePhase) -> ReadPhase: ...

    @abstractmethod
    def remove(self, id: int) -> bool: ...

    @abstractmethod
    def modify(self, id: int, updated_phase: BasePhaseOptional) -> ReadPhase: ...
