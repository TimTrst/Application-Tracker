from pydantic import BaseModel


class BasePhase(BaseModel):
    name: str

class ReadPhase(BasePhase):
    id: int