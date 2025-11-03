# 📋 Implementation Roadmap & Issues

このドキュメントは、プロジェクトの今後の実装課題と優先度を管理します。

---

## 🚀 Phase 1: Core Features (v0.1 - v0.3) ✅

### ✅ Completed

- [x] プロジェクト基盤構築
- [x] GitHub API連携実装
- [x] トップ10ランキング機能
- [x] カテゴリ分類機能
- [x] 自動更新ワークフロー
- [x] ロギング機能実装
- [x] 例外処理強化
- [x] 型ヒント完全化
- [x] ドキュメント整備

---

## 🔧 Phase 2: Enhancement Features (v0.4 - v0.6)

### High Priority

#### Issue #1: latest.json の自動生成
**Priority:** High  
**Labels:** `enhancement`, `good-first-issue`

**Description:**
現在、日次JSONファイルは生成されているが、最新データへのクイックアクセスのために `data/latest.json` を自動生成する機能が必要。

**Tasks:**
- [ ] main.py で latest.json を生成
- [ ] latest.json のスキーマをドキュメント化
- [ ] 古いデータの自動削除機能（7日以上前）

**Acceptance Criteria:**
- 毎回の実行で data/latest.json が更新される
- 7日以前のJSONファイルは自動削除される

---

#### Issue #2: HackerNews API 連携
**Priority:** High  
**Labels:** `enhancement`, `new-feature`

**Description:**
GitHub以外のソースとして、HackerNews APIから人気の技術記事を収集する。

**Tasks:**
- [ ] `src/hn_client.py` の実装
- [ ] HN APIからトップストーリーを取得
- [ ] GitHub repos と HN stories を統合
- [ ] README に HN セクションを追加

**API Reference:**
- https://github.com/HackerNews/API

**Acceptance Criteria:**
- HackerNewsの人気記事トップ10を取得できる
- GitHubデータと統合されて表示される

---

#### Issue #3: dev.to RSS フィード連携
**Priority:** Medium  
**Labels:** `enhancement`, `new-feature`

**Description:**
dev.to の人気記事をRSSフィードから取得し、トレンドに追加。

**Tasks:**
- [ ] RSS パーサーの実装
- [ ] dev.to RSS フィードの取得
- [ ] データの正規化
- [ ] README への統合

**Acceptance Criteria:**
- dev.toの人気記事を取得できる
- RSSフィードのエラーハンドリングが実装されている

---

#### Issue #4: データクリーンアップスクリプト
**Priority:** Medium  
**Labels:** `chore`, `maintenance`

**Description:**
古いJSONファイルを自動削除し、リポジトリサイズを管理する。

**Tasks:**
- [ ] `scripts/cleanup.py` の作成
- [ ] 7日以上前のファイルを削除
- [ ] GitHub Actions での自動実行
- [ ] ログ出力

**Acceptance Criteria:**
- 7日以上前のJSONファイルが削除される
- GitHub Actionsで週1回自動実行される

---

### Medium Priority

#### Issue #5: AI要約機能（Gemini API）
**Priority:** Medium  
**Labels:** `enhancement`, `ai`, `experimental`

**Description:**
Gemini API（無料枠）を使って、日次トレンドの要約を自動生成。

**Tasks:**
- [ ] `src/summarizer.py` の実装
- [ ] Gemini API 連携
- [ ] プロンプトエンジニアリング
- [ ] README に要約セクション追加
- [ ] エラーハンドリング（API制限対応）

**Requirements:**
- GEMINI_API_KEY の設定
- 無料枠の制限に配慮

**Acceptance Criteria:**
- トレンドの自動要約が生成される
- API制限時には graceful degradation

---

#### Issue #6: Discord/Slack 通知機能
**Priority:** Medium  
**Labels:** `enhancement`, `notification`

**Description:**
日次更新時にDiscord/SlackにWebhook通知を送信。

**Tasks:**
- [ ] `src/notifier.py` の実装
- [ ] Discord Webhook 対応
- [ ] Slack Webhook 対応
- [ ] 通知フォーマットの設計
- [ ] エラー時の通知

**Acceptance Criteria:**
- 日次更新完了時に通知が送信される
- エラー発生時にも通知が送信される

---

