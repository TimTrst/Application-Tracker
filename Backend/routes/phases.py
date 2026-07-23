from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from models.phase import ReadPhase, BasePhaseOptional, BasePhase
from repositories.interfaces.phase_repository import PhaseRepository
from repositories.dependencies import get_phase_repository

router = APIRouter(tags=["phases"])


@router.get("/", response_model=list[ReadPhase])
def read_phases(repo: PhaseRepository = Depends(get_phase_repository)):
    return repo.get_all()


@router.get("/{id}", response_model=ReadPhase)
def read_phase(
    id: Annotated[int, Path(gt=0)],
    repo: PhaseRepository = Depends(get_phase_repository),
):
    try:
        phase = repo.get_by_id(id)

        if not phase:
            raise HTTPException(status_code=404, detail="Item not found")
        return phase
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ReadPhase)
def write_phase(
    phase: BasePhase, repo: PhaseRepository = Depends(get_phase_repository)
):
    try:
        return repo.add(phase)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
def delete_phase(
    id: Annotated[int, Path(gt=0)],
    repo: PhaseRepository = Depends(get_phase_repository),
):
    try:
        if not repo.remove(id):
            raise HTTPException(status_code=404, detail="Phase not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=ReadPhase)
def update_phase(
    id: Annotated[int, Path(gt=0)],
    updated_phase: BasePhaseOptional,
    repo: PhaseRepository = Depends(get_phase_repository),
):
    try:
        updated_phase = repo.modify(id, updated_phase)
        if not updated_phase:
            raise HTTPException(status_code=404, detail="Phase not found")
        return updated_phase
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
