from datetime import date, timedelta
from typing import List, Dict, Any
from collections import defaultdict
from ..models.base import LogEntry
from ..storage import YAMLStore


class PatternAnalyzer:
    def __init__(self, store: YAMLStore):
        self.store = store
    
    def find_correlations(self, days_back: int = 7) -> Dict[str, Any]:
        """Find correlations between different tracked metrics."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        entries = self.store.load_entries(start_date, end_date)
        
        # Group by day and category
        daily_data = defaultdict(lambda: defaultdict(list))
        for entry in entries:
            day = entry.timestamp.date()
            daily_data[day][entry.category].append(entry.value)
        
        # Simple correlation analysis
        correlations = {}
        categories = set()
        for day_data in daily_data.values():
            categories.update(day_data.keys())
        
        # Find days where multiple categories overlap
        for cat1 in categories:
            for cat2 in categories:
                if cat1 != cat2:
                    overlap_days = []
                    for day, day_data in daily_data.items():
                        if cat1 in day_data and cat2 in day_data:
                            overlap_days.append((day, day_data[cat1], day_data[cat2]))
                    
                    if len(overlap_days) >= 3:  # Minimum data points
                        correlations[f"{cat1}_vs_{cat2}"] = overlap_days
        
        return correlations
    
    def query_patterns(self, query: str) -> List[LogEntry]:
        """Natural language-ish queries like 'gas and low focus last week'."""
        # Simple keyword matching - could be enhanced with LLM
        keywords = query.lower().split()
        
        # Date parsing
        days_back = 7
        if 'yesterday' in keywords:
            days_back = 1
        elif 'week' in keywords:
            days_back = 7
        elif 'month' in keywords:
            days_back = 30
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        entries = self.store.load_entries(start_date, end_date)
        
        # Filter by keywords
        matching_entries = []
        for entry in entries:
            entry_text = f"{entry.category} {entry.notes or ''} {' '.join(entry.tags)}".lower()
            if any(keyword in entry_text for keyword in keywords):
                matching_entries.append(entry)
        
        return matching_entries