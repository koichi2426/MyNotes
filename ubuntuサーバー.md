# Ubuntu サーバー

Ubuntu サーバーは、Canonical Ltd.によって開発された無料のオープンソースオペレーティングシステムです。企業レベルのサーバー、クラウド環境、または小規模なプロジェクト用のサーバーとして広く使用されています。

## 概要

### Ubuntu サーバーについて

Ubuntu サーバーは、Canonical Ltd.によって開発された無料のオープンソースオペレーティングシステムです。企業レベルのサーバー、クラウド環境、または小規模なプロジェクト用のサーバーとして広く使用されています。

### Ubuntu サーバーの主な特徴

1. **安定性と信頼性**：
    - Ubuntu サーバーは長期サポート（LTS）リリースを提供しており、通常5年間のセキュリティアップデートとメンテナンスアップデートを受けることができます。

2. **拡張性と柔軟性**：
    - オープンソースであるため、必要に応じてシステムをカスタマイズし、拡張することが可能です。

3. **多様なパッケージとツールのサポート**：
    - APTパッケージ管理システムを使用して、数千もの無料のソフトウェアパッケージを簡単にインストールできます。

4. **強力なセキュリティ**：
    - AppArmorやSELinuxのようなセキュリティフレームワークを利用して、システムとデータを保護します。

### Ubuntu サーバーの利点

- **コスト効率**：ライセンス費用が不要で、多くの無料のアップデートとサポートを利用できます。
- **広範なコミュニティサポート**：世界中の開発者とユーザーからの広範なサポートを受けることができます。
- **クラウドとの親和性**：AWS、Google Cloud Platform、Microsoft Azureなど、主要なクラウドプラットフォームで広く利用されています。

### Ubuntu サーバーの使用例

1. **ウェブサーバー**：
    - ApacheやNginxなどの人気のあるウェブサーバーソフトウェアを使用して、動的なウェブサイトやアプリケーションをホスティングします。

2. **データベースサーバー**：
    - MySQLやPostgreSQLなどのデータベース管理システムを運用し、大量のデータを効率的に管理します。

3. **ファイルサーバー**：
    - SambaやNFSを用いて、ファイルをネットワーク上で共有し、アクセス管理を行います。

4. **仮想化プラットフォーム**：
    - KVMやDockerを使用して、複数の仮想マシンやコンテナを実行します。

Ubuntu サーバーは、その多様性と柔軟性により、あらゆる規模のプロジェクトやビジネスニーズに適応する強力なサーバーオペレーティングシステムです。コスト効率の良さと高いカスタマイズ性で、多くのIT専門家に選ばれています。

## 基本操作

コマンドラインを通じた基本的なUbuntuサーバー操作をカバーしています。ディレクトリとファイル操作からプロセス管理、システム管理まで、効率的なシステム使用を支える重要なコマンドが含まれています。

### ディレクトリ操作系

1. **pwd (print working directory)**: 現在のディレクトリのフルパスを表示。

```bash
$ pwd
/home/kai
```

2. **dir**: カレントディレクトリの内容を表示。

```bash
$ dir
テンプレート ドキュメント ピクチャ 公開 ダウンロード デスクトップ ビデオ ミュージック test.txt
```

3. **cd (change directory)**: ディレクトリを移動。

```bash
$ cd デスクトップ
```

4. **mkdir (make directory)**: 新しいディレクトリを作成。

```bash
$ mkdir test
```

5. **rm (remove)**: ディレクトリやファイルを削除。

```bash
$ rm -rf test
```

### ファイル操作系

1. **touch**: 新規ファイルを作成。

```bash
$ touch test.txt
```

2. **cat (concatenate)**: ファイルの内容を表示。

```bash
$ cat test.txt
testだよ
```

3. **cp (copy)**: ファイルをコピー。

```bash
$ cp test.txt test2.txt
```

4. **mv (move)**: ファイルやディレクトリの名前を変更、または移動。

```bash
$ mv test.txt testtttt.txt
```

### プロセス管理系

1. **ps (process status)**: 現在実行中のプロセス一覧を表示。

```bash
$ ps
```

2. **kill**: 特定のプロセスを終了。

```bash
$ kill プロセスID
```

3. **jobs**: バックグラウンドで実行中のジョブを表示。

```bash
$ jobs
```

