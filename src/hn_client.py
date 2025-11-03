"""HackerNews API Client for fetching trending stories.

This module provides a client for interacting with the HackerNews API
to fetch trending tech stories and discussions.
"""

import logging
import time
from typing import Any, Dict, List, Optional

import requests
from requests.exceptions import RequestException, Timeout, HTTPError

logger = logging.getLogger(__name__)


class HackerNewsClient:
    """Client for interacting with HackerNews API.
    
    Attributes:
        BASE_URL: HackerNews API base URL
        session: Requests session
    """
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self):
        """Initialize HackerNews client."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "oss-orbit-tracker/0.4.0"
        })
        logger.debug("Initialized HackerNewsClient")
    
    def get_top_stories(
        self, 
        limit: int = 30,
        retry_count: int = 3
    ) -> List[int]:
        """Fetch top story IDs from HackerNews.
        
        Args:
            limit: Maximum number of story IDs to fetch
            retry_count: Number of retries on failure
            
        Returns:
            List of story IDs
            
        Raises:
            RequestException: If API request fails after all retries
        """
        url = f"{self.BASE_URL}/topstories.json"
        
        for attempt in range(retry_count):
            try:
                logger.debug(f"Fetching top stories (attempt {attempt + 1}/{retry_count})")
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                story_ids = response.json()
                limited_ids = story_ids[:limit]
                
                logger.info(f"Successfully fetched {len(limited_ids)} story IDs")
                return limited_ids
                
            except Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
                    
            except HTTPError as e:
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
    
    def get_story_details(
        self, 
        story_id: int,
        retry_count: int = 3
    ) -> Optional[Dict[str, Any]]:
        """Fetch details for a specific story.
        
        Args:
            story_id: HackerNews story ID
            retry_count: Number of retries on failure
            
        Returns:
            Story data dictionary or None if failed
        """
        url = f"{self.BASE_URL}/item/{story_id}.json"
        
        for attempt in range(retry_count):
            try:
                response = self.session.get(url, timeout=5)
                response.raise_for_status()
                
                story = response.json()
                
                # Validate story data
                if not story or story.get("type") not in ["story", "link"]:
                    logger.debug(f"Story {story_id} is not a valid story type")
                    return None
                
                logger.debug(f"Successfully fetched story {story_id}")
                return story
                
            except Timeout:
                logger.warning(f"Timeout fetching story {story_id} (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(1)
                else:
                    return None
                    
            except HTTPError as e:
                if e.response.status_code == 404:
                    logger.debug(f"Story {story_id} not found")
                    return None
                logger.warning(f"HTTP error for story {story_id} (attempt {attempt + 1}/{retry_count})")
                if attempt < retry_count - 1:
                    time.sleep(1)
                else:
                    return None
                    
            except RequestException as e:
                logger.warning(f"Error fetching story {story_id}: {e}")
                if attempt < retry_count - 1:
                    time.sleep(1)
                else:
                    return None
        
        return None
    
    def get_trending_stories(
        self, 
        limit: int = 10,
        min_score: int = 50
    ) -> List[Dict[str, Any]]:
        """Fetch trending stories with details.
        
        Args:
            limit: Maximum number of stories to return
            min_score: Minimum score (points) for a story to be included
            
        Returns:
            List of story data dictionaries
        """
        logger.info(f"Fetching top {limit} trending stories (min_score: {min_score})")
        
        try:
            # Get top story IDs
            story_ids = self.get_top_stories(limit=limit * 3)  # Fetch more to filter by score
            
            if not story_ids:
                logger.warning("No story IDs fetched")
                return []
            
            # Fetch details for each story
            stories = []
            for story_id in story_ids:
                if len(stories) >= limit:
                    break
                
                story = self.get_story_details(story_id)
                
                if story:
                    # Filter by score
                    score = story.get("score", 0)
                    if score >= min_score:
                        stories.append(story)
                        logger.debug(f"Added story: {story.get('title', 'N/A')} (score: {score})")
                
                # Rate limiting - be nice to HN API
                time.sleep(0.1)
            
            logger.info(f"Successfully fetched {len(stories)} trending stories")
            return stories
            
        except Exception as e:
            logger.error(f"Error fetching trending stories: {e}")
            return []
    
    def extract_story_data(self, stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relevant data from raw story responses.
        
        Args:
            stories: List of raw story data from HackerNews API
            
        Returns:
            List of cleaned story data
        """
        if not stories:
            logger.warning("Empty story list provided")
            return []
        
        extracted = []
        
        for story in stories:
            try:
                extracted.append({
                    "id": story.get("id"),
                    "title": story.get("title", "No title"),
                    "url": story.get("url", f"https://news.ycombinator.com/item?id={story.get('id')}"),
                    "score": story.get("score", 0),
                    "author": story.get("by", "unknown"),
                    "time": story.get("time", 0),
                    "descendants": story.get("descendants", 0),  # comment count
                    "type": story.get("type", "story"),
                    "hn_url": f"https://news.ycombinator.com/item?id={story.get('id')}",
                })
            except Exception as e:
                logger.warning(f"Error extracting story data: {e}")
                continue
        
        logger.info(f"Extracted data from {len(extracted)}/{len(stories)} stories")
        return extracted
