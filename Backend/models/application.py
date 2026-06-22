from typing import Annotated
from pydantic import BaseModel, AfterValidator, HttpUrl, BeforeValidator
from models.status import ReadStatus
from datetime import datetime
from models.helper import must_not_be_empty, must_be_positive, empty_str_to_none


class BaseApplication(BaseModel):
    company_name: Annotated[str, AfterValidator(must_not_be_empty)]
    job_title: Annotated[str, AfterValidator(must_not_be_empty)]
    url: Annotated[HttpUrl | None, BeforeValidator(empty_str_to_none)]
    date_appointment: Annotated[datetime | None,
                                BeforeValidator(empty_str_to_none)]


class ReadApplication(BaseApplication):
    id: int
    status: ReadStatus
    date_added: datetime


class WriteApplication(BaseApplication):
    status_id: Annotated[int, AfterValidator(must_be_positive)]


class BaseApplicationOptional(BaseModel):
    company_name: Annotated[str | None, AfterValidator(must_not_be_empty)]
    job_title: Annotated[str | None, AfterValidator(must_not_be_empty)]
    url: Annotated[HttpUrl | None, BeforeValidator(empty_str_to_none)]
    date_appointment: datetime | None = None


class UpdateApplication(BaseApplicationOptional):
    status_id: Annotated[int | None, AfterValidator(must_be_positive)]
