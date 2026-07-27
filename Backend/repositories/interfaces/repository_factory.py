from abc import ABC, abstractmethod
from repositories.interfaces.application_repository import ApplicationRepository
from repositories.interfaces.status_repository import StatusRepository
from repositories.interfaces.phase_repository import PhaseRepository


# Contract every DB backend must fulfil to be usable via dependencies.py.
# A backend (e.g. SqliteRepositoryFactory) implements this to bundle the
# construction of all repositories that share one underlying connection.
# Routes never see this directly - they only receive the repositories it
# produces, via the get_*_repository dependencies.
class RepositoryFactory(ABC):
    @abstractmethod
    def application_repository(self) -> ApplicationRepository: ...

    @abstractmethod
    def status_repository(self) -> StatusRepository: ...

    @abstractmethod
    def phase_repository(self) -> PhaseRepository: ...
