"""Markdown and JSON renderer for trend data."""

from typing import Any, Dict, List
from datetime import datetime


class TrendRenderer:
    """Renderer for generating README and JSON outputs."""
    
    def generate_readme(
        self, 
        trending: List[Dict[str, Any]], 
        categories: Dict[str, List[Dict[str, Any]]],
        collected_at: str
    ) -> str:
        """Generate README content with trend data.
        
        Args:
            trending: List of top trending repositories
            categories: Dictionary of categorized repositories
            collected_at: Timestamp of data collection
            
        Returns:
            Markdown formatted README content
        """
        readme = """# OSS Orbit Tracker

> 世界中のOSSトレンドを毎日収集・分析・可視化するオープンデータプロジェクト

[![Daily Update](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/daily-update.yml/badge.svg)](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/daily-update.yml)
[![Quality Check](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/quality-check.yml/badge.svg)](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/quality-check.yml)

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
- [ ] GitHub Pages可視化 (v1.0)

## 🤝 コントリビューション

Issue・PRを歓迎します!

## 📄 ライセンス

MIT License

---

**Made with ❤️ by OSS Community**

🗓 最終更新: {collected_at}
"""
        
        return readme
    
    def generate_json(
        self,
        trending: List[Dict[str, Any]],
        categories: Dict[str, List[Dict[str, Any]]],
        collected_at: str
    ) -> Dict[str, Any]:
        """Generate JSON data structure.
        
        Args:
            trending: List of trending repositories
            categories: Dictionary of categorized repositories
            collected_at: Timestamp of data collection
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            "collected_at": collected_at,
            "trending": trending,
            "categories": categories,
            "total_repos": len(trending),
            "metadata": {
                "version": "0.1.0",
                "source": "GitHub API"
            }
        }
