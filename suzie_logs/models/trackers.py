from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from .base import LogEntry, TrackerType


class PhysicalTracker(LogEntry):
    tracker_type: TrackerType = TrackerType.PHYSICAL
    
    @classmethod
    def hydration(cls, glasses: int, **kwargs):
        return cls(category="hydration", value=glasses, **kwargs)
    
    @classmethod 
    def digestion(cls, rating: int, symptoms: List[str] = None, **kwargs):
        return cls(category="digestion", value=rating, 
                  tags=symptoms or [], **kwargs)


class MentalTracker(LogEntry):
    tracker_type: TrackerType = TrackerType.MENTAL
    
    @classmethod
    def mood(cls, rating: int, **kwargs):
        return cls(category="mood", value=rating, **kwargs)
    
    @classmethod
    def energy(cls, rating: int, **kwargs):
        return cls(category="energy", value=rating, **kwargs)


class WorkTracker(LogEntry):
    tracker_type: TrackerType = TrackerType.WORK
    
    @classmethod
    def context_switches(cls, count: int, **kwargs):
        return cls(category="context_switches", value=count, **kwargs)
    
    @classmethod
    def focus_session(cls, duration_min: int, quality: int, **kwargs):
        return cls(category="focus", value={
            "duration": duration_min, "quality": quality
        }, **kwargs)