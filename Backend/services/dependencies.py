from fastapi import Depends

from repositories.dependencies import (
    get_application_repository,
    get_application_history_log_repository,
)
from repositories.interfaces.application_repository import ApplicationRepository
from repositories.interfaces.application_history_log_repository import (
    ApplicationHistoryLogRepository,
)
from services.application_service import ApplicationService


def get_application_service(
    application_repo: ApplicationRepository = Depends(get_application_repository),
    history_log_repo: ApplicationHistoryLogRepository = Depends(
        get_application_history_log_repository
    ),
) -> ApplicationService:
    return ApplicationService(application_repo, history_log_repo)