#### Issue #7: スター増加率分析
**Priority:** Medium  
**Labels:** `enhancement`, `analytics`

**Description:**
前日比でのスター増加数・増加率を計算し、「急上昇リポジトリ」を特定。

**Tasks:**
- [ ] 前日データとの差分計算
- [ ] 増加率ランキング生成
- [ ] README に急上昇セクション追加
- [ ] グラフ化（SVGバッジ）

**Acceptance Criteria:**
- スター増加率トップ10が表示される
- 前日データがない場合のエラーハンドリング

---

### Low Priority

#### Issue #8: GitHub Pages ダッシュボード
**Priority:** Low  
**Labels:** `enhancement`, `visualization`, `v1.0`

**Description:**
GitHub Pagesで静的HTMLダッシュボードを作成し、トレンドをグラフ表示。

**Tasks:**
- [ ] `templates/page_template.html.j2` の作成
- [ ] Chart.js または Plotly.js 導入
- [ ] 時系列グラフの実装
- [ ] カテゴリ別円グラフ
- [ ] レスポンシブデザイン
- [ ] GitHub Pages へのデプロイ設定

**Acceptance Criteria:**
- インタラクティブなダッシュボードが表示される
- モバイル対応
- 過去データの時系列表示

---

#### Issue #9: 週次・月次レポート
**Priority:** Low  
**Labels:** `enhancement`, `reporting`

**Description:**
週次・月次での集計レポートを自動生成。

**Tasks:**
- [ ] 週次集計ロジック
- [ ] 月次集計ロジック
- [ ] レポートテンプレート作成
- [ ] GitHub Issue への自動投稿

**Acceptance Criteria:**
- 毎週月曜日に週次レポートが生成される
- 毎月1日に月次レポートが生成される

---

#### Issue #10: 多言語対応（i18n）
**Priority:** Low  
**Labels:** `enhancement`, `i18n`

**Description:**
README を英語・日本語の両方で生成。

**Tasks:**
- [ ] テンプレートの多言語化
- [ ] 言語切り替え機構
- [ ] README_en.md の自動生成
- [ ] GitHub Pages の多言語対応

**Acceptance Criteria:**
- README.md（日本語）とREADME_en.md（英語）が生成される

---

## 🐛 Bugs & Improvements

### Issue #11: Rate Limit 警告の改善
**Priority:** High  
**Labels:** `bug`, `enhancement`

**Description:**
Rate Limit残量が少ない場合の警告を改善し、適切な待機時間を提案。

**Tasks:**
- [ ] Rate Limit チェックの強化
- [ ] リセット時刻の表示
- [ ] 自動待機機能（オプション）

---

### Issue #12: エラーログの充実
**Priority:** Medium  
**Labels:** `enhancement`, `logging`

**Description:**
エラー時のログをより詳細にし、デバッグを容易にする。

**Tasks:**
- [ ] スタックトレースの完全出力
- [ ] エラーコンテキストの追加
- [ ] ログローテーション設定

---

### Issue #13: ユニットテストの追加
**Priority:** Medium  
**Labels:** `test`, `quality`

**Description:**
各モジュールのユニットテストを追加し、CI/CDで自動実行。

**Tasks:**
- [ ] test_github_client.py
- [ ] test_analyzer.py
- [ ] test_renderer.py
- [ ] pytest の設定
- [ ] GitHub Actions での自動実行

---

## 📊 Metrics & Goals

### v0.4 Goals
- [ ] Issue #1: latest.json 実装
- [ ] Issue #4: データクリーンアップ
- [ ] Issue #11: Rate Limit 改善

### v0.5 Goals
- [ ] Issue #2: HackerNews 連携
- [ ] Issue #6: 通知機能
- [ ] Issue #13: テスト追加

### v1.0 Goals
- [ ] Issue #8: GitHub Pages ダッシュボード
- [ ] Issue #7: スター増加率分析
- [ ] 全主要機能の完成

---

## 🎯 Contributing

これらの課題に取り組みたい方は:

1. 該当する Issue を作成
2. コメントで取り組みを宣言
3. `feature/<issue-number>-<description>` ブランチで開発
4. PR を送信

詳しくは [CONTRIBUTING.md](../CONTRIBUTING.md) をご覧ください。

---

**Last Updated:** 2025-11-03
