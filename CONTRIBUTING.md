# 🤝 Contributing to OSS Orbit Tracker

ご協力ありがとうございます!このプロジェクトへの貢献を歓迎します。

---

## 🌟 貢献の方法

### 1. バグ報告

バグを見つけた場合は、以下の情報を含めてIssueを作成してください:

- **環境**: OS、Pythonバージョン
- **再現手順**: バグを再現する方法
- **期待される動作**: 本来どう動くべきか
- **実際の動作**: 何が起きたか
- **ログ**: エラーメッセージやスタックトレース

### 2. 機能リクエスト

新機能の提案は大歓迎です!以下を含めてください:

- **ユースケース**: なぜこの機能が必要か
- **提案内容**: 具体的にどんな機能か
- **実装案**: 可能であれば実装方法のアイデア

### 3. プルリクエスト

コードの貢献は以下の手順で:

1. このリポジトリをFork
2. 新しいブランチを作成 (`feature/amazing-feature`)
3. 変更を実装
4. テストを追加・実行
5. コミット (`git commit -m 'feat: add amazing feature'`)
6. Pushして (`git push origin feature/amazing-feature`)
7. Pull Requestを作成

---

## 📝 コミットメッセージ規約

このプロジェクトは[Conventional Commits](https://www.conventionalcommits.org/)に従います:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
- `refactor`: バグ修正や機能追加を伴わないコード変更
- `perf`: パフォーマンス改善
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

### 例

```bash
feat(analyzer): add weekly trend analysis
fix(client): handle rate limit gracefully
docs(readme): update installation instructions
chore: update dependencies
```

---

## 🧪 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/oss-orbit-tracker.git
cd oss-orbit-tracker

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env ファイルにGH_TOKENを設定

# テスト実行
python src/main.py
```

---

## 🎨 コーディングスタイル

### Python

- **PEP 8**に従う
- **型ヒント**を必ず使用
- **Docstring**を全ての関数・クラスに記述
- **Black**でフォーマット（推奨）

```python
def analyze_trends(repos: List[Dict[str, Any]], threshold: int = 100) -> List[Dict[str, Any]]:
    """Analyze repository trends based on star count.
    
    Args:
        repos: List of repository data dictionaries
        threshold: Minimum star count to include
        
    Returns:
        Filtered and sorted list of trending repositories
        
    Raises:
        ValueError: If repos is empty
    """
    if not repos:
        raise ValueError("Repository list cannot be empty")
    
    return [r for r in repos if r["stars"] >= threshold]
```

### ロギング

`print()`ではなく`logging`モジュールを使用:

```python
import logging

logger = logging.getLogger(__name__)

# Good
logger.info("Fetching trending repositories")
logger.error(f"API error: {error}")

# Bad
print("Fetching trending repositories")
```

---

## ✅ テスト

新機能を追加する場合は、対応するテストも追加してください:

```python
# tests/test_analyzer.py
import pytest
from src.analyzer import TrendAnalyzer

def test_rank_by_stars():
    analyzer = TrendAnalyzer()
    repos = [
        {"name": "repo1", "stars": 100},
        {"name": "repo2", "stars": 200},
    ]
    
    result = analyzer.rank_by_stars(repos, top_n=1)
    
    assert len(result) == 1
    assert result[0]["stars"] == 200
```

テスト実行:
```bash
pytest tests/
```

---

## 📚 ドキュメント

- 新機能を追加したら、READMEを更新
- 複雑な機能は`docs/`にドキュメントを追加
- APIの変更は`docs/architecture.md`を更新

---

## 🔍 レビュープロセス

1. PRを作成すると、GitHub Actionsで自動チェックが実行されます
2. メンテナがコードレビューを行います
3. 必要に応じて修正をお願いする場合があります
4. 承認されたら`main`ブランチにマージされます

---

## 🙏 コミュニティガイドライン

- 尊重と礼儀を持って接する
- 建設的なフィードバックを心がける
- 他の人の時間を尊重する
- 初心者にも優しく

---

## 📞 質問・相談

- **バグ報告・機能リクエスト**: GitHubのIssue
- **セキュリティの問題**: `SECURITY.md`を参照
- **一般的な質問**: DiscussionsまたはIssue

---

## 🎉 コントリビューター

すべてのコントリビューターに感謝します!

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- プルリクエストでコントリビューターが追加されます -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

**ハッピーコーディング! 🚀**
