# OSS Orbit Tracker

> 世界中のOSSトレンドを毎日収集・分析・可視化するオープンデータプロジェクト

[![Daily Update](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/daily-update.yml/badge.svg)](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/daily-update.yml)
[![Quality Check](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/quality-check.yml/badge.svg)](https://github.com/YOUR_USERNAME/oss-orbit-tracker/actions/workflows/quality-check.yml)

## 🎯 プロジェクト概要

GitHub全体の人気OSS・注目プロジェクト・活発リポジトリを**毎日自動で収集・可視化**します。

- 📊 **毎日更新**: GitHub Actionsで完全自動化
- 🌍 **完全OSS**: MIT Licenseで誰でも利用可能
- 📈 **トレンド追跡**: スター数・フォーク数・更新頻度を分析
- 🤖 **自動commit**: 毎日の更新で草を育てる

## 📊 今日のトレンド

> 最終更新: 準備中

トレンドデータは初回実行後に表示されます。

## 🚀 セットアップ

### 必要な環境

- Python 3.11+
- GitHub Personal Access Token

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/oss-orbit-tracker.git
cd oss-orbit-tracker

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
export GH_TOKEN=your_personal_access_token

# 実行
python src/main.py
```

## 🏗️ プロジェクト構造

```
oss-orbit-tracker/
├── src/
│   ├── main.py           # メインエントリーポイント
│   ├── github_client.py  # GitHub API クライアント
│   ├── analyzer.py       # データ分析
│   └── renderer.py       # Markdown/JSON生成
├── data/                 # 日次データ (YYYY-MM-DD.json)
├── tests/                # テストコード
├── .github/
│   └── workflows/
│       ├── daily-update.yml    # 毎日の自動更新
│       └── quality-check.yml   # コード品質チェック
└── README.md
```

## 🤖 自動化

- **毎日午前9時 (JST)**: トレンドデータを自動収集
- **自動commit**: データ更新とREADME更新
- **Issue作成**: 日次レポートを自動生成

## 📈 ロードマップ

- [x] プロジェクト基盤構築
- [ ] GitHub API連携 (v0.1)
- [ ] トップ10ランキング (v0.2)
- [ ] カテゴリ分類 (v0.3)
- [ ] GitHub Pages可視化 (v1.0)

## 🤝 コントリビューション

Issue・PRを歓迎します！

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

---

**Made with ❤️ by OSS Community**
