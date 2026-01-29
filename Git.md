# Git - バージョン管理システム

分散型バージョン管理システム Git の使い方と実践的な手順

## Git とは

Git は、ソースコードの変更履歴を管理する分散型バージョン管理システムです。

### 基本概念

```
【ローカルリポジトリ】
あなたのパソコン上で管理
├─ Working Directory（作業ディレクトリ）
├─ Staging Area（ステージング領域）
└─ .git（リポジトリ）

【リモートリポジトリ】
GitHub などのサーバー上で管理
├─ origin/main
├─ origin/develop
└─ その他ブランチ
```

## すでに存在するローカルプロジェクトをリモートリポジトリに反映する

このセクションでは、ローカルで開発したプロジェクトを初めてリモートリポジトリに push する手順を説明します。

### ステップ1：GitHub でリモートリポジトリを作成

```
1. GitHub にログイン（https://github.com）
2. 右上の「+」ボタン → 「New repository」をクリック
3. リポジトリ名を入力
   例：my-project
4. 説明を入力（オプション）
5. 「Public」または「Private」を選択
6. 「README を作成」はチェック不要（ローカルからプッシュするため）
7. 「Create repository」をクリック
```

**重要：** README、.gitignore、LICENSE は作成しないでください。
ローカルで既に作成されている可能性があり、競合の原因になります。

### ステップ2：ローカルディレクトリで git 初期化

```bash
# プロジェクトディレクトリに移動
cd /path/to/your/project

# git を初期化
git init

# ローカルで作業するユーザー情報を設定（初回のみ）
git config user.name "Your Name"
git config user.email "your-email@example.com"

# グローバル設定の場合（全プロジェクト対象）
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### ステップ3：ローカルファイルを git に追加

```bash
# ディレクトリの内容確認
ls -la

# 全ファイルをステージングエリアに追加
git add .

# 特定ファイルのみを追加する場合
git add src/
git add README.md

# ステージングされたファイルを確認
git status
```

**出力例：**
```
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
        new file:   src/app.js
        new file:   package.json
```

### ステップ4：コミットを作成

```bash
# 最初のコミットを作成
git commit -m "Initial commit"

# より詳細なメッセージの場合
git commit -m "Initial commit: Add project structure

- Create main application files
- Set up package.json
- Add documentation"
```

**確認：**
```bash
# コミット履歴を確認
git log

# 出力例：
# commit abc1234567890def... (HEAD -> master)
# Author: Your Name <your-email@example.com>
# Date:   Wed Jan 29 10:00:00 2026 +0900
#
#     Initial commit
```

### ステップ5：リモートリポジトリを追加

```bash
# GitHub でリポジトリ作成後、表示される URL をコピー
# 例：https://github.com/username/my-project.git

# リモートを追加
git remote add origin https://github.com/username/my-project.git

# SSH を使用する場合
git remote add origin git@github.com:username/my-project.git

# 設定を確認
git remote -v

# 出力例：
# origin  https://github.com/username/my-project.git (fetch)
# origin  https://github.com/username/my-project.git (push)
```

### ステップ6：リモートリポジトリに push

```bash
# main ブランチに push（GitHub のデフォルトブランチ）
git push -u origin main

# または master の場合
git push -u origin master

# パスワード認証の場合：GitHub でログイン情報を入力
# トークン認証の場合：GitHub Personal Access Token を入力
```

**初回 push 時の注意：**

```
GitHub がローカルブランチ名（master か main）を
リモートブランチ名と一致させるよう指示する場合：

# ブランチ名を確認
git branch

# main が存在しない場合は作成・切り替え
git checkout -b main

# その後 push
git push -u origin main
```

### ステップ7：確認

```bash
# push 確認
git status

# 出力例：
# On branch main
# Your branch is up to date with 'origin/main'.

# ローカルとリモートのブランチを確認
git branch -a

