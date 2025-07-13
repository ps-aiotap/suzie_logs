import click
from datetime import date, datetime
from rich.console import Console
from rich.table import Table
from ..storage import YAMLStore, GitManager
from ..models import PhysicalTracker, MentalTracker, WorkTracker
from ..ai import PatternAnalyzer, RecommendationEngine

console = Console()
store = YAMLStore()
git_mgr = GitManager()
analyzer = PatternAnalyzer(store)
recommender = RecommendationEngine(store)


@click.group()
def cli():
    """SuzieLogs - Developer friction tracker with AI augmentation."""
    pass


@cli.command()
@click.argument('category')
@click.argument('value')
@click.option('--notes', '-n', help='Additional notes')
@click.option('--tags', '-t', multiple=True, help='Tags for categorization')
def log(category, value, notes, tags):
    """Log an entry. Examples:
    
    suzie log mood 7
    suzie log hydration 8 --notes "felt good today"
    suzie log focus "45,8" --tags deep-work --tags morning
    """
    # Parse value based on category
    if category in ['mood', 'energy', 'hydration', 'digestion']:
        entry = _create_physical_mental_entry(category, int(value), notes, tags)
    elif category == 'focus':
        duration, quality = map(int, value.split(','))
        entry = WorkTracker.focus_session(duration, quality, notes=notes, tags=list(tags))
    elif category == 'context_switches':
        entry = WorkTracker.context_switches(int(value), notes=notes, tags=list(tags))
    else:
        click.echo(f"Unknown category: {category}")
        return
    
    store.save_entry(entry)
    console.print(f"✓ Logged {category}: {value}", style="green")


@cli.command()
@click.option('--date', '-d', default='today', help='Date to summarize (today, yesterday, YYYY-MM-DD)')
def summary(date_str):
    """Show summary for a specific date."""
    target_date = _parse_date(date_str)
    entries = store.load_entries(target_date)
    
    if not entries:
        console.print(f"No entries found for {target_date}", style="yellow")
        return
    
    table = Table(title=f"Summary for {target_date}")
    table.add_column("Time", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Value", style="green")
    table.add_column("Notes", style="dim")
    
    for entry in entries:
        table.add_row(
            entry.timestamp.strftime("%H:%M"),
            entry.category,
            str(entry.value),
            entry.notes or ""
        )
    
    console.print(table)


@cli.command()
@click.option('--auto-commit/--no-auto-commit', default=True)
def commit(auto_commit):
    """Commit today's logs to git."""
    if git_mgr.commit_daily_logs():
        console.print("✓ Committed daily logs", style="green")
    else:
        console.print("No changes to commit", style="yellow")


@cli.command()
@click.argument('query')
def query(query):
    """Query patterns: 'gas and low focus last week'"""
    results = analyzer.query_patterns(query)
    
    if not results:
        console.print(f"No matches found for: {query}", style="yellow")
        return
    
    table = Table(title=f"Query Results: {query}")
    table.add_column("Date", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Value", style="green")
    table.add_column("Notes", style="dim")
    
    for entry in results:
        table.add_row(
            entry.timestamp.strftime("%m-%d %H:%M"),
            entry.category,
            str(entry.value),
            entry.notes or ""
        )
    
    console.print(table)


@cli.command()
@click.option('--days', '-d', default=7, help='Days to analyze')
def analyze(days):
    """Analyze patterns and correlations."""
    correlations = analyzer.find_correlations(days)
    
    if not correlations:
        console.print("No significant correlations found", style="yellow")
        return
    
    console.print(f"\n[bold]Pattern Analysis ({days} days)[/bold]")
    for pattern, data in correlations.items():
        console.print(f"\n• {pattern.replace('_vs_', ' vs ')}: {len(data)} overlapping days")


@cli.command()
def recommend():
    """Get AI-powered recommendations."""
    recommendations = recommender.get_recommendations()
    
    if not recommendations:
        console.print("No recommendations at this time", style="yellow")
        return
    
    console.print("\n[bold]Recommendations[/bold]")
    for rec in recommendations:
        priority_color = {"high": "red", "medium": "yellow", "low": "green"}
        color = priority_color.get(rec['priority'], 'white')
        console.print(f"\n[{color}]• {rec['message']}[/{color}]")
        if 'data' in rec:
            console.print(f"  Data: {rec['data']}", style="dim")


def _create_physical_mental_entry(category, value, notes, tags):
    if category in ['hydration', 'digestion']:
        return PhysicalTracker(category=category, value=value, notes=notes, tags=list(tags))
    else:
        return MentalTracker(category=category, value=value, notes=notes, tags=list(tags))


def _parse_date(date_str):
    if date_str == 'today':
        return date.today()
    elif date_str == 'yesterday':
        return date.today().replace(day=date.today().day - 1)
    else:
        return datetime.strptime(date_str, '%Y-%m-%d').date()


if __name__ == '__main__':
    cli()