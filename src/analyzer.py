"""Data analyzer for processing repository trends.

This module provides analysis functions for ranking and categorizing
GitHub repositories based on various metrics.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Analyzer for processing and ranking repository data.
    
    This class provides methods to extract, rank, and categorize
    repository data for trend analysis.
    """
    
    def extract_repo_data(self, repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relevant data from raw repository responses.
        
        Args:
            repos: List of raw repository data from GitHub API
            
        Returns:
            List of cleaned repository data
            
        Raises:
            ValueError: If repos is empty or invalid
        """
        if not repos:
            logger.warning("Empty repository list provided")
            return []
        
        if not isinstance(repos, list):
            raise ValueError("repos must be a list")
        
        extracted = []
        
        for idx, repo in enumerate(repos):
            try:
                extracted.append({
                    "name": repo.get("full_name", "unknown/unknown"),
                    "description": repo.get("description", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "language": repo.get("language") or "Unknown",
                    "url": repo.get("html_url", ""),
                    "updated_at": repo.get("updated_at", ""),
                    "created_at": repo.get("created_at", ""),
                    "topics": repo.get("topics", []),
                    "open_issues": repo.get("open_issues_count", 0),
                })
            except Exception as e:
                logger.warning(f"Error extracting repo at index {idx}: {e}")
                continue
        
        logger.info(f"Extracted data from {len(extracted)}/{len(repos)} repositories")
        return extracted
    
    def rank_by_stars(
        self, 
        repos: List[Dict[str, Any]], 
        top_n: int = 10
    ) -> List[Dict[str, Any]]:
        """Rank repositories by star count.
        
        Args:
            repos: List of repository data
            top_n: Number of top repositories to return
            
        Returns:
            Top N repositories sorted by stars
            
        Raises:
            ValueError: If top_n is negative or repos is empty
        """
        if not repos:
            logger.warning("Empty repository list provided for ranking")
            return []
        
        if top_n < 0:
            raise ValueError("top_n must be non-negative")
        
        if top_n == 0:
            return []
        
        try:
            sorted_repos = sorted(
                repos, 
                key=lambda x: x.get("stars", 0), 
                reverse=True
            )
            result = sorted_repos[:top_n]
            
            logger.debug(f"Ranked top {len(result)} repositories by stars")
            return result
            
        except Exception as e:
            logger.error(f"Error ranking repositories: {e}")
            return []
    
    def categorize_by_language(
        self, 
        repos: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group repositories by programming language.
        
        Args:
            repos: List of repository data
            
        Returns:
            Dictionary mapping language to list of repositories
        """
        if not repos:
            logger.warning("Empty repository list provided for language categorization")
            return {}
        
        categories: Dict[str, List[Dict[str, Any]]] = {}
        
        for repo in repos:
            try:
                lang = repo.get("language", "Unknown")
                if lang not in categories:
                    categories[lang] = []
                categories[lang].append(repo)
            except Exception as e:
                logger.warning(f"Error categorizing repo by language: {e}")
                continue
        
        logger.info(f"Categorized into {len(categories)} language groups")
        return categories
    
    def categorize_by_topic(
        self, 
        repos: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group repositories by topics/tags.
        
        Uses predefined topic categories to classify repositories
        based on their GitHub topics.
        
        Args:
            repos: List of repository data
            
        Returns:
            Dictionary mapping topic category to list of repositories
        """
        if not repos:
            logger.warning("Empty repository list provided for topic categorization")
            return {}
        
        categories: Dict[str, List[Dict[str, Any]]] = {}
        
        # Define topic categories
        topic_categories = {
            "AI/ML": [
                "machine-learning", "artificial-intelligence", "deep-learning", 
                "llm", "ai", "neural-network", "tensorflow", "pytorch"
            ],
            "Web": [
                "web", "frontend", "backend", "react", "vue", "angular", 
                "nextjs", "svelte", "webdev"
            ],
            "DevOps": [
                "devops", "kubernetes", "docker", "cicd", "infrastructure",
                "terraform", "ansible", "jenkins"
            ],
            "Data": [
                "data-science", "data-engineering", "analytics", "database",
                "big-data", "etl", "sql", "nosql"
            ],
            "Mobile": [
                "mobile", "ios", "android", "flutter", "react-native",
                "swift", "kotlin", "mobile-app"
            ],
        }
        
        for repo in repos:
            try:
                topics = repo.get("topics", [])
                
                if not topics:
                    continue
                
                for category, keywords in topic_categories.items():
                    # Check if any keyword matches any topic
                    if any(keyword in topic.lower() for keyword in keywords for topic in topics):
                        if category not in categories:
                            categories[category] = []
                        # Avoid duplicates
                        if repo not in categories[category]:
                            categories[category].append(repo)
                            
            except Exception as e:
                logger.warning(f"Error categorizing repo by topic: {e}")
                continue
        
        # Sort each category by stars
        for category in categories:
            categories[category] = sorted(
                categories[category],
                key=lambda x: x.get("stars", 0),
                reverse=True
            )
        
        logger.info(f"Categorized into {len(categories)} topic groups")
        for category, category_repos in categories.items():
            logger.debug(f"  - {category}: {len(category_repos)} repositories")
        
        return categories