# 出力例：
#   master
# * main
#   remotes/origin/main
```

GitHub にアクセスして、ファイルが反映されているか確認します。

---

## 実際の操作流れ（フルコマンド例）

```bash
# 1. プロジェクトディレクトリに移動
cd ~/my-project

# 2. git 初期化
git init

# 3. ユーザー設定
git config user.name "John Doe"
git config user.email "john@example.com"

# 4. ファイルを追加
git add .

# 5. 状態確認
git status

# 6. コミット
git commit -m "Initial commit"

# 7. リモート追加
git remote add origin https://github.com/johndoe/my-project.git

# 8. push
git push -u origin main

# 完了！
```

---

## よくあるトラブルと対応

### 問題1：「fatal: not a git repository」エラー

**原因：** `git init` していない

**解決策：**
```bash
git init
```

### 問題2：「fatal: No configured push destination」エラー

**原因：** リモートリポジトリが設定されていない

**解決策：**
```bash
git remote add origin <リポジトリ URL>
```

### 問題3：「error: src refspec main does not match any」エラー

**原因：** main ブランチが存在しない、または コミットがない

**解決策：**
```bash
# ブランチを確認
git branch

# コミットが存在するか確認
git log

# ない場合は作成・コミット
git checkout -b main
git add .
git commit -m "Initial commit"
```

### 問題4：リモートが master だが、ローカルが main の場合

**原因：** GitHub のデフォルトブランチ設定とローカルの不一致

**解決策：**
```bash
# ローカルブランチを確認
git branch

# master に切り替え
git checkout master

# master をデフォルトに push
git push -u origin master

# または、GitHub の設定を main に変更
# （GitHub → Settings → Branches → Default branch を main に）
```

### 問題5：「Authentication failed」エラー

**原因：** パスワード認証が無効、または HTTPS URL の認証情報が間違っている

**解決策：**

#### HTTPS の場合（Personal Access Token を使用）

```bash
# GitHub → Settings → Developer settings → Personal access tokens
# で Fine-grained token を作成

# リモート URL を再設定
git remote set-url origin https://github.com/username/my-project.git

# push 時にトークンを入力
git push -u origin main

# キャッシュに保存する場合
git config --global credential.helper store
```

#### SSH の場合

```bash
# SSH キーを生成（初回のみ）
ssh-keygen -t ed25519 -C "your-email@example.com"

# 公開鍵を GitHub に登録
# GitHub → Settings → SSH and GPG keys → New SSH key

# リモート URL を SSH に変更
git remote set-url origin git@github.com:username/my-project.git

# push
git push -u origin main
```

---

## Git の基本コマンド

### リポジトリ管理

```bash
# 新しいリポジトリを初期化
git init

# 既存のリモートリポジトリをクローン
git clone https://github.com/username/repo.git

# リモートリポジトリを設定
git remote add origin <URL>
git remote set-url origin <新しい URL>
git remote -v  # リモートを確認
git remote remove origin  # リモートを削除
```

### ブランチ管理

```bash
# ブランチ一覧を表示
git branch  # ローカル
git branch -a  # ローカル + リモート

# ブランチを作成
git branch feature/new-feature

# ブランチを切り替え
git checkout feature/new-feature

# ブランチを作成 + 切り替え
git checkout -b feature/new-feature

# ブランチ名を変更
git branch -m old-name new-name

# ブランチを削除
git branch -d feature/old-feature
git branch -D feature/old-feature  # 強制削除
```

### 変更の管理

```bash
# 変更を確認
git status  # 状態確認
git diff  # 変更内容確認（未ステージング）
git diff --staged  # ステージング済みの変更確認

# ファイルをステージング
git add <file>  # 特定ファイル
git add .  # 全ファイル
git add *.js  # パターンマッチ

# ステージングを取り消す
git reset <file>
git reset HEAD

