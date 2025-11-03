"""GitHub API Client for fetching repository data.

This module provides a robust client for interacting with GitHub's REST API,
with proper error handling, rate limiting, and logging.
"""

import logging
import os
import time
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import RequestException, Timeout, HTTPError

logger = logging.getLogger(__name__)


class GitHubClient:
    """Client for interacting with GitHub REST API.
    
    Attributes:
        BASE_URL: GitHub API base URL
        token: GitHub Personal Access Token
        session: Requests session with authentication
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client with authentication token.
        
        Args:
            token: GitHub Personal Access Token. If None, reads from GH_TOKEN env var.
            
        Raises:
            ValueError: If token is not provided and GH_TOKEN is not set
        """
        self.token = token or os.getenv("GH_TOKEN")
        if not self.token:
            raise ValueError(
                "GitHub token is required. Set GH_TOKEN environment variable or pass token parameter."
            )
        
        # Mask token in logs
        masked_token = f"{self.token[:8]}{'*' * 20}"
        logger.debug(f"Initialized GitHubClient with token: {masked_token}")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "oss-orbit-tracker/0.3.0"
        })
    
    def get_trending_repositories(
        self, 
        language: Optional[str] = None,
        since: str = "daily",
        limit: int = 100,
        retry_count: int = 3
    ) -> List[Dict[str, Any]]:
        """Fetch trending repositories from GitHub.
        
        Args:
            language: Filter by programming language (optional)
            since: Time period ("daily", "weekly", "monthly")
            limit: Maximum number of repositories to fetch
            retry_count: Number of retries on failure
            
        Returns:
            List of repository data dictionaries
            
        Raises:
            RequestException: If API request fails after all retries
        """
        query = "stars:>100"
        
        if language:
            query += f" language:{language}"
        
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 100)  # API max is 100
        }
        
        url = f"{self.BASE_URL}/search/repositories"
        
        for attempt in range(retry_count):
            try:
                logger.debug(f"Fetching repositories (attempt {attempt + 1}/{retry_count})")
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                items = data.get("items", [])
                
                logger.info(f"Successfully fetched {len(items)} repositories")
                return items
                
            except Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
                    
            except HTTPError as e:
                if e.response.status_code == 403:
                    logger.error("Rate limit exceeded or access forbidden")
                    raise
                elif e.response.status_code == 422:
                    logger.error(f"Invalid query parameters: {params}")
                    raise
                else:
                    logger.warning(f"HTTP error {e.response.status_code} (attempt {attempt + 1}/{retry_count})")
                    if attempt < retry_count - 1:
                        time.sleep(2 ** attempt)
                    else:
                        raise
                        
            except RequestException as e:
                logger.warning(f"Request failed: {e} (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
        
        return []
    
    def get_repository_details(
        self, 
        owner: str, 
        repo: str,
        retry_count: int = 3
    ) -> Dict[str, Any]:
        """Fetch detailed information for a specific repository.
        
        Args:
            owner: Repository owner username
            repo: Repository name
            retry_count: Number of retries on failure
            
        Returns:
            Repository data dictionary
            
        Raises:
            RequestException: If API request fails after all retries
            ValueError: If owner or repo is empty
        """
        if not owner or not repo:
            raise ValueError("Owner and repo must be non-empty strings")
        
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        
        for attempt in range(retry_count):
            try:
                logger.debug(f"Fetching details for {owner}/{repo}")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                logger.debug(f"Successfully fetched details for {owner}/{repo}")
                return data
                
            except Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
                    
            except HTTPError as e:
                if e.response.status_code == 404:
                    logger.error(f"Repository {owner}/{repo} not found")
                    raise
                else:
                    logger.warning(f"HTTP error {e.response.status_code} (attempt {attempt + 1}/{retry_count})")
                    if attempt < retry_count - 1:
                        time.sleep(2 ** attempt)
                    else:
                        raise
                        
            except RequestException as e:
                logger.warning(f"Request failed: {e} (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
        
        return {}
    
    def check_rate_limit(self) -> Dict[str, Any]:
        """Check current API rate limit status.
        
        Returns:
            Rate limit information including remaining requests and reset time
            
        Raises:
            RequestException: If rate limit check fails
        """
        url = f"{self.BASE_URL}/rate_limit"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Log rate limit info
            core = data.get("rate", {})
            remaining = core.get("remaining", 0)
            limit = core.get("limit", 0)
            reset_time = core.get("reset", 0)
            
            logger.debug(f"Rate limit: {remaining}/{limit} (resets at {reset_time})")
            
            return data
            
        except RequestException as e:
            logger.error(f"Failed to check rate limit: {e}")
            raise
