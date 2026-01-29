# CircleCI

## 概要

### Continuous Integration（CI）とは

Continuous Integration（CI）は、ソフトウェア開発プロセスの一部として、コードの変更を頻繁に統合し、自動化されたビルドとテストを通じて継続的に検証するアプローチです。CIは、開発者間の協力を促進し、コードの品質を向上させるための重要な手法です。

#### CI の基本概念

CIの主な目的は、コードの変更がリポジトリにマージされるたびに自動的にビルドとテストを実行することです。これにより、コードの変更による問題を早期に発見し、迅速に修正することができます。

```
コード変更
    ↓
自動ビルド（Automated Build）
    ↓
自動テスト（Automated Testing）
    ↓
テスト結果通知
```

#### CI のステップ

| ステップ | 説明 |
|---------|------|
| **コミット** | 開発者がコード変更をリポジトリにコミット |
| **自動ビルド** | コミット検知で自動ビルド実行 |
| **自動テスト** | ビルド成功後、自動テストを実行 |
| **フィードバック** | テスト結果を開発者に通知 |

### CI の利点

| 利点 | 説明 |
|-----|------|
| **早期のバグ検出** | 小さな変更が頻繁にテストされるため、バグが即座に発見 |
| **コード品質向上** | 継続的なテストで品質を確保 |
| **統合リスク低減** | 小規模な変更を頻繁に統合で大規模統合を回避 |
| **チーム協力促進** | 開発者間の協力が強化される |
| **デプロイ準備** | 常に本番環境へ対応可能な状態を維持 |

### CI と CD の関係

```
CI（Continuous Integration）
↓ テスト済みコード
CD（Continuous Delivery）
↓ 本番環境対応
デプロイ可能な状態
```

**CI と CD の違い：**

| 特性 | CI | CD |
|-----|-----|------|
| **焦点** | テストの自動化 | デプロイの自動化 |
| **最終段階** | テスト完了 | 本番環境反映 |
| **対象範囲** | ビルド+テスト | ビルド+テスト+デプロイ |

### CircleCI の特徴

- **完全自動化**: ビルド、テスト、デプロイを完全自動化
- **スケーラブル**: 複数の言語・フレームワークに対応
- **高速**: 並列処理により高速なCI/CDパイプライン実現
- **セキュアな環境変数管理**: 機密情報の安全な管理
- **幅広いインテグレーション**: GitHub、GitLabなど多数のプラットフォームに対応

## Continuous Integration の詳細

### CI サーバーのコンポーネント

| コンポーネント | 説明 |
|-------------|------|
| **バージョン管理システム** | Git、SVN などでコード変更を管理 |
| **CI サーバー** | CircleCI、Jenkins、Travis CI などで自動実行 |
| **ビルドツール** | Maven、Gradle、npm などでビルド自動化 |
| **テストフレームワーク** | JUnit、RSpec、Jest などでテスト自動化 |

### CI パイプラインの例

```
1. コード変更をプッシュ
   ↓
2. CircleCI がポーリングで変更を検知
   ↓
3. リポジトリからコードをチェックアウト
   ↓
4. 依存関係をインストール（npm install など）
   ↓
5. コードをビルド（npm run build など）
   ↓
6. 静的解析を実行（ESLint など）
   ↓
7. ユニットテストを実行（Jest、JUnit など）
   ↓
8. 統合テストを実行
   ↓
9. テストレポートを生成
   ↓
10. 開発者にフィードバック通知
```

### CI ベストプラクティス

#### 1. 小さな変更を頻繁にコミット

```
✅ Good：小規模な変更を頻繁にコミット
- 1日に複数回のコミット
- 各コミット：機能単位で小分け
- 平均コミット：50-100行

❌ Bad：大規模な変更をたまにコミット
- 1週間に1回のコミット
- 数千行の変更が一度に統合
- マージ競合が多発
```

#### 2. テストを必ず含める

```
推奨テストカバレッジ：70-80%

テストの種類：
- ユニットテスト：関数・メソッド単位
- 統合テスト：複数モジュール連携
- 関数テスト：API・画面単位
- パフォーマンステスト：速度・負荷確認
```

