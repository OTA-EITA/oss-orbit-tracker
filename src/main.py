"""Main entry point for OSS Orbit Tracker."""

import os
import json
from datetime import datetime
from pathlib import Path

from github_client import GitHubClient
from analyzer import TrendAnalyzer
from renderer import TrendRenderer


def main():
    """Main execution function."""
    print("🚀 Starting OSS Orbit Tracker...")
    
    # Initialize components
    try:
        client = GitHubClient()
        print("✅ GitHub client initialized")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set GH_TOKEN environment variable")
        return 1
    
    analyzer = TrendAnalyzer()
    renderer = TrendRenderer()
    
    # Check rate limit
    rate_limit = client.check_rate_limit()
    remaining = rate_limit['rate']['remaining']
    print(f"📊 API Rate Limit: {remaining} requests remaining")
    
    if remaining < 10:
        print("⚠️  Warning: Low rate limit remaining")
    
    # Fetch trending repositories
    print("📡 Fetching trending repositories...")
    try:
        raw_repos = client.get_trending_repositories(limit=100)
        print(f"✅ Fetched {len(raw_repos)} repositories")
    except Exception as e:
        print(f"❌ Error fetching repositories: {e}")
        return 1
    
    # Extract and analyze data
    print("🔍 Analyzing data...")
    repos = analyzer.extract_repo_data(raw_repos)
    trending = analyzer.rank_by_stars(repos, top_n=50)
    categories = analyzer.categorize_by_topic(repos)
    
    print(f"✅ Analyzed {len(repos)} repositories")
    print(f"📊 Found {len(categories)} categories")
    
    # Generate outputs
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    print("📝 Generating outputs...")
    
    # Generate README
    readme_content = renderer.generate_readme(trending, categories, collected_at)
    readme_path = Path("README.md")
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"✅ Updated {readme_path}")
    
    # Generate JSON
    json_data = renderer.generate_json(trending, categories, collected_at)
    json_path = Path(f"data/{date_str}.json")
    json_path.parent.mkdir(exist_ok=True)
    json_path.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Saved data to {json_path}")
    
    print("🎉 OSS Orbit Tracker completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())
