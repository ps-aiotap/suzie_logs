from typing import List, Dict, Any, Optional
from datetime import date, timedelta
from ..models.base import LogEntry
from ..storage import YAMLStore


class RecommendationEngine:
    def __init__(self, store: YAMLStore, llm_client=None):
        self.store = store
        self.llm_client = llm_client  # OpenAI, Bedrock, etc.
    
    def get_recommendations(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Generate recommendations based on recent patterns."""
        recommendations = []
        
        # Rule-based recommendations
        recommendations.extend(self._rule_based_recommendations(days_back))
        
        # LLM-based recommendations (if available)
        if self.llm_client:
            recommendations.extend(self._llm_recommendations(days_back))
        
        return recommendations
    
    def _rule_based_recommendations(self, days_back: int) -> List[Dict[str, Any]]:
        """Simple rule-based recommendations."""
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        entries = self.store.load_entries(start_date, end_date)
        
        recommendations = []
        
        # Hydration check
        hydration_entries = [e for e in entries if e.category == 'hydration']
        if hydration_entries:
            avg_hydration = sum(e.value for e in hydration_entries) / len(hydration_entries)
            if avg_hydration < 6:
                recommendations.append({
                    'type': 'health',
                    'priority': 'medium',
                    'message': 'Consider increasing daily water intake',
                    'data': f'Average: {avg_hydration:.1f} glasses/day'
                })
        
        # Context switching pattern
        cs_entries = [e for e in entries if e.category == 'context_switches']
        if cs_entries:
            avg_switches = sum(e.value for e in cs_entries) / len(cs_entries)
            if avg_switches > 10:
                recommendations.append({
                    'type': 'productivity',
                    'priority': 'high',
                    'message': 'High context switching detected - consider time blocking',
                    'data': f'Average: {avg_switches:.1f} switches/day'
                })
        
        return recommendations
    
    def _llm_recommendations(self, days_back: int) -> List[Dict[str, Any]]:
        """LLM-powered recommendations (placeholder for future implementation)."""
        # This would integrate with OpenAI, Bedrock, etc.
        # For now, return empty list
        return []
    
    def suggest_products(self, category: str) -> List[Dict[str, Any]]:
        """Suggest products based on tracked patterns."""
        # Placeholder for affiliate/ad integration
        suggestions = {
            'hydration': [
                {'name': 'Smart Water Bottle', 'reason': 'Track intake automatically'},
                {'name': 'Electrolyte Supplements', 'reason': 'Improve hydration quality'}
            ],
            'focus': [
                {'name': 'Noise-Canceling Headphones', 'reason': 'Reduce distractions'},
                {'name': 'Pomodoro Timer App', 'reason': 'Structure focus sessions'}
            ]
        }
        
        return suggestions.get(category, [])