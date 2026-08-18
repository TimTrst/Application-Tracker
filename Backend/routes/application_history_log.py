from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from repositories.dependencies import get_application_history_log_repository
from repositories.interfaces.application_history_log_repository import (
    ApplicationHistoryLogRepository,
    ReadApplicationHistoryTransition,
)

router = APIRouter(tags=["log"])


@router.get("/transitions", response_model=list[ReadApplicationHistoryTransition])
def get_application_history_transitions(
    repo: ApplicationHistoryLogRepository = Depends(
        get_application_history_log_repository
    ),
):
    try:
        return repo.get_transitions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
