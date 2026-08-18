from pydantic import BaseModel
from datetime import datetime


class BaseApplicationHistoryLog(BaseModel):
    application_id: int
    phase_id: int
    status_id: int


class ReadApplicationHistoryLog(BaseApplicationHistoryLog):
    occurred_at: datetime
    id: int


class ReadApplicationHistoryTransition(BaseModel):
    application_id: int
    from_phase_id: int | None
    from_status_id: int | None
    to_phase_id: int
    to_status_id: int
    occurred_at: datetime
