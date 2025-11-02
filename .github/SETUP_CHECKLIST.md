# 🚀 OSS Orbit Tracker セットアップチェックリスト

このファイルは初回セットアップ時に確認すべき項目をリストアップしています。

## ✅ 必須セットアップ

### 1. GitHubリポジトリ作成
- [ ] リポジトリを作成 (`YOUR_USERNAME/oss-orbit-tracker`)
- [ ] ローカルからpush
```bash
cd /Users/ota-eita/Documents/work/oss-orbit-tracker
git init
git add .
git commit -m "feat: initial project setup"
git branch -M master
git remote add origin https://github.com/YOUR_USERNAME/oss-orbit-tracker.git
git push -u origin master
```

### 2. GitHub Personal Access Token (PAT) 作成
- [ ] [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens) にアクセス
- [ ] "Generate new token (classic)" をクリック
- [ ] Scopeを選択:
  - [x] `public_repo` (公開リポジトリへのアクセス)
  - [x] `read:org` (オプション: 組織データを読む場合)
- [ ] トークンをコピーして保存

### 3. GitHub Secrets設定
- [ ] リポジトリの **Settings > Secrets and variables > Actions** に移動
- [ ] 以下のSecretsを追加:
  - `PERSONAL_ACCESS_TOKEN`: 上記で作成したPersonal Access Token
  - `GIT_USER_NAME`: "oss-tracker-bot" (またはお好みの名前)
  - `GIT_USER_EMAIL`: "bot@ossorbit.dev" (またはお好みのメール)

### 4. GitHub Actions有効化
- [ ] リポジトリの **Actions** タブに移動
- [ ] "I understand my workflows, go ahead and enable them" をクリック
- [ ] "Daily OSS Trend Update" workflowを選択
- [ ] "Enable workflow" をクリック

### 5. 初回手動実行
- [ ] "Daily OSS Trend Update" workflowを開く
- [ ] "Run workflow" をクリック
- [ ] masterブランチを選択して実行
- [ ] ワークフローの成功を確認

## 🧪 テスト実行

### ローカルでのテスト
```bash
# 環境変数を設定
export GH_TOKEN=your_personal_access_token

# スクリプトを実行
python src/main.py

# 出力を確認
ls -la data/
cat README.md
```

### 期待される出力
- ✅ `data/YYYY-MM-DD.json` ファイルが作成される
- ✅ `README.md` がトレンドデータで更新される
- ✅ コンソールに成功メッセージが表示される

## 📋 README更新

- [ ] READMEの `YOUR_USERNAME` を実際のGitHubユーザー名に置換
```bash
sed -i 's/YOUR_USERNAME/your-github-username/g' README.md
git add README.md
git commit -m "docs: update username in README"
git push
```

## 🐛 トラブルシューティング

### Rate Limit エラー
- GitHub APIのrate limitに達した場合
- 解決策: 少し待ってから再実行

### 認証エラー
- `GH_TOKEN` が正しく設定されているか確認
- トークンのScopeが正しいか確認

### データが取得できない
- `github_client.py` のクエリを確認
- GitHub APIの応答を確認: https://api.github.com/rate_limit

## 📊 確認項目

### 初回実行後
- [ ] data/ディレクトリにJSONファイルが作成されている
- [ ] README.mdにトレンドデータが表示されている
- [ ] GitHub Actionsが正常に完了している
- [ ] 自動commitが作成されている

### 2日目以降
- [ ] 毎日午前9時に自動実行されている
- [ ] 日次レポートIssueが作成されている
- [ ] 履歴データが蓄積されている

## 🎯 次のステップ

セットアップ完了後、以下の拡張を検討:

1. **データ分析の改善**
   - [ ] 前日比較機能の実装
   - [ ] トレンドスコアの計算
   - [ ] カテゴリ分類の精度向上

2. **可視化の強化**
   - [ ] SVGバッジの生成
   - [ ] GitHub Pagesダッシュボード
   - [ ] チャート/グラフの追加

3. **通知機能**
   - [ ] Slack通知
   - [ ] Discord通知
   - [ ] メール通知

4. **API提供**
   - [ ] REST API endpoint
   - [ ] JSON API

---

**セットアップ完了後、このファイルは削除してOKです！**

最終更新: 2025-11-02
