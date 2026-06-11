from typing import Annotated
from pydantic import BaseModel, AfterValidator
from models.phase import ReadPhase
from models.helper import must_not_be_empty, must_be_positive


class BaseStatus(BaseModel):
    name: Annotated[str, AfterValidator(must_not_be_empty)]


class WriteStatus(BaseStatus):
    phase_id: Annotated[int, AfterValidator(must_be_positive)]


class ReadStatus(BaseStatus):
    id: int
    phase: ReadPhase


class BaseStatusOptional(BaseModel):
    name: Annotated[str | None, AfterValidator(must_not_be_empty)]


class UpdateStatus(BaseStatusOptional):
    phase_id: Annotated[int | None, AfterValidator(must_be_positive)]
