# 🏗️ OSS Orbit Tracker: アーキテクチャ設計

> システム全体の構成と各コンポーネントの責務を定義します。

---

## 📐 システム構成図

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                           │
│                  (daily-update.yml)                          │
│                                                               │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐          │
│  │ Schedule │─────▶│ main.py  │─────▶│ Renderer │          │
│  │  (cron)  │      │          │      │          │          │
│  └──────────┘      └────┬─────┘      └────┬─────┘          │
│                          │                  │                │
│                          ▼                  ▼                │
│                    ┌──────────┐      ┌──────────┐          │
│                    │ Clients  │      │  Output  │          │
│                    │  Layer   │      │  Layer   │          │
│                    └────┬─────┘      └────┬─────┘          │
└─────────────────────────┼───────────────────┼───────────────┘
                          │                   │
                          ▼                   ▼
                    ┌──────────┐      ┌──────────┐
                    │ GitHub   │      │  README  │
                    │   API    │      │   JSON   │
                    └──────────┘      └──────────┘
```

---

## 🧩 コンポーネント設計

### 1. **main.py** - メインオーケストレーター

**責務:**
- 全体のフロー制御
- エラーハンドリング
- ロギング管理

**処理フロー:**
```python
1. 環境変数・設定の読み込み
2. GitHubClient初期化
3. Rate Limit確認
4. データ収集
5. データ分析
6. 出力生成（README + JSON）
7. コミット準備
```

---

### 2. **github_client.py** - GitHub API クライアント

**責務:**
- GitHub REST API との通信
- 認証管理
- Rate Limit 監視

**主要メソッド:**
```python
class GitHubClient:
    def __init__(token: str)
    def get_trending_repositories(limit: int) -> List[Dict]
    def get_repository_details(owner: str, repo: str) -> Dict
    def check_rate_limit() -> Dict
```

**API制限:**
- 認証済み: 5,000 requests/hour
- 未認証: 60 requests/hour
- Search API: 30 requests/minute

---

### 3. **analyzer.py** - データ分析エンジン

**責務:**
- リポジトリデータの抽出
- ランキング計算
- カテゴリ分類

**主要メソッド:**
```python
class TrendAnalyzer:
    def extract_repo_data(repos: List[Dict]) -> List[Dict]
    def rank_by_stars(repos: List[Dict], top_n: int) -> List[Dict]
    def categorize_by_language(repos: List[Dict]) -> Dict
    def categorize_by_topic(repos: List[Dict]) -> Dict
```

**分類ロジック:**
- トピックベース分類
- 言語ベース分類
- スター数ランキング

---

### 4. **renderer.py** - 出力生成エンジン

**責務:**
- README.md の生成
- JSON データの生成
- テンプレート処理

**主要メソッド:**
```python
class TrendRenderer:
    def generate_readme(trending, categories, timestamp) -> str
    def generate_json(trending, categories, timestamp) -> Dict
```

**出力形式:**
- Markdown: UTF-8エンコーディング
- JSON: インデント2スペース、ensure_ascii=False

---

## 📊 データフロー

```
GitHub API
    │
    ▼
[Raw JSON]
    │
    ▼
GitHubClient.get_trending_repositories()
    │
    ▼
[List[Dict]] 生データ
    │
    ▼
TrendAnalyzer.extract_repo_data()
    │
    ▼
[List[Dict]] 正規化データ
    │
    ├─▶ rank_by_stars() ─▶ トップ10
    │
    └─▶ categorize_by_topic() ─▶ カテゴリ別
              │
              ▼
       TrendRenderer
              │
              ├─▶ generate_readme() ─▶ README.md
              │
              └─▶ generate_json() ─▶ data/YYYY-MM-DD.json
```

---

## 🗂️ データモデル

### Repository データ構造

```json
{
  "name": "owner/repo",
  "description": "リポジトリの説明",
  "stars": 12345,
  "forks": 678,
  "language": "Python",
  "url": "https://github.com/owner/repo",
  "updated_at": "2025-11-03T00:00:00Z",
  "created_at": "2020-01-01T00:00:00Z",
  "topics": ["machine-learning", "python"],
  "open_issues": 42
}
```

### 出力 JSON 構造

```json
{
  "collected_at": "2025-11-03 09:00:00",
  "trending": [...],
  "categories": {
    "AI/ML": [...],
    "Web": [...]
  },
  "total_repos": 100,
  "metadata": {
    "version": "0.1.0",
    "source": "GitHub API"
  }
}
```

---

## ⚙️ 設定管理

### 環境変数

```bash
# 必須
GH_TOKEN=ghp_xxxxxxxxxxxxx

# オプション（将来実装）
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
GEMINI_API_KEY=AIzaSy...
```

### 設定ファイル（将来）

```yaml
# config.yml
collection:
  limit: 100
  languages:
    - Python
    - JavaScript
    - Go

categories:
  AI/ML:
    - machine-learning
    - artificial-intelligence
  Web:
    - web
    - frontend
```

---

## 🔄 GitHub Actions ワークフロー

### daily-update.yml

```yaml
name: Daily OSS Trend Update

on:
  schedule:
    - cron: "0 0 * * *"  # 毎日 00:00 UTC (JST 09:00)
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tracker
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: python src/main.py
      
      - name: Commit results
        run: |
          git config user.name "oss-tracker-bot"
          git config user.email "bot@ossorbit.dev"
          git add data/*.json README.md
          git commit -m "chore: daily update $(date +'%Y-%m-%d')"
          git push
```

---

## 🚀 拡張ポイント

### Phase 1: 現在実装済み
- ✅ GitHub API連携
- ✅ トップ10ランキング
- ✅ カテゴリ分類
- ✅ 自動更新

### Phase 2: 近日実装
- 🔲 HackerNews API連携
- 🔲 dev.to RSS連携
- 🔲 AI要約（Gemini API）
- 🔲 Discord通知

### Phase 3: 将来実装
- 🔲 GitHub Pages ダッシュボード
- 🔲 週次・月次レポート
- 🔲 スター増加率分析
- 🔲 コミュニティ貢献度分析

---

## 🔧 エラーハンドリング戦略

### Rate Limit対策
```python
if rate_limit['rate']['remaining'] < 10:
    logger.warning("Rate limit low, waiting...")
    time.sleep(60)
```

### API障害時
```python
try:
    repos = client.get_trending_repositories()
except requests.exceptions.RequestException as e:
    logger.error(f"API error: {e}")
    # 前日のデータを使用
    with open("data/latest.json") as f:
        repos = json.load(f)["trending"]
```

### データ欠損時
```python
# デフォルト値で補完
repo_data = {
    "name": repo.get("full_name", "unknown/unknown"),
    "stars": repo.get("stargazers_count", 0),
    # ...
}
```

---

## 📈 パフォーマンス指標

| 指標 | 目標値 |
|------|--------|
| **実行時間** | < 2分 |
| **API呼び出し** | < 50回/日 |
| **データサイズ** | < 100KB/日 |
| **成功率** | > 99% |

---

## 🧪 テスト戦略

### ユニットテスト
```python
# tests/test_analyzer.py
def test_rank_by_stars():
    repos = [{"stars": 100}, {"stars": 200}]
    result = analyzer.rank_by_stars(repos)
    assert result[0]["stars"] == 200
```

### 統合テスト
```python
# tests/test_integration.py
def test_full_pipeline():
    client = GitHubClient(token=TEST_TOKEN)
    repos = client.get_trending_repositories(limit=10)
    assert len(repos) > 0
```

---

このアーキテクチャは、**シンプル・拡張可能・無料運用**の3原則に基づいて設計されています。
