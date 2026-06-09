from pydantic import BaseModel
from models.status import ReadStatus
from datetime import datetime


class BaseApplication(BaseModel):
    company_name: str
    job_title: str
    url: str | None = None
    date_appointment: datetime | None = None


class ReadApplication(BaseApplication):
    id: int
    status: ReadStatus
    date_added: datetime


class WriteApplication(BaseApplication):
    status_id: int


class BaseApplicationOptional(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    url: str | None = None
    date_appointment: datetime | None = None

class UpdateApplication(BaseApplicationOptional):
    status_id: int | None = None

    

