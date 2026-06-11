from typing import Annotated
from pydantic import BaseModel, AfterValidator
from models.helper import must_not_be_empty, must_be_positive


class BasePhase(BaseModel):
    name: Annotated[str, AfterValidator(must_not_be_empty)]


class ReadPhase(BasePhase):
    id: int


class BasePhaseOptional(BaseModel):
    name: Annotated[str | None, AfterValidator(must_not_be_empty)]