# コミット
git commit -m "メッセージ"
git commit -am "メッセージ"  # add + commit（トラッキングされたファイルのみ）
git commit --amend  # 直前のコミットを修正

# 変更を破棄
git restore <file>  # 最後のコミット状態に戻す
git clean -fd  # 未トラッキングファイルを削除
```

### リモートとの同期

```bash
# リモートから最新を取得（マージなし）
git fetch origin

# リモートから最新を取得 + マージ
git pull origin main

# ローカルをリモートにアップロード
git push origin main

# ローカルブランチを追跡設定して push
git push -u origin feature/new-feature

# リモートブランチを削除
git push origin --delete feature/old-feature

# 全ブランチをプッシュ
git push origin --all
```

### 履歴管理

```bash
# コミット履歴を表示
git log  # 詳細表示
git log --oneline  # 1行表示
git log --graph --oneline --all  # グラフ表示

# 特定ファイルの変更履歴
git log <file>

# 差分を含めて表示
git log -p

# 特定コミットの詳細を表示
git show <commit-hash>

# 過去の状態に戻す
git reset --hard <commit-hash>  # コミット以降の全変更を破棄
git revert <commit-hash>  # コミットを打ち消すコミットを作成
git checkout <commit-hash> -- <file>  # 特定ファイルを復元
```

### マージと rebase

```bash
# ブランチをマージ
git checkout main
git merge feature/new-feature

# マージをキャンセル
git merge --abort

# リベース（履歴を整理）
git rebase main

# リベースをキャンセル
git rebase --abort
```

---

## .gitignore ファイル

リポジトリに含めたくないファイルを指定します。

```
# Node.js
node_modules/
npm-debug.log
package-lock.json

# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 環境変数
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# ビルド出力
dist/
build/
out/
```

---

## 実践的なワークフロー

### シングル開発者のフロー

```
1. main ブランチで開発
2. 作業 → コミット → push

# または

1. feature ブランチを作成
2. 作業 → コミット
3. main にマージ
4. push

コマンド例：
git checkout -b feature/login
# 作業...
git add .
git commit -m "Add login feature"
git checkout main
git merge feature/login
git push origin main
```

### チーム開発のフロー（Git Flow）

```
main（本番環境）
├─ develop（開発用）
│  ├─ feature/user-auth（機能開発）
│  ├─ feature/dashboard（機能開発）
│  └─ bugfix/login-error（バグ修正）
│
└─ release/1.0.0（リリース準備）
```

---

## GitHub の操作

### リモートリポジトリの確認

```
GitHub にアクセス → リポジトリ → Code タブ
├─ ファイル一覧
├─ コミット履歴
└─ ブランチ
```

### Pull Request（PR）

```bash
# ローカルで作業
git checkout -b feature/new-feature
# 作業...
git push -u origin feature/new-feature

# GitHub で PR を作成
# → Create pull request をクリック
# → タイトル・説明を入力
# → Create pull request をクリック

# レビュー → マージ
```

---

## ベストプラクティス

```
✅ すべきこと

① こまめにコミット
   └─ 1コミット = 1つの意味のある変更

② 明確なコミットメッセージ
   └─ 「何をしたか」を簡潔に

③ 変更前に pull
   └─ 最新の状態を保つ

④ .gitignore を活用
   └─ 不要なファイルをリポジトリに含めない

⑤ ブランチを使い分ける
   └─ main は常に動作状態を保つ

❌ してはいけないこと

① credentials（パスワード、API キー）をコミット
   └─ リポジトリに含めない

② 大きなバイナリファイル
   └─ Git LFS を使用

③ 不適切なマージやリベース
   └─ 履歴が混乱

④ 強制プッシュ
   └─ チーム開発では特に禁止
   git push --force は慎重に
```

---

## 関連トピック

- [[VersionControl]]：バージョン管理全般
- [[GitHubDesktop]]：GUI クライアント
- [[DevelopmentProcesses]]：開発プロセス
