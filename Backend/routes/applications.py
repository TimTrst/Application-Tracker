from fastapi import APIRouter, Depends
from models.application import ReadApplication
from database.database import get_db
from repositories.application_repository import get_all_applications

router = APIRouter(tags=["applications"])

@router.get("/", response_model=list[ReadApplication])
def read_applications(conn = Depends(get_db)):
    return get_all_applications(conn)