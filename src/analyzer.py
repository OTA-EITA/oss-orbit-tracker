"""Data analyzer for processing repository trends."""

from typing import Any, Dict, List
from datetime import datetime


class TrendAnalyzer:
    """Analyzer for processing and ranking repository data."""
    
    def extract_repo_data(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relevant data from raw repository responses.
        
        Args:
            repos: List of raw repository data from GitHub API
            
        Returns:
            List of cleaned repository data
        """
        extracted = []
        
        for repo in repos:
            extracted.append({
                "name": repo.get("full_name", ""),
                "description": repo.get("description", ""),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language", "Unknown"),
                "url": repo.get("html_url", ""),
                "updated_at": repo.get("updated_at", ""),
                "created_at": repo.get("created_at", ""),
                "topics": repo.get("topics", []),
                "open_issues": repo.get("open_issues_count", 0),
            })
        
        return extracted
    
    def rank_by_stars(self, repos: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """Rank repositories by star count.
        
        Args:
            repos: List of repository data
            top_n: Number of top repositories to return
            
        Returns:
            Top N repositories sorted by stars
        """
        sorted_repos = sorted(repos, key=lambda x: x["stars"], reverse=True)
        return sorted_repos[:top_n]
    
    def categorize_by_language(self, repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group repositories by programming language.
        
        Args:
            repos: List of repository data
            
        Returns:
            Dictionary mapping language to list of repositories
        """
        categories: Dict[str, List[Dict[str, Any]]] = {}
        
        for repo in repos:
            lang = repo.get("language", "Unknown")
            if lang not in categories:
                categories[lang] = []
            categories[lang].append(repo)
        
        return categories
    
    def categorize_by_topic(self, repos: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group repositories by topics/tags.
        
        Args:
            repos: List of repository data
            
        Returns:
            Dictionary mapping topic to list of repositories
        """
        categories: Dict[str, List[Dict[str, Any]]] = {}
        
        # Define topic categories
        topic_categories = {
            "AI/ML": ["machine-learning", "artificial-intelligence", "deep-learning", "llm", "ai"],
            "Web": ["web", "frontend", "backend", "react", "vue", "angular", "nextjs"],
            "DevOps": ["devops", "kubernetes", "docker", "cicd", "infrastructure"],
            "Data": ["data-science", "data-engineering", "analytics", "database"],
            "Mobile": ["mobile", "ios", "android", "flutter", "react-native"],
        }
        
        for repo in repos:
            topics = repo.get("topics", [])
            
            for category, keywords in topic_categories.items():
                if any(keyword in topics for keyword in keywords):
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(repo)
        
        return categories
