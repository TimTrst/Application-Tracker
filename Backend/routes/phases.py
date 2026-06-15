from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from models.phase import ReadPhase, BasePhaseOptional, BasePhase
from database.database import get_db
from repositories.phase_repository import get_all_phases, get_phase_by_id, add_phase, remove_phase, modify_phase

router = APIRouter(tags=["phases"])


@router.get("/", response_model=list[ReadPhase])
def read_phases(conn=Depends(get_db)):
    return get_all_phases(conn)


@router.get("/{id}", response_model=ReadPhase)
def read_phase(id: Annotated[int, Path(gt=0)], conn=Depends(get_db)):
    try:
        status = get_phase_by_id(id, conn)

        if not status:
            raise HTTPException(status_code=404, detail="Item not found")
        return status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ReadPhase)
def write_phase(status: BasePhase, conn=Depends(get_db)):
    try:
        return add_phase(status, conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
def delete_phase(id: Annotated[int, Path(gt=0)], conn=Depends(get_db)):
    try:
        if not remove_phase(id, conn):
            raise HTTPException(
                status_code=404, detail="Phase not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=ReadPhase)
def update_phase(id: Annotated[int, Path(gt=0)], updated_phase: BasePhaseOptional, conn=Depends(get_db)):
    try:
        updated_phase = modify_phase(id, updated_phase, conn)
        if not updated_phase:
            raise HTTPException(
                status_code=404, detail="Phase not found")
        return updated_phase
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
