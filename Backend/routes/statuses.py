from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from models.status import ReadStatus, WriteStatus, UpdateStatus
from repositories.interfaces.status_repository import StatusRepository
from repositories.dependencies import get_status_repository

router = APIRouter(tags=["statuses"])


@router.get("/", response_model=list[ReadStatus])
def read_states(repo: StatusRepository = Depends(get_status_repository)):
    return repo.get_all()


@router.get("/{id}", response_model=ReadStatus)
def read_status(
    id: Annotated[int, Path(gt=0)],
    repo: StatusRepository = Depends(get_status_repository),
):
    try:
        status = repo.get_by_id(id)

        if not status:
            raise HTTPException(status_code=404, detail="Item not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ReadStatus)
def write_status(
    status: WriteStatus, repo: StatusRepository = Depends(get_status_repository)
):
    try:
        return repo.add(status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
def delete_status(
    id: Annotated[int, Path(gt=0)],
    repo: StatusRepository = Depends(get_status_repository),
):
    try:
        if not repo.remove(id):
            raise HTTPException(status_code=404, detail="Status not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=ReadStatus)
def update_status(
    id: Annotated[int, Path(gt=0)],
    updated_status: UpdateStatus,
    repo: StatusRepository = Depends(get_status_repository),
):
    try:
        updated_status = repo.modify(id, updated_status)
        if not updated_status:
            raise HTTPException(status_code=404, detail="Status not found")
        return updated_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