#### 3. 高速なビルド・テスト

```
目標時間：
- ビルド時間：5-10 分以内
- テスト時間：10-15 分以内
- 全体パイプライン：20 分以内

最適化方法：
- 並列テスト実行
- キャッシング活用
- 不要なテストを削除
```

#### 4. 自動テストを中心に

```
テストピラミッド：

        △ E2E テスト（少量）
       /  \
      /    \
     /      \  統合テスト（中量）
    /        \
   /          \
  /____________\ ユニットテスト（多量）

理想的な比率：
- ユニットテスト：70%
- 統合テスト：20%
- E2E テスト：10%
```

## Continuous Delivery（CD）の基本概念

### CD パイプライン

Continuous Delivery は、コードの変更がリポジトリにマージされると、これらの変更が自動的にビルド、テスト、そしてデプロイされる一連のプロセスを指します。

```
コード変更
    ↓
ビルド（Build）
    ↓
テスト（Test）
    ↓
デプロイ（Deploy）
    ↓
本番環境反映
```

### 各ステップの説明

#### 1. ビルド（Build）

```
責務：
- ソースコードをコンパイル
- 実行可能なアーティファクトを生成
- 依存関係の解決

例：
- npm run build（React）
- maven build（Java）
- go build（Go）
```

#### 2. テスト（Test）

```
実施内容：
- 単体テスト（Unit Test）
- 統合テスト（Integration Test）
- UI テスト（E2E Test）
- パフォーマンステスト

目的：
- コード品質の保証
- バグの早期発見
- リグレッションの防止
```

#### 3. デプロイ（Deploy）

```
対象環境：
- Staging 環境（テスト環境）
- Production 環境（本番環境）

実装例：
- SSH での自動デプロイ
- Kubernetes ロールアウト
- Container レジストリへのプッシュ
```

## Continuous Delivery の利点

| 利点 | 説明 |
|-----|------|
| **迅速なリリースサイクル** | 新機能やバグ修正をすぐにユーザーに提供 |
| **高い品質** | 自動化されたテストで品質を保証 |
| **リリースリスク低減** | 小規模な変更を頻繁にデプロイしてリスク分散 |
| **開発者生産性向上** | 手動デプロイ作業を削減 |
| **ビジネス敏捷性** | 市場変化への素早い対応 |

## CircleCI セットアップ

### 前提条件

```
必要なもの：
- GitHub リポジトリ
- CircleCI アカウント（https://circleci.com/）
- デプロイ先サーバー（SSH アクセス可能）
- SSH キー
```

### Step 1: CircleCI プロジェクト設定

#### 1. CircleCI にログイン

- ウェブブラウザで CircleCI（https://circleci.com/）にアクセス
- GitHub アカウントでログイン

#### 2. プロジェクトを追加

- ダッシュボードから「Add Projects」をクリック
- GitHub リポジトリを選択して接続

#### 3. Project Settings に移動

- プロジェクト右上の「Project Settings」をクリック
- 「Advanced Settings」から「Auto-cancel redundant workflows」を有効化

### Step 2: SSH キーの設定

#### ローカルマシンで SSH キーを生成

```bash
# SSH キーを生成（既にある場合はスキップ）
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# デフォルトの保存場所で Enter キーを押す
# パスフレーズは設定しない場合は Enter キーを2回押す
```

#### Ubuntuサーバーに公開キーを追加

```bash
# ローカルマシンで実行
cat ~/.ssh/id_rsa.pub | ssh ubuntu@your.server.ip 'cat >> ~/.ssh/authorized_keys'

# パスワード入力を求められたらサーバーパスワードを入力
```

#### CircleCI に秘密鍵を追加

1. Project Settings → SSH Permissions に移動
2. 「Add SSH Key」をクリック
3. Hostname にサーバー IP アドレスを入力
4. Private Key に秘密キーの内容を貼り付け

秘密キーをコピーする方法：

```bash
# macOS
pbcopy < ~/.ssh/id_rsa

# Linux
xclip -sel clip < ~/.ssh/id_rsa
```

### Step 3: 環境変数の設定

Project Settings → Environment Variables で以下を追加：

