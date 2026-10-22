# 🌍 OSS Orbit Tracker

> 世界中のOSSトレンドを毎日収集・分析・可視化するオープンデータプロジェクト

[![Daily Update](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/daily-update.yml/badge.svg)](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/daily-update.yml)
[![Weekly Cleanup](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/weekly-cleanup.yml/badge.svg)](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/weekly-cleanup.yml)
[![Quality Check](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/quality-check.yml/badge.svg)](https://github.com/OTA-EITA/oss-orbit-tracker/actions/workflows/quality-check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 プロジェクト概要

GitHub全体の人気OSS・注目プロジェクト・活発リポジトリを**毎日自動で収集・可視化**します。

### ✨ 特徴

- 🤖 **完全自動化**: GitHub Actionsで毎日自動更新
- 📊 **マルチソース**: GitHub + HackerNews のトレンド収集
- 📰 **技術記事**: 人気の技術記事も自動収集
- 🌐 **オープンデータ**: JSON形式で誰でも利用可能
- 💰 **完全無料**: 有料APIやDBを使わない設計
- 🌱 **草が育つ**: 毎日のcommitで自動的に草が生える!

---

## 🚀 クイックスタート

### 必要なもの

- Python 3.11以降
- GitHub Personal Access Token（GitHub APIのみ必須）

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/OTA-EITA/oss-orbit-tracker.git
cd oss-orbit-tracker

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env ファイルを編集して GH_TOKEN を設定
```

### 環境変数の設定

#### 必須
- **`GH_TOKEN`**: GitHub Personal Access Token
  - [取得方法](https://github.com/settings/tokens)
  - スコープ: `public_repo` (読み取り専用)

#### オプション（自動的にスキップ）
- **HackerNews API**: 認証不要・自動動作
- **Discord/Slack通知**: 将来機能（未実装）
- **AI要約**: 将来機能（未実装）

```bash
# .env (最小構成)
GH_TOKEN=ghp_your_token_here

# HackerNews APIは認証不要なので設定不要!
```

### 実行

```bash
# トレンドデータを収集（GitHub + HackerNews）
python src/main.py

# 古いデータをクリーンアップ（7日以上前）
python scripts/cleanup.py --retention-days 7
```

---

## 📊 データソース

### 収集データ

| ソース | 内容 | 認証 | レート制限 |
|--------|------|------|-----------|
| **GitHub API** | リポジトリトレンド | 必須 | 5,000/時 |
| **HackerNews API** | 技術記事トレンド | 不要 | 無制限 |

### 出力形式

```json
{
  "collected_at": "2025-11-03 09:00:00",
  "trending": [...],          // GitHub repos
  "hn_stories": [...],        // HackerNews stories
  "categories": {...},
  "total_repos": 50,
  "total_hn_stories": 10,
  "metadata": {
    "version": "0.4.0",
    "sources": ["GitHub API", "HackerNews API"]
  }
}
```

---

## 📁 プロジェクト構造

```
oss-orbit-tracker/
├── src/
│   ├── main.py              # メインオーケストレーター
│   ├── github_client.py     # GitHub API クライアント
│   ├── hn_client.py         # HackerNews API クライアント ✨
│   ├── analyzer.py          # データ分析
│   └── renderer.py          # 出力生成
├── data/
│   ├── YYYY-MM-DD.json      # 日次データ
│   └── latest.json          # 最新データ
├── templates/
│   └── readme_template.md.j2
└── scripts/
    └── cleanup.py           # データクリーンアップ
```

---

## 🤖 自動化

### 毎日の更新

- **実行時刻**: 毎日 09:00 JST (00:00 UTC)
- **処理内容**:
  1. GitHub APIからトレンドリポジトリを収集
  2. HackerNews APIから人気記事を収集 ✨
  3. データを分析・ランキング化
  4. README.mdとJSONファイルを更新
  5. 自動commit & push
  6. 古いデータファイルをクリーンアップ
  7. 日次レポートをIssueに投稿

### 週次クリーンアップ

- **実行時刻**: 毎週日曜日 12:00 JST
- **処理内容**: 7日以上前のJSONファイルを削除

---

## 📈 ロードマップ

現在の開発フェーズ: **v0.4** 🎉

### ✅ 完了済み

- [x] v0.1: GitHub API連携
- [x] v0.2: トップ10ランキング
- [x] v0.3: カテゴリ分類・ロギング強化
- [x] v0.4: HackerNews API連携 ✨

### 🚧 開発中

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
└──┬──────────────────────┬───────────────┘
   │                      │
   ▼                      ▼
┌──────────────┐    ┌──────────────┐
│github_client │    │  hn_client   │ ✨
│ (GitHub API) │    │ (HN API)     │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └────────┬──────────┘
                ▼
          ┌──────────┐
          │ analyzer │
          │ (分析)   │
          └────┬─────┘
               ▼
          ┌──────────┐
          │ renderer │
          │ (出力)   │
          └────┬─────┘
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

---

## 📚 ドキュメント

- [プロジェクトルール](docs/project_rules.md)
- [アーキテクチャ設計](docs/architecture.md)
- [ロードマップ](.github/ROADMAP.md)
- [セキュリティポリシー](SECURITY.md)
- [HackerNews連携ドキュメント](.github/ISSUE_2_COMPLETE.md) ✨

---

## 💡 使用例

### プログラムから利用

```python
import json

# 最新データを読み込み
with open('data/latest.json') as f:
    data = json.load(f)

# GitHubトレンド
for repo in data['trending'][:5]:
    print(f"{repo['name']}: {repo['stars']} stars")

# HackerNewsトレンド ✨
for story in data['hn_stories'][:5]:
    print(f"{story['title']}: {story['score']} points")

# カテゴリ別
ai_repos = data['categories'].get('AI/ML', [])
```

---

## 📄 ライセンス

[MIT License](LICENSE)

このプロジェクトは完全にオープンソースです。自由に使用・改変・再配布できます。

---

## 🙏 謝辞

- **GitHub API**: OSSリポジトリトレンドの提供
- **HackerNews API**: 技術記事トレンドの提供 ✨
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

[![Star History Chart](https://api.star-history.com/svg?repos=OTA-EITA/oss-orbit-tracker&type=Date)](https://star-history.com/#OTA-EITA/oss-orbit-tracker&Date)
