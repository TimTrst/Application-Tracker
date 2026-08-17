from typing import Annotated
from pydantic import BaseModel, AfterValidator, HttpUrl, BeforeValidator
from models.status import ReadStatus
from datetime import datetime
from models.helper import must_not_be_empty, must_be_positive, empty_str_to_none

# These models are shared by both injectables routes can depend on:
# - ApplicationRepository (repositories/interfaces/application_repository.py):
#   plain CRUD against the applications table only. Inject this directly
#   for reads/deletes that have no side effects on other tables.
# - ApplicationService (services/application_service.py): wraps an
#   ApplicationRepository *and* an ApplicationHistoryLogRepository so that
#   creating an application or changing its status also writes a history
#   log entry. Inject this instead of the repository for any write where a
#   status/phase change must be tracked (see routes/applications.py POST/PATCH).


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
