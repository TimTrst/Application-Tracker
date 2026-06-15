from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from models.status import ReadStatus, WriteStatus, UpdateStatus
from database.database import get_db
from repositories.status_repository import get_all_states, get_status_by_id, add_status, remove_status, modify_status

router = APIRouter(tags=["statuses"])


@router.get("/", response_model=list[ReadStatus])
def read_states(conn=Depends(get_db)):
    return get_all_states(conn)


@router.get("/{id}", response_model=ReadStatus)
def read_status(id: Annotated[int, Path(gt=0)], conn=Depends(get_db)):
    try:
        status = get_status_by_id(id, conn)

        if not status:
            raise HTTPException(status_code=404, detail="Item not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ReadStatus)
def write_status(status: WriteStatus, conn=Depends(get_db)):
    try:
        return add_status(status, conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
def delete_status(id: Annotated[int, Path(gt=0)], conn=Depends(get_db)):
    try:
        if not remove_status(id, conn):
            raise HTTPException(
                status_code=404, detail="Status not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=ReadStatus)
def update_status(id: Annotated[int, Path(gt=0)], updated_status: UpdateStatus, conn=Depends(get_db)):
    try:
        updated_status = modify_status(id, updated_status, conn)
        if not updated_status:
            raise HTTPException(
                status_code=404, detail="Status not found")
        return updated_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
