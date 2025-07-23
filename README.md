# SuzieLogs - Developer Friction Tracker

AI-extendable personal friction tracker for developers. Track hydration, digestion, mood, energy, sleep, and work-related friction (context switching, burnout) using YAML logs with optional AI-powered insights.

## Quick Start

```bash
pip install -e .

# Basic logging
suzie log mood 7
suzie log hydration 8 --notes "felt good today"
suzie log focus "90,8" --tags deep-work --tags morning
suzie log context_switches 12 --notes "slack interruptions"

# View summaries
suzie summary today
suzie summary yesterday
suzie summary 2024-01-15

# AI-powered analysis
suzie query "low energy and high context switches"
suzie analyze --days 14
suzie recommend

# Git integration
suzie commit
```

## Features

- **CLI-first**: Built with Click for developer-friendly interface
- **YAML logs**: Human-readable, git-friendly daily logs
- **Modular tracking**: Physical, mental, work, environmental categories
- **AI integration**: Pattern analysis, correlations, recommendations
- **Git versioning**: Automatic commit of daily logs
- **Extensible**: Plugin architecture for custom trackers and AI models

## Log Categories

### Physical

- `hydration`: Glasses of water (1-12)
- `digestion`: Rating 1-10 with optional symptom tags

### Mental

- `mood`: Rating 1-10
- `energy`: Rating 1-10

### Work

- `context_switches`: Count of interruptions/task switches
- `focus`: Duration (minutes) and quality (1-10): "90,8"

## YAML Log Format

Daily logs are stored in `logs/YYYY-MM-DD.yaml`:

```yaml
- timestamp: '2024-01-15T09:30:00'
  tracker_type: 'mental'
  category: 'energy'
  value: 7
  notes: 'Good start to day'
  tags: ['morning', 'coffee']

- timestamp: '2024-01-15T16:00:00'
  tracker_type: 'work'
  category: 'focus'
  value:
    duration: 90
    quality: 8
  notes: 'Deep work on feature X'
  tags: ['deep-work', 'coding']
```

## AI Features

### Pattern Analysis

```bash
# Find correlations between metrics
suzie analyze --days 30

# Natural language queries
suzie query "gas and low focus last week"
suzie query "high energy morning sessions"
```

### Recommendations

```bash
# Get AI-powered suggestions
suzie recommend
```

Recommendations include:

- Health patterns (hydration, energy)
- Productivity insights (context switching, focus)
- Product suggestions based on tracked friction

## Extending SuzieLogs

### Custom Trackers

Add new tracker types in `suzie_logs/models/trackers.py`:

```python
class EnvironmentalTracker(LogEntry):
    tracker_type: TrackerType = TrackerType.ENVIRONMENTAL

    @classmethod
    def noise_level(cls, rating: int, **kwargs):
        return cls(category="noise", value=rating, **kwargs)
```

### AI Integration

Connect your preferred LLM in `suzie_logs/ai/recommender.py`:

```python
# OpenAI integration
from openai import OpenAI
client = OpenAI(api_key="your-key")
recommender = RecommendationEngine(store, llm_client=client)

# AWS Bedrock integration
from langchain.llms import Bedrock
llm = Bedrock(model_id="anthropic.claude-v2")
recommender = RecommendationEngine(store, llm_client=llm)
```
