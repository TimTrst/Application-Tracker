from pydantic import BaseModel
from models.phase import BasePhase


class BaseStatus(BaseModel):
    name: str


class WriteStatus(BaseStatus):
    phase_id: int


class ReadStatus(BaseStatus):
    id: int
    phase: BasePhase