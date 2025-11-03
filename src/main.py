"""Main entry point for OSS Orbit Tracker.

This module orchestrates the entire data collection, analysis,
and output generation pipeline.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from github_client import GitHubClient
from hn_client import HackerNewsClient
from analyzer import TrendAnalyzer
from renderer import TrendRenderer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main() -> int:
    """Main execution function.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    logger.info("🚀 Starting OSS Orbit Tracker...")
    
    # Initialize components
    try:
        github_client = GitHubClient()
        logger.info("✅ GitHub client initialized")
    except ValueError as e:
        logger.error(f"❌ Failed to initialize GitHub client: {e}")
        logger.error("Please set GH_TOKEN environment variable")
        return 1
    except Exception as e:
        logger.error(f"❌ Unexpected error during initialization: {e}")
        return 1
    
    # Initialize HackerNews client
    try:
        hn_client = HackerNewsClient()
        logger.info("✅ HackerNews client initialized")
    except Exception as e:
        logger.warning(f"⚠️  HackerNews client initialization failed: {e}")
        hn_client = None
    
    analyzer = TrendAnalyzer()
    renderer = TrendRenderer()
    
    # Check rate limit
    try:
        rate_limit = github_client.check_rate_limit()
        remaining = rate_limit['rate']['remaining']
        total = rate_limit['rate']['limit']
        logger.info(f"📊 GitHub API Rate Limit: {remaining}/{total} requests remaining")
        
        if remaining < 10:
            logger.warning("⚠️  Warning: Low rate limit remaining")
            logger.warning("Consider waiting or using a different token")
    except Exception as e:
        logger.warning(f"⚠️  Could not check rate limit: {e}")
        logger.warning("Proceeding anyway...")
    
    # Fetch trending repositories from GitHub
    logger.info("📡 Fetching trending GitHub repositories...")
    try:
        raw_repos = github_client.get_trending_repositories(limit=100)
        logger.info(f"✅ Fetched {len(raw_repos)} repositories")
    except Exception as e:
        logger.error(f"❌ Error fetching repositories: {e}")
        return 1
    
    # Validate data
    if not raw_repos:
        logger.error("❌ No repositories fetched")
        return 1
    
    # Extract and analyze GitHub data
    logger.info("🔍 Analyzing GitHub data...")
    try:
        repos = analyzer.extract_repo_data(raw_repos)
        trending = analyzer.rank_by_stars(repos, top_n=50)
        categories = analyzer.categorize_by_topic(repos)
        
        logger.info(f"✅ Analyzed {len(repos)} repositories")
        logger.info(f"📊 Found {len(categories)} categories")
        
        # Log category distribution
        for category, category_repos in categories.items():
            logger.debug(f"  - {category}: {len(category_repos)} repos")
            
    except Exception as e:
        logger.error(f"❌ Error during analysis: {e}")
        return 1
    
    # Fetch HackerNews stories
    hn_stories = []
    if hn_client:
        logger.info("📰 Fetching trending HackerNews stories...")
        try:
            raw_stories = hn_client.get_trending_stories(limit=10, min_score=100)
            hn_stories = hn_client.extract_story_data(raw_stories)
            logger.info(f"✅ Fetched {len(hn_stories)} HackerNews stories")
        except Exception as e:
            logger.warning(f"⚠️  Error fetching HackerNews stories: {e}")
            logger.warning("Continuing without HackerNews data...")
    
    # Generate outputs
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    logger.info("📝 Generating outputs...")
    
    # Generate README
    try:
        readme_content = renderer.generate_readme(
            trending, 
            categories, 
            collected_at,
            hn_stories=hn_stories
        )
        readme_path = Path("README.md")
        readme_path.write_text(readme_content, encoding="utf-8")
        logger.info(f"✅ Updated {readme_path}")
    except Exception as e:
        logger.error(f"❌ Error generating README: {e}")
        return 1
    
    # Generate JSON
    try:
        json_data = renderer.generate_json(
            trending, 
            categories, 
            collected_at,
            hn_stories=hn_stories
        )
        
        # Save daily JSON
        json_path = Path(f"data/{date_str}.json")
        json_path.parent.mkdir(exist_ok=True)
        json_path.write_text(
            json.dumps(json_data, indent=2, ensure_ascii=False), 
            encoding="utf-8"
        )
        logger.info(f"✅ Saved data to {json_path}")
        
        # Save latest.json for easy access
        latest_path = Path("data/latest.json")
        latest_path.write_text(
            json.dumps(json_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        logger.info(f"✅ Updated {latest_path}")
        
    except Exception as e:
        logger.error(f"❌ Error generating JSON: {e}")
        return 1
    
    logger.info("🎉 OSS Orbit Tracker completed successfully!")
    logger.info(f"📊 Summary: {len(trending)} GitHub repos, {len(hn_stories)} HN stories, {len(categories)} categories")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
