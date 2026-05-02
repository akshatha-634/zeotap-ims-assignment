from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Signal(BaseModel):
    component_id: str
    error_type: str
    severity: str  # P0, P1, P2
    message: str
    timestamp: Optional[datetime] = None

class WorkItem(BaseModel):
    component_id: str
    status: str = "OPEN"  # OPEN -> INVESTIGATING -> RESOLVED -> CLOSED
    signal_count: int = 1
    created_at: Optional[datetime] = None
    rca: Optional[dict] = None
