from pydantic import BaseModel
from datetime import datetime


class BaseApplicationHistoryLog(BaseModel):
    application_id: int
    phase_id: int
    status_id: int


class ReadApplicationHistoryLog(BaseApplicationHistoryLog):
    occurred_at: datetime
    id: int