```
USER=ubuntu
YOUR_SERVER_IP=your.server.ip
SUDO_PASSWORD=your_sudo_password
SSH_PASSWORD=your_ssh_password
```

**注意**: 機密情報は環境変数で管理し、コミットしないこと

## CircleCI 設定ファイル

### 基本的な config.yml

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: circleci/node:14
    steps:
      - checkout
      - run:
          name: Install Dependencies
          command: npm install
      - run:
          name: Build Project
          command: npm run build
      - run:
          name: Archive Build Artifacts
          command: tar -czf build.tar.gz build

  deploy:
    docker:
      - image: circleci/node:14
    steps:
      - add_ssh_keys:
          fingerprints:
            - "your-ssh-key-fingerprint"
      - run:
          name: Copy Build to Server
          command: scp build.tar.gz $USER@$YOUR_SERVER_IP:/home/ubuntu/project
      - run:
          name: Deploy on Server
          command: |
            ssh $USER@$YOUR_SERVER_IP << 'EOF'
              cd /home/ubuntu/project
              tar -xzf build.tar.gz
              echo $SUDO_PASSWORD | sudo -S cp -r build/* /var/www/html/
              echo $SUDO_PASSWORD | sudo -S systemctl restart apache2
            EOF

workflows:
  version: 2
  build_and_deploy:
    jobs:
      - build
      - deploy:
          requires:
            - build
          filters:
            branches:
              only: main
```

## React アプリケーション自動デプロイ

### シナリオ

GitHub の `main` ブランチへのプッシュ/マージで、CircleCI が自動的に React アプリケーションをビルドし、Ubuntu サーバーの Apache にデプロイ

### Step 1: CircleCI 設定ファイルの作成

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: circleci/node:14
    steps:
      - checkout
      - run:
          name: Install Dependencies
          command: npm install
      - run:
          name: Build Project
          command: npm run build
      - run:
          name: Archive Build Artifacts
          command: tar -czf build.tar.gz build

  deploy:
    docker:
      - image: circleci/node:14
    steps:
      - add_ssh_keys:
          fingerprints:
            - "your-ssh-key-fingerprint"
      - run:
          name: Copy Build to Server
          command: scp build.tar.gz $USER@$YOUR_SERVER_IP:/home/ubuntu/UI_pagespeedinsights
      - run:
          name: Extract and Deploy Build on Server
          command: |
            sshpass -p $SSH_PASSWORD ssh $USER@$YOUR_SERVER_IP << 'EOF'
              echo $SUDO_PASSWORD | sudo -S tar -xzf /home/ubuntu/UI_pagespeedinsights/build.tar.gz -C /home/ubuntu/UI_pagespeedinsights
              echo $SUDO_PASSWORD | sudo -S cp -r /home/ubuntu/UI_pagespeedinsights/build/* /var/www/html/
              
              # .htaccess 設定
              echo '<IfModule mod_rewrite.c>
                      RewriteEngine On
                      RewriteBase /
                      RewriteRule ^index\.html$ - [L]
                      RewriteCond %{REQUEST_FILENAME} !-f
                      RewriteCond %{REQUEST_FILENAME} !-d
                      RewriteRule . /index.html [L]
                    </IfModule>' | sudo tee /var/www/html/.htaccess
              
              # mod_rewrite を有効化
              echo $SUDO_PASSWORD | sudo -S a2enmod rewrite
              
              # Apache 再起動
              echo $SUDO_PASSWORD | sudo -S systemctl restart apache2
            EOF

workflows:
  version: 2
  build_and_deploy:
    jobs:
      - build
      - deploy:
          requires:
            - build
          filters:
            branches:
              only: main
```

## サーバーでの自動 git pull

### シナリオ

CircleCI が SSH 接続してサーバー上で `git pull` を実行し、最新コードを自動取得

### 前提条件

サーバー上に `.env` ファイルを作成：

```bash
# /home/ubuntu/project/.env
GITHUB_USER=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=username/repository
SUDO_PASSWORD=your_sudo_password
```

### config.yml（git pull パターン）

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: circleci/node:14
    steps:
      - checkout
      - run:
          name: Install Dependencies
          command: npm install
      - add_ssh_keys:
          fingerprints:
            - "your-ssh-key-fingerprint"
      - run:
          name: SSH Connection and Git Pull
          command: |
            ssh -o StrictHostKeyChecking=no ${USER}@${YOUR_SERVER_IP} << 'EOF'
              echo "Connected to server"
              cd /home/ubuntu/UI_pagespeedinsights
              pwd
              
              # .env ファイルから環境変数を読み込む
              if [ -f .env ]; then
                export $(grep -v '^#' .env | xargs)
              fi
              
              # Git 認証情報を設定
              git config --global credential.helper store
              echo "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
              
              # 最新のコードをプル
              git pull https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git
              echo "Git pull completed"
            EOF

workflows:
  version: 2
  build_and_ssh:
    jobs:
      - build
```

## サーバーでの React ビルド実行

### config.yml（ビルド実行パターン）

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: circleci/node:14
    steps:
      - checkout
      - run:
          name: Install Dependencies
          command: npm install
      - add_ssh_keys:
          fingerprints:
            - "your-ssh-key-fingerprint"
      - run:
          name: SSH and Build on Server
          command: |
            ssh -o StrictHostKeyChecking=no ${USER}@${YOUR_SERVER_IP} << 'EOF'
              echo "Connected to server"
              cd /home/ubuntu/UI_pagespeedinsights
              pwd
              
              # .env ファイルから環境変数を読み込む
              if [ -f .env ]; then
                export $(grep -v '^#' .env | xargs)
              fi
              
              # Git 認証情報を設定
              git config --global credential.helper store
              echo "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
              
              # 最新のコードをプル
              git pull https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git
              echo "Git pull completed"
              
              # 依存関係をインストール
              echo ${SUDO_PASSWORD} | sudo -S npm install
              echo "Dependencies installed"
              
              # React をビルド
              echo ${SUDO_PASSWORD} | sudo -S npm run build
              echo "Build completed"
              
              # ビルド成果物をコピー
              cd /home/ubuntu/UI_pagespeedinsights/build
              echo ${SUDO_PASSWORD} | sudo -S bash -c 'cp -r * /var/www/html/'
              echo "Build artifacts copied"
            EOF

workflows:
  version: 2
  build_and_ssh:
    jobs:
      - build
```

## 実践的な設定例

### 完全な自動デプロイ設定

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: circleci/node:14
    steps:
      - checkout
      - run:
          name: Install Dependencies
          command: npm install
      - add_ssh_keys:
          fingerprints:
            - "your-ssh-key-fingerprint"
      - run:
          name: Full Deployment Process
          command: |
            ssh -o StrictHostKeyChecking=no ${USER}@${YOUR_SERVER_IP} << 'EOF'
              echo "=== Connected to server ==="
              cd /home/ubuntu/UI_pagespeedinsights
              pwd
              
              # .env ファイルから環境変数を読み込む
              if [ -f .env ]; then
                export $(grep -v '^#' .env | xargs)
              fi
              
              # Git プル
              git config --global credential.helper store
              echo "https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
              git pull https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git
              echo "=== Git pull completed ==="
              
              # npm インストール
              echo ${SUDO_PASSWORD} | sudo -S npm install
              echo "=== Dependencies installed ==="
              
              # React ビルド
              echo ${SUDO_PASSWORD} | sudo -S npm run build
              echo "=== Build completed ==="
              
              # ビルド成果物をコピー
              cd /home/ubuntu/UI_pagespeedinsights/build
              echo ${SUDO_PASSWORD} | sudo -S cp -r * /var/www/html/
              echo "=== Build artifacts copied ==="
              
              # .htaccess 設定
              echo ${SUDO_PASSWORD} | sudo -S bash -c 'cat > /var/www/html/.htaccess << "HTACCESS"'
              echo '<IfModule mod_rewrite.c>'
              echo '    RewriteEngine On'
              echo '    RewriteBase /'
              echo '    RewriteRule ^index\.html$ - [L]'
              echo '    RewriteCond %{REQUEST_FILENAME} !-f'
              echo '    RewriteCond %{REQUEST_FILENAME} !-d'
              echo '    RewriteRule . /index.html [L]'
              echo '</IfModule>'
              echo 'HTACCESS'
              
              # Apache 再起動
              echo ${SUDO_PASSWORD} | sudo -S systemctl restart apache2
              echo "=== Apache restarted ==="
              echo "=== Deployment completed successfully ==="
            EOF

workflows:
  version: 2
  continuous_deployment:
    jobs:
      - build:
          filters:
            branches:
              only: main
```

## トラブルシューティング

### SSH 接続エラー

```
エラー：
ssh: connect to host aa.bb.cc.dd port 22: Connection refused

原因：
- サーバーが起動していない
- SSH ポートが開いていない
- IP アドレスが間違っている

対処：
1. サーバーが起動しているか確認
2. ファイアウォール設定を確認
3. IP アドレスを再確認
```

### 認証エラー

```
エラー：
Permission denied (publickey,gssapi-keyex,gssapi-with-mic)

原因：
- SSH キーが正しく登録されていない
- .authorized_keys ファイルの権限が不正

対処：
1. SSH キーを再度確認
2. ~/.ssh/authorized_keys の権限を確認
   chmod 600 ~/.ssh/authorized_keys
3. CircleCI のSSH キー設定を確認
```

### 環境変数が読み込まれない

```
原因：
- .env ファイルが存在しない
- .env ファイルのパス指定が間違っている
- export コマンドの形式が不正

対処：
ssh 内で確認
if [ -f .env ]; then
  echo ".env found"
  cat .env
else
  echo ".env not found"
fi
```

### sudo パスワード関連エラー

```
エラー：
sudo: sorry, you must have a tty to run sudo

原因：
- SSH セッションが TTY を持っていない

対処：
ssh -tt オプションを使用
ssh -tt -o StrictHostKeyChecking=no ${USER}@${YOUR_SERVER_IP} << 'EOF'
```

### git pull エラー

```
エラー：
fatal: could not read Username for 'https://github.com'

原因：
- GitHub 認証情報が設定されていない
- GITHUB_TOKEN が無効

対処：
1. GitHub Personal Access Token を確認
2. ~/.git-credentials が正しく設定されているか確認
3. git config を確認
```

## ベストプラクティス

### 1. 環境変数の管理

```yaml
# ✅ Good：環境変数で機密情報を管理
environment:
  GITHUB_TOKEN: $GITHUB_TOKEN
  SUDO_PASSWORD: $SUDO_PASSWORD

# ❌ Bad：config.yml にパスワードを記述
command: sshpass -p password ssh user@host
```

### 2. エラーハンドリング

```bash
#!/bin/bash
set -e  # エラーで停止
set -u  # 未定義変数でエラー

# コマンド実行
if ! npm install; then
  echo "npm install failed"
  exit 1
fi

echo "Success"
```

### 3. ログ出力

```bash
# ✅ Good：進捗をログ出力
echo "=== Step 1: Connect to server ==="
echo "=== Step 2: Git pull ==="
echo "=== Step 3: Build ==="

# ❌ Bad：ログなし
```

### 4. Workflow の並列実行

```yaml
workflows:
  version: 2
  build_and_test:
    jobs:
      - build
      - test_unit
      - test_integration
      - deploy:
          requires:
            - build
            - test_unit
            - test_integration
          filters:
            branches:
              only: main
```

### 5. キャッシング（高速化）

```yaml
jobs:
  build:
    docker:
      - image: circleci/node:14
    steps:
      - checkout
      - restore_cache:
          keys:
            - v1-dependencies-{{ checksum "package-lock.json" }}
      - run:
          name: Install Dependencies
          command: npm install
      - save_cache:
          paths:
            - node_modules
          key: v1-dependencies-{{ checksum "package-lock.json" }}
```

## まとめ

CircleCI は、**完全自動化された CI/CD パイプラインを実現するツール**です。

**重要なポイント：**
- SSH キーと環境変数で安全に設定
- config.yml で全てのプロセスを定義
- ワークフローで複数ジョブの連携
- ログで進捗と問題を追跡
- エラーハンドリングで堅牢性を確保

適切に設定すれば、開発者がコードをプッシュするだけで、自動的にテスト、ビルド、デプロイまで実行できます。
