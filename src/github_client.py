"""GitHub API Client for fetching repository data."""

import os
from typing import Any, Dict, List, Optional
import requests


class GitHubClient:
    """Client for interacting with GitHub REST API."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client with authentication token.
        
        Args:
            token: GitHub Personal Access Token. If None, reads from GH_TOKEN env var.
        """
        self.token = token or os.getenv("GH_TOKEN")
        if not self.token:
            raise ValueError("GitHub token is required. Set GH_TOKEN environment variable.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "oss-orbit-tracker"
        })
    
    def get_trending_repositories(
        self, 
        language: Optional[str] = None,
        since: str = "daily",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch trending repositories from GitHub.
        
        Args:
            language: Filter by programming language (optional)
            since: Time period ("daily", "weekly", "monthly")
            limit: Maximum number of repositories to fetch
            
        Returns:
            List of repository data dictionaries
        """
        # GitHub doesn't have official trending API, so we use search API
        # with stars created in the last day as a proxy
        query = "stars:>100"
        
        if language:
            query += f" language:{language}"
        
        # Sort by stars to get trending repos
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 100)  # API max is 100
        }
        
        url = f"{self.BASE_URL}/search/repositories"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("items", [])
    
    def get_repository_details(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch detailed information for a specific repository.
        
        Args:
            owner: Repository owner username
            repo: Repository name
            
        Returns:
            Repository data dictionary
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def check_rate_limit(self) -> Dict[str, Any]:
        """Check current API rate limit status.
        
        Returns:
            Rate limit information
        """
        url = f"{self.BASE_URL}/rate_limit"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
