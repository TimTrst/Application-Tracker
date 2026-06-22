from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from models.application import ReadApplication, WriteApplication, UpdateApplication
from database.database import get_db
from repositories.application_repository import get_all_applications, get_application_by_id, add_application, remove_application, modify_application

router = APIRouter(tags=["applications"])


@router.get("/", response_model=list[ReadApplication])
def read_applications(conn=Depends(get_db)):
    return get_all_applications(conn)


@router.get("/{id}", response_model=ReadApplication)
def read_application(id: Annotated[int, Path(gt=0)], conn=Depends(get_db)):
    try:
        application = get_application_by_id(id, conn)

        if not application:
            raise HTTPException(status_code=404, detail="Item not found")
        return application
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ReadApplication)
def write_application(application: WriteApplication, conn=Depends(get_db)):
    try:
        return add_application(application, conn)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
def delete_application(id: Annotated[int, Path(gt=0)], conn=Depends(get_db)):
    try:
        if not remove_application(id, conn):
            raise HTTPException(
                status_code=404, detail="Application not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{id}", response_model=ReadApplication)
def update_application(id: Annotated[int, Path(gt=0)], updated_application: UpdateApplication, conn=Depends(get_db)):
    print(id, updated_application)
    try:
        updated_application = modify_application(id, updated_application, conn)
        if not updated_application:
            raise HTTPException(
                status_code=404, detail="Application not found")
        return updated_application
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
