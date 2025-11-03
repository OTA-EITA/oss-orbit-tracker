# 📝 Git Commit Guide

このドキュメントは、今回作成したすべてのファイルのコミット手順を示します。

---

## 🎯 Commit Strategy

**原則**: 1ファイル1コミット、簡潔なメッセージ

---

## 📋 Commit Sequence

### 1. Documentation Files

```bash
# Project Rules
git add docs/project_rules.md
git commit -m "docs: add project rules"

# Architecture Document
git add docs/architecture.md
git commit -m "docs: add architecture design"

# Contributing Guide
git add CONTRIBUTING.md
git commit -m "docs: add contributing guidelines"

# Security Policy
git add SECURITY.md
git commit -m "docs: add security policy"

# Implementation Summary
git add IMPLEMENTATION_SUMMARY.md
git commit -m "docs: add implementation summary"

# README Template
git add README_TEMPLATE.md
git commit -m "docs: add comprehensive readme template"

# Roadmap
git add .github/ROADMAP.md
git commit -m "docs: add development roadmap"
```

### 2. Configuration Files

```bash
# Environment Template
git add .env.example
git commit -m "chore: add environment template"

# Dependencies
git add requirements.txt
git commit -m "chore: add jinja2 dependency"
```

### 3. Templates

```bash
# Jinja2 README Template
git add templates/readme_template.md.j2
git commit -m "feat(templates): add jinja2 readme template"
```

### 4. Core Source Code

```bash
# Main Script (Refactored)
git add src/main.py
git commit -m "refactor(main): add logging and error handling"

# GitHub Client (Enhanced)
git add src/github_client.py
git commit -m "refactor(client): add retry logic and logging"

# Analyzer (Improved)
git add src/analyzer.py
git commit -m "refactor(analyzer): add type hints and validation"

# Renderer (Jinja2 Support)
git add src/renderer.py
git commit -m "feat(renderer): add jinja2 template support"
```

### 5. Scripts

```bash
# Data Cleanup Script
git add scripts/cleanup.py
git commit -m "feat(scripts): add data cleanup script"
```

### 6. GitHub Actions Workflows

```bash
# Daily Update Workflow (Updated)
git add .github/workflows/daily-update.yml
git commit -m "feat(workflow): add cleanup step to daily update"

# Weekly Cleanup Workflow (New)
git add .github/workflows/weekly-cleanup.yml
git commit -m "feat(workflow): add weekly cleanup workflow"
```

---

## 🚀 Quick Commit All (Alternative)

もし一括でコミットしたい場合:

```bash
# Stage all new/modified files
git add .

# Commit with comprehensive message
git commit -m "feat: implement v0.3 with logging, cleanup, and docs

- Add comprehensive documentation (project rules, architecture, contributing, security)
- Refactor all source files with logging and error handling
- Add Jinja2 template support for README generation
- Implement data cleanup script with retention policy
- Enhance GitHub Actions workflows with cleanup steps
- Add .env.example for environment configuration
- Complete type hints and validation
- Add development roadmap and implementation summary

Closes #1 (latest.json generation)
Closes #4 (data cleanup)
"

# Push to remote
git push origin master
```

---

## ✅ Verification

コミット後に確認:

```bash
# Check git status
git status

# View commit log
git log --oneline -n 20

# Check remote
git remote -v

# Push if not done
git push origin master
```

---

## 📊 Commit Statistics

| Category | Files | Commits |
|----------|-------|---------|
| **Documentation** | 7 | 7 |
| **Configuration** | 2 | 2 |
| **Templates** | 1 | 1 |
| **Source Code** | 4 | 4 |
| **Scripts** | 1 | 1 |
| **Workflows** | 2 | 2 |
| **TOTAL** | **17** | **17** |

---

## 🎨 Commit Message Format

すべてのコミットは以下の形式に従います:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types Used

- `feat`: 新機能
- `refactor`: リファクタリング
- `docs`: ドキュメント
- `chore`: 雑務

### Examples

```bash
# Good
git commit -m "feat(renderer): add jinja2 template support"
git commit -m "docs: add project rules"
git commit -m "refactor(client): add retry logic and logging"

# Bad (避けるべき)
git commit -m "update files"
git commit -m "fix"
git commit -m "WIP"
```

---

## 🚦 Pre-Push Checklist

Push前に確認:

- [ ] すべてのファイルがコミットされている
- [ ] コミットメッセージが適切
- [ ] .envファイルがgitignoreされている
- [ ] requirements.txtが最新
- [ ] README.mdが自動生成される設定になっている

---

## 🔄 Post-Push Actions

Push後に:

1. GitHub Actionsが正常に動作することを確認
2. READMEが正しく表示されることを確認
3. データファイルが生成されることを確認

---

**Happy Committing! 🎉**
