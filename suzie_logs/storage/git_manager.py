import git
from pathlib import Path
from datetime import datetime


class GitManager:
    def __init__(self, repo_path: Path = Path(".")):
        self.repo_path = Path(repo_path)
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            self.repo = git.Repo.init(repo_path)
    
    def commit_daily_logs(self, message: str = None):
        """Commit today's logs with auto-generated message."""
        if message is None:
            message = f"Daily logs: {datetime.now().strftime('%Y-%m-%d')}"
        
        # Add logs directory
        self.repo.index.add(["logs/"])
        
        # Commit if there are changes
        if self.repo.index.diff("HEAD"):
            self.repo.index.commit(message)
            return True
        return False
    
    def get_log_history(self, file_pattern: str = "logs/*.yaml"):
        """Get commit history for log files."""
        commits = list(self.repo.iter_commits(paths=file_pattern, max_count=10))
        return [(c.hexsha[:8], c.message.strip(), c.committed_datetime) 
                for c in commits]