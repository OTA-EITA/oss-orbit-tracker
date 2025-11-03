# 🧭 oss-orbit-tracker: プロジェクトルール

> このドキュメントは、`oss-orbit-tracker`（Free Edition）の開発・運用・貢献ルールを定義します。  
> 目的は「**無料で継続可能なOSSトラッカーの開発**」と「**誰でも安心して貢献できるプロジェクト文化**」の両立です。

---

## 🎯 プロジェクトの基本理念

1. **完全無料で動作するOSS**  
   - 有料API・クラウドサービス・DBを使用しない  
   - GitHub Actions / Pages / 無料API のみで構築  

2. **自動化と継続性を最優先**  
   - 手動作業を減らし、スケジュール駆動で毎日動作  
   - 継続運用できる軽量構成を保つ  

3. **OSSとしての透明性**  
   - データ収集・更新ロジック・依存関係を明確化  
   - 公開リポジトリ・MITライセンスで運営  

4. **コミュニティが育てるエコシステム**  
   - フォークやPRを歓迎  
   - 「一緒に改善できる仕組み」を重視  

---

## ⚙️ 技術ポリシー

| 項目 | 内容 |
|------|------|
| **実行基盤** | GitHub Actions（スケジュールcron） |
| **ホスティング** | GitHub Pages（静的HTML/JS） |
| **主要言語** | Python 3.11 以降 |
| **データ形式** | JSON（履歴保存）＋ Markdown（README反映） |
| **AI要約** | Gemini API / Ollama / HuggingFace Inference API（無料枠） |
| **通知** | Discord / Slack Webhook（無料プラン） |
| **外部データソース** | GitHub API, HackerNews API, dev.to RSS |
| **データベース** | 使用禁止（ローカルJSONのみ） |

---

## 🧩 ディレクトリ構成ルール

```
oss-orbit-tracker/
├── src/                # コード本体
│   ├── main.py         # メイン実行スクリプト
│   ├── github_client.py
│   ├── hn_client.py
│   ├── summarizer.py
│   ├── renderer.py
│   └── notifier.py
├── data/               # JSONデータ（日次アーカイブ）
│   ├── 2025-11-02.json
│   ├── 2025-11-03.json
│   └── latest.json
├── templates/          # README / HTML テンプレート
│   ├── readme_template.md.j2
│   └── page_template.html.j2
├── .github/
│   └── workflows/
│       └── daily-update.yml
├── docs/               # プロジェクト説明資料
│   ├── project_rules.md
│   └── architecture.md
└── README.md
```

---

## 🧠 コーディングルール

| 規則 | 内容 |
|------|------|
| **言語** | Python 3.11+（型ヒント必須） |
| **コードスタイル** | PEP8 + Black フォーマット |
| **命名規則** | snake_case（関数・変数） / PascalCase（クラス） |
| **ドキュメンテーション** | docstring必須 (`"""..."""`形式) |
| **依存管理** | `requirements.txt` に明記（最小限） |
| **秘密情報** | `.env` に定義、GitHub Secrets で管理 |
| **ログ** | `logging` 標準モジュール使用、print禁止 |
| **例外処理** | 全例外をtry-exceptで明示処理 |
| **外部API呼び出し** | 1秒以上のレート制限を遵守（GitHub API制限対策） |

---

## 🧩 コミット・ブランチルール

| 項目 | ルール |
|------|--------|
| **メインブランチ** | `main`：安定版のみマージ可 |
| **開発ブランチ** | `feature/<機能名>` |
| **コミットメッセージ形式** | `type(scope): summary` |
| **主なtype例** | `feat`, `fix`, `docs`, `chore`, `refactor`, `style` |
| **例** | `feat(analyzer): add daily GitHub trend parser` |
| **PRタイトル** | コミット形式に準拠 |
| **レビュー要件** | 自動テスト＋README更新確認 |

---

## 📦 データ運用ルール

| 項目 | 内容 |
|------|------|
| **保存形式** | `data/YYYY-MM-DD.json` |
| **最新データ** | `data/latest.json` にコピー |
| **バックアップ** | 直近7日分を保持、古いデータは自動削除 |
| **README更新** | 最新データからJinja2で生成 |
| **公開対象** | JSON / README / Pages（※個人情報なし） |

---

## 🔒 セキュリティとプライバシー

1. 個人情報・トークン・メールアドレスは**絶対に出力しない**
2. `GH_TOKEN` や `DISCORD_WEBHOOK_URL` は GitHub Secrets に保存
3. 無料APIの利用上限に注意（Rate Limit対策を実装）
4. 外部データは**オープンソース・公開情報のみ**を扱う
5. 脆弱性報告は `SECURITY.md` に従いGitHub Issueで受付

---

## 🌱 運用ポリシー

- **自動commitポリシー**
  - `chore: daily update YYYY-MM-DD` 形式で行う
  - コミットログをスパム化させない（1日1回に制限）

- **Actions実行時間**
  - 毎日0:00 UTC（JST:9:00）に実行

- **障害発生時**
  - Discord通知でアラート送信
  - リトライは最大3回まで

---

## 🤝 コントリビューションガイド

1. Forkしてブランチを作成（`feature/<your-feature>`）
2. コード変更・テストを実施
3. PRを送信（タイトルは `feat(scope): summary` 形式）
4. CI（GitHub Actions）でエラーがないことを確認
5. メンテナがレビューし、`main`へマージ

---

## 📜 ライセンス

- 本プロジェクトは **MIT License** で提供します。  
- 全てのソースコード・生成データは自由に再利用可能です。  
- クレジット表記（"Powered by oss-orbit-tracker"）を歓迎します。

---

## 🪴 最後に

> このプロジェクトは「**草が育つOSS**」をテーマにしています。  
> 自動化・透明性・無料運用という3本柱を守りながら、  
> 世界中のOSS活動を毎日観測していきましょう。
