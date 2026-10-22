"""Markdown and JSON renderer for trend data.

This module handles the generation of README files and JSON outputs
using Jinja2 templates for better maintainability.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

logger = logging.getLogger(__name__)


class TrendRenderer:
    """Renderer for generating README and JSON outputs."""
    
    def __init__(self, template_dir: str = "templates"):
        """Initialize renderer with template directory.
        
        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = Path(template_dir)
        
        if self.template_dir.exists():
            self.env = Environment(
                loader=FileSystemLoader(str(self.template_dir)),
                trim_blocks=True,
                lstrip_blocks=True
            )
            logger.debug(f"Initialized Jinja2 environment with {template_dir}")
        else:
            self.env = None
            logger.warning(f"Template directory {template_dir} not found, using fallback")
    
    def generate_readme(
        self, 
        trending: List[Dict[str, Any]], 
        categories: Dict[str, List[Dict[str, Any]]],
        collected_at: str,
        hn_stories: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generate README content with trend data.
        
        Args:
            trending: List of top trending repositories
            categories: Dictionary of categorized repositories
            collected_at: Timestamp of data collection
            hn_stories: Optional list of HackerNews stories
            
        Returns:
            Markdown formatted README content
        """
        # Try to use Jinja2 template
        if self.env:
            try:
                template = self.env.get_template("readme_template.md.j2")
                return template.render(
                    trending=trending,
                    categories=categories,
                    collected_at=collected_at,
                    hn_stories=hn_stories or []
                )
            except TemplateNotFound:
                logger.warning("Template not found, using fallback generation")
            except Exception as e:
                logger.error(f"Error rendering template: {e}")
                logger.warning("Using fallback generation")
        
        # Fallback: generate without template
        return self._generate_readme_fallback(trending, categories, collected_at, hn_stories)
    
    def _generate_readme_fallback(
        self,
        trending: List[Dict[str, Any]],
        categories: Dict[str, List[Dict[str, Any]]],
        collected_at: str,
        hn_stories: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Fallback README generation without Jinja2.
        
        Args:
            trending: List of trending repositories
            categories: Categorized repositories
            collected_at: Collection timestamp
            hn_stories: Optional HackerNews stories
            
        Returns:
            Markdown formatted README
        """
        readme = """# OSS Orbit Tracker

> 世界中のOSSトレンドを毎日収集・分析・可視化するオープンデータプロジェクト

[![Daily Update](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/daily-update.yml/badge.svg)](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/daily-update.yml)
[![Quality Check](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/quality-check.yml/badge.svg)](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/quality-check.yml)

## 🎯 プロジェクト概要

GitHub全体の人気OSS・注目プロジェクト・活発リポジトリを**毎日自動で収集・可視化**します。

---

"""
        
        # Add trending section
        readme += f"## 📊 今日のトレンド ({collected_at})\n\n"
        readme += "| Rank | Repository | Stars | Forks | Language | Description |\n"
        readme += "|------|------------|-------|-------|----------|-------------|\n"
        
        for idx, repo in enumerate(trending[:10], 1):
            name = repo['name']
            stars = f"⭐ {repo['stars']:,}"
            forks = f"🍴 {repo['forks']:,}"
            lang = repo['language']
            desc = (repo['description'] or 'No description')[:60] + "..."
            
            readme += f"| {idx} | **[{name}]({repo['url']})** | {stars} | {forks} | {lang} | {desc} |\n"
        
        readme += "\n---\n\n"
        
        # Add HackerNews section if available
        if hn_stories:
            readme += "## 📰 今日のテック記事トレンド (HackerNews)\n\n"
            readme += "| Rank | Title | Score | Comments |\n"
            readme += "|------|-------|-------|----------|\n"
            
            for idx, story in enumerate(hn_stories[:10], 1):
                title = story.get('title', 'No title')
                score = story.get('score', 0)
                comments = story.get('descendants', 0)
                hn_url = story.get('hn_url', '#')
                
                # Truncate title if too long
                if len(title) > 60:
                    title = title[:60] + "..."
                
                readme += f"| {idx} | **[{title}]({hn_url})** | 🔥 {score} | 💬 {comments} |\n"
            
            readme += "\n---\n\n"
        
        # Add category sections
        readme += "## 🏷️ カテゴリ別トレンド\n\n"
        
        for category, repos in list(categories.items())[:5]:  # Top 5 categories
            if repos:
                readme += f"### {category}\n\n"
                for repo in repos[:5]:  # Top 5 in each category
                    readme += f"- **[{repo['name']}]({repo['url']})** ⭐ {repo['stars']:,}\n"
                readme += "\n"
        
        readme += """---

## 🤖 自動化

- **毎日午前9時 (JST)**: トレンドデータを自動収集
- **自動commit**: データ更新とREADME更新
- **Issue作成**: 日次レポートを自動生成

## 📈 ロードマップ

- [x] プロジェクト基盤構築
- [x] GitHub API連携 (v0.1)
- [x] トップ10ランキング (v0.2)
- [x] カテゴリ分類 (v0.3)
- [x] HackerNews連携 (v0.4)
- [ ] GitHub Pages可視化 (v1.0)

## 🤝 コントリビューション

Issue・PRを歓迎します!詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) をご覧ください

---

**Made with ❤️ by OSS Community**

🗓 最終更新: {collected_at}
"""
        
        return readme.format(collected_at=collected_at)
    
    def generate_json(
        self,
        trending: List[Dict[str, Any]],
        categories: Dict[str, List[Dict[str, Any]]],
        collected_at: str,
        hn_stories: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generate JSON data structure.
        
        Args:
            trending: List of trending repositories
            categories: Dictionary of categorized repositories
            collected_at: Timestamp of data collection
            hn_stories: Optional HackerNews stories
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            "collected_at": collected_at,
            "trending": trending,
            "categories": categories,
            "hn_stories": hn_stories or [],
            "total_repos": len(trending),
            "total_hn_stories": len(hn_stories) if hn_stories else 0,
            "metadata": {
                "version": "0.4.0",
                "sources": ["GitHub API", "HackerNews API"] if hn_stories else ["GitHub API"]
            }
        }
