from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from typing import Annotated
from models.application import ReadApplication, WriteApplication, UpdateApplication
from repositories.interfaces.application_repository import ApplicationRepository
from services.application_service import ApplicationService
from services.dependencies import get_application_service
from repositories.dependencies import get_application_repository

# Two injectables are available for these routes:
# - ApplicationRepository (get_application_repository): plain CRUD against
#   the applications table only. Used below for reads/deletes, which have
#   no side effects on other tables.
# - ApplicationService (get_application_service): wraps an
#   ApplicationRepository *and* an ApplicationHistoryLogRepository so that
#   creating an application or changing its status also writes a history
#   log entry. Used below for POST/PATCH, where a status/phase change must
#   be tracked.

router = APIRouter(tags=["applications"])


@router.get("/", response_model=list[ReadApplication])
def read_applications(
    repo: ApplicationRepository = Depends(get_application_repository),
):
    return repo.get_all()


@router.get("/{id}", response_model=ReadApplication)
def read_application(
    id: Annotated[int, Path(gt=0)],
    repo: ApplicationRepository = Depends(get_application_repository),
):
    try:
        application = repo.get_by_id(id)

        if not application:
            raise HTTPException(status_code=404, detail="Item not found")
        return application
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ReadApplication)
def write_application(
    application: WriteApplication,
    service: ApplicationService = Depends(get_application_service),
):
    try:
        return service.add(application)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=204)
def delete_application(
    id: Annotated[int, Path(gt=0)],
    repo: ApplicationRepository = Depends(get_application_repository),
):
    try:
        if not repo.remove(id):
            raise HTTPException(status_code=404, detail="Application not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=ReadApplication)
def update_application(
    id: Annotated[int, Path(gt=0)],
    updated_application: UpdateApplication,
    service: ApplicationService = Depends(get_application_service),
):
    try:
        result = service.modify(id, updated_application)
        if not result:
            raise HTTPException(status_code=404, detail="Application not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