### システム管理系

1. **sudo**: スーパーユーザー権限でコマンドを実行。

```bash
$ sudo -s
```

2. **who**: ログイン中のユーザーを表示。

```bash
$ who
```

3. **whoami**: 現在ログインしているユーザー名を表示。

```bash
$ whoami
```

4. **hostname**: ホスト名を表示。

```bash
$ hostname
```

5. **shutdown / reboot**: システムをシャットダウンまたは再起動。

```bash
$ shutdown
$ reboot
```

## インストール集

### Git インストールと基本操作

[Gitインストールとgitの基本操作 - Qiita](https://qiita.com/studio_meowtoon/items/719e6765dd11f17a0b19)

### npm インストール

[npmインストール - Qiita](https://qiita.com/studio_meowtoon/items/111f556d8fb11a76430a)

#### npmインストール時の注意

この記事で紹介されているコマンド：

```bash
curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash -
```

を実行すると、スクリプト廃止予定の警告が表示されます。

```
================================================================================
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
================================================================================

                               SCRIPT DEPRECATION WARNING                    

  This script, located at https://deb.nodesource.com/setup_X, used to
  install Node.js is deprecated now and will eventually be made inactive.

  Please visit the NodeSource distributions Github and follow the
  instructions to migrate your repo.
  https://github.com/nodesource/distributions

  The NodeSource Node.js Linux distributions GitHub repository contains
  information about which versions of Node.js and which Linux distributions
  are supported and how to install it.
  https://github.com/nodesource/distributions

                                SCRIPT DEPRECATION WARNING

================================================================================
```

この場合は、最新の方法に従って [NodeSource distributions GitHub](https://github.com/nodesource/distributions) からインストールしてください。

### gem インストール

[Ruby のインストール（Ubuntu 上）](https://www.kkaneko.jp/tools/ubuntu/rubyinstalllinux.html)

### Ruby インストール

[Ubuntu で最新の Ruby をインストールする方法 - Qiita](https://qiita.com/kerupani129/items/77dd1e3390b53f4e97b2)

### Rails インストール

[Ubuntu Rails インストール](https://home-programming.com/2023/02/22/ubuntu_rails_install/)

#### Railsインストール時の注意

`gem install rails`を実行する際、以下のようなエラーが発生することがあります。

```
ERROR:  Error installing rails:
	ERROR: Failed to build gem native extension.
```

このエラーは、ビルドツールが不足していることが原因です。以下の手順で解決できます。

**1. ビルドツールのインストール**

```bash
sudo apt-get update
sudo apt-get install build-essential
```

**2. PATHの設定**

gemが正しく実行されるように、gemの実行可能ファイルのパスを環境変数PATHに追加します。

```bash
echo 'export PATH="$HOME/.local/share/gem/ruby/3.0.0/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**3. Railsの再インストール**

```bash
gem install rails
```

### Docker インストール

[DockerのUbuntuインストール方法](https://www.kagoya.jp/howto/cloud/container/dockerubuntu/)

#### Dockerの permission denied エラー

`permission denied` エラーは、Dockerデーモンへのアクセス権限が不足しているために発生します。

**1. Dockerグループにユーザーを追加**

```bash
sudo usermod -aG docker $USER
```

その後、システムからログアウトして再度ログインします。

**2. Dockerデーモンの権限を確認**

```bash
sudo chmod 666 /var/run/docker.sock
```

**3. Dockerデーモンが正しく動作しているか確認**

```bash
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker
```

**4. Dockerをsudoで実行**

急ぐ場合は、Dockerコマンドを `sudo` で実行することも一時的な解決策になります。

```bash
sudo docker compose up -d
```

## React アプリケーションのデプロイ

GitHubからプロジェクトをクローンし、Ubuntuサーバーでビルドしてデプロイする完全な手順です。

### 1. 必要なツールのインストール

サーバーにSSHでログイン後、GitとNode.js（npmを含む）をインストールします。

```bash
sudo apt update
sudo apt install git
sudo apt install nodejs npm
```

### 2. GitHubからプロジェクトのクローン

公開ディレクトリ（例えば `/var/www/html`）に移動し、GitHubからプロジェクトをクローンします。

```bash
cd /var/www/html
git clone https://github.com/ユーザー名/リポジトリ名.git
cd リポジトリ名
```

### 3. 依存関係のインストール

プロジェクトディレクトリ内で、npmを使って依存関係をインストールします。

```bash
npm install
```

### 4. アプリケーションのビルド

Reactプロジェクトの場合、本番用にビルドします。

```bash
npm run build
```

### 5. Web サーバーの設定

ApacheやNginxを設定して、ビルドしたアプリケーションを配信します。

**Apacheの設定例**：

```
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /var/www/html/リポジトリ名/build
    <Directory "/var/www/html/リポジトリ名/build">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

**Nginxの設定例**：

```
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /var/www/html/リポジトリ名/build;
        try_files $uri $uri/ /index.html;
    }
}
```

詳細は [Apache HTTP Server](Apache%20HTTP%20Server.md) を参照してください。

### 6. ドメイン名の設定

ドメイン名を持っている場合、DNS設定でドメインをサーバーのIPアドレスに向けます。

### 7. サーバーの再起動

設定変更を適用するために、Webサーバーを再起動します。

```bash
sudo systemctl restart apache2  # Apacheの場合
sudo systemctl restart nginx   # Nginxの場合
```

### 8. URLでのアクセス

以上の設定後、ブラウザで `http://yourdomain.com` （または設定したドメイン）を開くと、デプロイしたReactアプリケーションが表示されます。

## 自動デプロイ (GitHub Actions)

GitHub Actionsを使用して、masterブランチにマージされたタイミングでFTPを使って本番環境に自動デプロイする方法です。

### ステップ 1: 秘密情報をGitHubに追加

1. **GitHubリポジトリにアクセス** - リポジトリのトップページに移動します。

2. **「Settings」に移動** - リポジトリのトップページ右上にある「Settings」タブをクリックします。

3. **「Secrets and variables」セクションを見つける** - 左サイドバーの「Security」セクションにある「Secrets and variables」をクリックし、ドロップダウンメニューから「Actions」を選択します。

4. **「New repository secret」を追加** - 「Actions secrets」ページで、右上にある「New repository secret」ボタンをクリックします。

5. **FTP接続情報を追加** - 以下の3つのシークレットを追加します：

- **FTP_SERVER**
    - **Name**: `FTP_SERVER`
    - **Value**: (FTPサーバーのIPアドレス)

- **FTP_USERNAME**
    - **Name**: `FTP_USERNAME`
    - **Value**: (FTPユーザー名)

- **FTP_PASSWORD**
    - **Name**: `FTP_PASSWORD`
    - **Value**: (FTPパスワード)

### ステップ 2: GitHub Actions ワークフローの設定

GitHubリポジトリのルートディレクトリに `.github/workflows/deploy.yml` という名前でファイルを作成し、以下の内容を記述します。

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Upload files via FTP
      uses: SamKirkland/FTP-Deploy-Action@4.3.0
      with:
        server: ${{ secrets.FTP_SERVER }}
        username: ${{ secrets.FTP_USERNAME }}
        password: ${{ secrets.FTP_PASSWORD }}
        local-dir: .
        server-dir: /home/ksato
```

### 説明

- **`on.push.branches`**: masterブランチへのプッシュがトリガーになります。
- **`jobs.deploy.runs-on`**: ワークフローが `ubuntu-latest` の環境で実行されます。
- **`steps`**: ジョブ内のステップです。
    - `actions/checkout@v2` はリポジトリのコードをチェックアウトします。
    - `SamKirkland/FTP-Deploy-Action@4.3.0` を使用して、FTP経由でファイルをアップロードします。
    - `server`, `username`, `password` は先ほど設定した秘密情報を参照しています。
    - `local-dir` はアップロードするローカルディレクトリ（現在のリポジトリのルート）を指定します。
    - `server-dir` はFTPサーバー上のディレクトリを指定します。

この設定により、masterブランチにプッシュされた際に、自動的にFTPで本番環境にデプロイが行われます。

参考：[GitHub Actions FTPデプロイ - Qiita](https://qiita.com/sgrs38/items/9e3d548aea5e4d9b94ec)

## まとめ

Ubuntu サーバーは、その安定性、セキュリティ、柔軟性により、あらゆる規模のプロジェクトに適した選択肢です。上記の知識を活用することで、効率的なサーバー管理とアプリケーションデプロイが実現できます。
