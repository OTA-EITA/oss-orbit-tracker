# 🔒 Security Policy

## サポートされているバージョン

現在サポートされているバージョンとセキュリティアップデートの提供状況:

| Version | Supported          |
| ------- | ------------------ |
| 0.3.x   | :white_check_mark: |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

---

## 🚨 脆弱性の報告

セキュリティ上の問題を発見した場合は、**公開Issueではなく**以下の方法で報告してください:

### 報告方法

1. **GitHub Security Advisory**を使用（推奨）
   - リポジトリの "Security" タブ → "Report a vulnerability"

2. **メール報告**
   - 件名: `[SECURITY] OSS Orbit Tracker - <簡単な説明>`
   - 内容: 詳細な脆弱性情報

### 報告に含めるべき情報

- 脆弱性の種類（例: XSS, SQLインジェクション, 認証バイパス等）
- 影響範囲と深刻度
- 再現手順
- 可能であればPoC（概念実証）コード
- 提案される修正方法（あれば）

---

## ⏱️ 対応タイムライン

| フェーズ | 期間 | 内容 |
|---------|------|------|
| **受領確認** | 24時間以内 | 報告を受け取った旨を通知 |
| **初期評価** | 3日以内 | 脆弱性の評価と優先度決定 |
| **修正開発** | 14日以内 | パッチの開発とテスト |
| **リリース** | 21日以内 | 修正版のリリース |
| **公開** | 30日後 | 詳細を公開（報告者と協議） |

---

## 🛡️ セキュリティベストプラクティス

### 1. トークン管理

```bash
# ❌ 絶対にしないこと
GH_TOKEN=ghp_xxxxx python src/main.py

# ✅ 正しい方法
export GH_TOKEN=ghp_xxxxx
python src/main.py

# または .env ファイル使用
echo "GH_TOKEN=ghp_xxxxx" > .env
python src/main.py
```

### 2. 環境変数の保護

```python
# ✅ 環境変数から読み込み
import os
token = os.getenv("GH_TOKEN")

# ❌ ハードコードは絶対NG
token = "ghp_xxxxxxxxxxxxx"
```

### 3. ログ出力の注意

```python
# ❌ トークンをログに出力
logger.info(f"Using token: {token}")

# ✅ マスキングして出力
logger.info(f"Using token: {token[:8]}***")
```

---

## 🔍 既知の脆弱性

現在、報告されている既知の脆弱性はありません。

### 過去の脆弱性

なし

---

## 🚫 スコープ外の問題

以下は脆弱性とは見なされません:

- GitHub API自体の問題
- サードパーティライブラリの既知の問題（最新版を使用している場合）
- ソーシャルエンジニアリング
- 物理的なアクセスによる攻撃
- DDoS攻撃

---

## 📝 セキュリティチェックリスト

開発者向けのセキュリティチェックリスト:

- [ ] 認証情報は環境変数で管理
- [ ] ログに機密情報を出力しない
- [ ] 外部入力は常にバリデーション
- [ ] Rate Limitを遵守
- [ ] 依存関係は定期的に更新
- [ ] `.gitignore`に`.env`を追加
- [ ] GitHub Secretsで機密情報を管理

---

## 🏆 セキュリティ研究者への謝辞

責任ある開示をしてくださったセキュリティ研究者の方々:

<!-- セキュリティ報告者リストがここに表示されます -->
_現在、謝辞はありません_

---

## 📚 参考資料

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

**セキュリティは全員の責任です。ご協力ありがとうございます! 🛡️**
