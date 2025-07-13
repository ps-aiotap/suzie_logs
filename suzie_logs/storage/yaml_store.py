import yaml
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any
from ..models.base import LogEntry


class YAMLStore:
    def __init__(self, logs_dir: Path = Path("logs")):
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(exist_ok=True)
    
    def save_entry(self, entry: LogEntry):
        """Save entry to daily YAML file."""
        day_file = self._get_day_file(entry.timestamp.date())
        
        # Load existing entries
        entries = self._load_day_entries(day_file)
        entries.append(entry.dict())
        
        # Save back
        with open(day_file, 'w') as f:
            yaml.dump(entries, f, default_flow_style=False, sort_keys=False)
    
    def load_entries(self, start_date: date, end_date: date = None) -> List[LogEntry]:
        """Load entries for date range."""
        if end_date is None:
            end_date = start_date
            
        entries = []
        current = start_date
        while current <= end_date:
            day_file = self._get_day_file(current)
            if day_file.exists():
                day_entries = self._load_day_entries(day_file)
                entries.extend([LogEntry(**e) for e in day_entries])
            current = current.replace(day=current.day + 1)
        
        return sorted(entries, key=lambda x: x.timestamp)
    
    def _get_day_file(self, day: date) -> Path:
        return self.logs_dir / f"{day.isoformat()}.yaml"
    
    def _load_day_entries(self, file_path: Path) -> List[Dict[str, Any]]:
        if not file_path.exists():
            return []
        with open(file_path) as f:
            return yaml.safe_load(f) or []