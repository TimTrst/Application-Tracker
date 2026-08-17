from repositories.interfaces.application_repository import ApplicationRepository
from repositories.interfaces.application_history_log_repository import (
    ApplicationHistoryLogRepository,
)
from models.application import WriteApplication, ReadApplication, UpdateApplication
from models.application_history_log import BaseApplicationHistoryLog


class ApplicationService:
    """This service combines two repositories (ApplicationRepository and ApplicationHistoryLogRepository)
    As new applications are added, their status or phases change -> this place bundles the changes for the applications and stores these changes in the history log aswell.
    """

    def __init__(
        self,
        application_repo: ApplicationRepository,
        history_log_repo: ApplicationHistoryLogRepository,
    ):
        self._application_repo = application_repo
        self._history_log_repo = history_log_repo

    def add(self, new_application: WriteApplication) -> ReadApplication:
        """Create a new application and seed its history log with the initial status/phase."""
        created = self._application_repo.add(new_application)

        history_entry = BaseApplicationHistoryLog(
            application_id=created.id,
            phase_id=created.status.phase.id,
            status_id=created.status.id,
        )
        self._history_log_repo.add(history_entry)

        return created

    def modify(
        self, id: int, updated_application: UpdateApplication
    ) -> ReadApplication | bool:
        """Update an application and append a history entry only if its status actually changed."""
        previous, updated = self._application_repo.modify(id, updated_application)

        # Only log a history entry on an actual status transition, not on every edit
        # (e.g. editing notes shouldn't create a spurious history record).
        if previous.status.id != updated.status.id:
            history_entry = BaseApplicationHistoryLog(
                application_id=updated.id,
                phase_id=updated.status.phase.id,
                status_id=updated.status.id,
            )
            self._history_log_repo.add(history_entry)

        return updated
