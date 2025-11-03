# 🎯 v0.4.0 - HackerNews Integration Commit Guide

**Feature**: HackerNews API Integration  
**Issue**: #2  
**Files**: 4 new/modified

---

## 📋 Commit Sequence

### 1. HackerNews Client

```bash
git add src/hn_client.py
git commit -m "feat(hn): add HackerNews API client"
```

**Changes:**
- 新しいHackerNewsクライアント実装
- トップストーリー・詳細取得機能
- リトライロジック・エラーハンドリング
- レート制限対策

---

### 2. Main Pipeline Integration

```bash
git add src/main.py
git commit -m "feat(main): integrate HackerNews data collection"
```

**Changes:**
- HNクライアント初期化
- HNストーリー取得処理追加
- エラーハンドリング強化
- ログ出力追加

---

### 3. Renderer Updates

```bash
git add src/renderer.py
git commit -m "feat(renderer): add HackerNews section support"
```

**Changes:**
- HNストーリー表示機能追加
- JSON出力にHNデータ追加
- フォールバック処理対応

---

### 4. Template Updates

```bash
git add templates/readme_template.md.j2
git commit -m "feat(templates): add HackerNews section to readme"
```

**Changes:**
- Jinja2テンプレートに HN セクション追加
- 条件付き表示（HNデータがある場合のみ）

---

### 5. Documentation

```bash
git add .github/ISSUE_2_COMPLETE.md
git commit -m "docs: add HackerNews integration completion report"
```

**Changes:**
- 実装完了レポート
- API仕様書
- 使用例・テスト結果

---

## 🚀 Quick Commit All

一括コミットする場合:

```bash
git add src/hn_client.py src/main.py src/renderer.py templates/readme_template.md.j2 .github/ISSUE_2_COMPLETE.md

git commit -m "feat: implement HackerNews API integration (v0.4.0)

- Add HackerNews API client with retry logic
- Integrate HN stories into main pipeline  
- Update renderer to display HN section
- Add HN section to README template
- Include comprehensive documentation

Closes #2
"

git push origin master
```

---

## ✅ Post-Commit Checklist

コミット後に確認:

- [ ] コミットログを確認 (`git log --oneline -5`)
- [ ] リモートにプッシュ (`git push`)
- [ ] GitHubでコミット確認
- [ ] 動作テスト (`python src/main.py`)
- [ ] README.mdにHNセクションが表示されることを確認
- [ ] latest.jsonに `hn_stories` が含まれることを確認

---

## 🧪 Testing Commands

```bash
# 実行テスト
python src/main.py

# JSONデータ確認
cat data/latest.json | jq '.total_hn_stories'
cat data/latest.json | jq '.hn_stories[0]'

# README確認
grep -A 5 "HackerNews" README.md

# ファイルリスト確認
ls -l src/*.py
```

---

## 📊 Version Bump

`src/renderer.py` のバージョンを更新済み:
```python
"metadata": {
    "version": "0.4.0",  # ← Updated
    "sources": ["GitHub API", "HackerNews API"]
}
```

---

**Ready to commit! 🚀**
