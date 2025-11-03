# 🌍 OSS Orbit Tracker

> 世界中のOSSトレンドを毎日収集・分析・可視化するオープンデータプロジェクト

[![Daily Update](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/daily-update.yml/badge.svg)](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/daily-update.yml)
[![Weekly Cleanup](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/weekly-cleanup.yml/badge.svg)](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/weekly-cleanup.yml)
[![Quality Check](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/quality-check.yml/badge.svg)](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/quality-check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 プロジェクト概要

GitHub全体の人気OSS・注目プロジェクト・活発リポジトリを**毎日自動で収集・可視化**します。

### ✨ 特徴

- 🤖 **完全自動化**: GitHub Actionsで毎日自動更新
- 📊 **トレンド分析**: スター数・フォーク数・カテゴリ別ランキング
- 🌐 **オープンデータ**: JSON形式で誰でも利用可能
- 💰 **完全無料**: 有料APIやDBを使わない設計
- 🌱 **草が育つ**: 毎日のcommitで自動的に草が生える!

---

## 🚀 クイックスタート

### 必要なもの

- Python 3.11以降
- GitHub Personal Access Token

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/oss-orbit-tracker.git
cd oss-orbit-tracker

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env ファイルを編集して GH_TOKEN を設定
```

### GitHub Tokenの取得

1. [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens) にアクセス
2. "Generate new token (classic)" をクリック
3. スコープ: `public_repo` を選択（読み取り専用でOK）
4. トークンをコピーして `.env` に設定

```bash
# .env
GH_TOKEN=ghp_your_token_here
```

### 実行

```bash
# トレンドデータを収集
python src/main.py

# 古いデータをクリーンアップ（7日以上前）
python scripts/cleanup.py --retention-days 7
```

---

## 📊 最新トレンド

[最新のトレンドデータ](data/latest.json)を確認するか、以下のREADMEセクションをご覧ください。

<!-- トレンドデータは自動更新されます -->

---

## 📁 データ構造

### JSON出力形式

```json
{
  "collected_at": "2025-11-03 09:00:00",
  "trending": [
    {
      "name": "owner/repo",
      "description": "リポジトリの説明",
      "stars": 12345,
      "forks": 678,
      "language": "Python",
      "url": "https://github.com/owner/repo",
      "topics": ["machine-learning", "python"]
    }
  ],
  "categories": {
    "AI/ML": [...],
    "Web": [...]
  },
  "total_repos": 100,
  "metadata": {
    "version": "0.3.0",
    "source": "GitHub API"
  }
}
```

### データの利用

```python
import json

# 最新データを読み込み
with open('data/latest.json') as f:
    data = json.load(f)

# トップ10を取得
top10 = data['trending'][:10]

# カテゴリ別データ
ai_repos = data['categories']['AI/ML']
```

---

## 🤖 自動化

### 毎日の更新

- **実行時刻**: 毎日 09:00 JST (00:00 UTC)
- **処理内容**:
  1. GitHub APIからトレンドデータを収集
  2. データを分析・ランキング化
  3. README.mdとJSONファイルを更新
  4. 自動commit & push
  5. 古いデータファイルをクリーンアップ
  6. 日次レポートをIssueに投稿

### 週次クリーンアップ

- **実行時刻**: 毎週日曜日 12:00 JST
- **処理内容**: 7日以上前のJSONファイルを削除

---

## 📈 ロードマップ

現在の開発フェーズ: **v0.3** 🎉

### ✅ 完了済み

- [x] v0.1: GitHub API連携
- [x] v0.2: トップ10ランキング
- [x] v0.3: カテゴリ分類
- [x] ロギング・例外処理の強化
- [x] データクリーンアップ機能

### 🚧 開発中

- [ ] v0.4: HackerNews API連携
- [ ] v0.5: Discord/Slack通知
- [ ] v0.6: AI要約機能（Gemini）

### 🔮 今後の予定

- [ ] v1.0: GitHub Pages ダッシュボード
- [ ] スター増加率分析
- [ ] 週次・月次レポート

詳細は [ROADMAP.md](.github/ROADMAP.md) をご覧ください。

---

## 🏗️ アーキテクチャ

```
┌─────────────────────────────────────────┐
│         GitHub Actions (Scheduler)       │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│              main.py                     │
│  (オーケストレーター)                     │
└─────┬───────────────────┬───────────────┘
      │                   │
      ▼                   ▼
┌─────────────┐     ┌─────────────┐
│github_client│     │  analyzer   │
│  (API連携)  │     │  (分析)     │
└─────┬───────┘     └──────┬──────┘
      │                    │
      └──────┬─────────────┘
             ▼
       ┌─────────────┐
       │  renderer   │
       │  (出力)     │
       └──────┬──────┘
              │
              ▼
       ┌─────────────┐
       │README + JSON│
       └─────────────┘
```

詳細は [docs/architecture.md](docs/architecture.md) をご覧ください。

---

## 🤝 コントリビューション

貢献を歓迎します!以下の方法で参加できます:

1. 🐛 **バグ報告**: Issueを作成
2. 💡 **機能提案**: Feature Requestを作成
3. 🔧 **プルリクエスト**: コードを改善
4. 📖 **ドキュメント**: ドキュメントを改善
5. ⭐ **スター**: プロジェクトにスターを付ける

詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

### Good First Issues

初めての方は、以下のIssueから始めてみてください:

- [Issue #1: latest.json 自動生成](https://github.com/YOUR_USERNAME/oss-orbit-tracker/issues)
- [Issue #4: データクリーンアップ](https://github.com/YOUR_USERNAME/oss-orbit-tracker/issues)

---

## 📚 ドキュメント

- [プロジェクトルール](docs/project_rules.md)
- [アーキテクチャ設計](docs/architecture.md)
- [ロードマップ](.github/ROADMAP.md)
- [セキュリティポリシー](SECURITY.md)

---

## 📄 ライセンス

[MIT License](LICENSE)

このプロジェクトは完全にオープンソースです。自由に使用・改変・再配布できます。

---

## 🙏 謝辞

- **GitHub API**: トレンドデータの提供
- **GitHub Actions**: 無料の自動化プラットフォーム
- **OSS Community**: 世界中のオープンソースコントリビューター

---

## 📞 お問い合わせ

- **Issues**: バグ報告・機能リクエスト
- **Discussions**: 質問・アイデア共有
- **Security**: セキュリティ問題は [SECURITY.md](SECURITY.md) を参照

---

**Made with ❤️ by OSS Community**

🗓 最終更新: このファイルは毎日自動更新されます

---

## ⭐ スター履歴

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/oss-orbit-tracker&type=Date)](https://star-history.com/#YOUR_USERNAME/oss-orbit-tracker&Date)
