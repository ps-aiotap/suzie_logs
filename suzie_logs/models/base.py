from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Union
from pydantic import BaseModel, Field


class TrackerType(str, Enum):
    PHYSICAL = "physical"
    MENTAL = "mental" 
    WORK = "work"
    ENVIRONMENTAL = "environmental"


class LogEntry(BaseModel):
    """Base model for all log entries."""
    timestamp: datetime = Field(default_factory=datetime.now)
    tracker_type: TrackerType
    category: str
    value: Union[int, float, str, Dict[str, Any]]
    notes: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }