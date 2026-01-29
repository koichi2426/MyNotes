# Docker

Dockerは、アプリケーションの開発、デプロイ、実行を容易にするオープンソースのコンテナ化プラットフォームです。コンテナは、ソフトウェアの動作に必要なすべてのもの（コード、ライブラリ、設定ファイルなど）をまとめてパッケージ化することで、一貫した環境で動作させることができます。

## 概要

### Dockerとは？

Dockerは、アプリケーションの開発、デプロイ、実行を容易にするオープンソースのコンテナ化プラットフォームです。コンテナは、ソフトウェアの動作に必要なすべてのもの（コード、ライブラリ、設定ファイルなど）をまとめてパッケージ化することで、一貫した環境で動作させることができます。

### Dockerの主な利点

- **軽量性**：コンテナは仮想マシンよりも軽量で、高速に起動します。
- **一貫性**：開発環境と本番環境の差異をなくし、「動くはずの環境で動かない」問題を解消します。
- **移植性**：どこでも同じコンテナが動作するため、アプリケーションの移植性が向上します。
- **効率性**：システムリソースを効率的に利用でき、複数のコンテナを同時に実行できます。

### Dockerの基本概念

- **イメージ (Image)**：コンテナの実行に必要な設定やアプリケーションを含んだ静的なテンプレート。
- **コンテナ (Container)**：イメージの実行可能なインスタンス。
- **Dockerfile**：イメージを作成するための設定ファイル。
- **Docker Hub**：Dockerイメージの共有と管理を行うためのリポジトリ。

### Dockerのインストール

Dockerは、主要なオペレーティングシステム（Linux、Windows、macOS）で利用可能です。以下は、UbuntuにDockerをインストールする手順です。

```bash
# 古いバージョンのDockerをアンインストール
sudo apt-get remove docker docker-engine docker.io containerd runc

# 必要なパッケージをインストール
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

# Dockerの公式GPGキーを追加
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Dockerリポジトリを追加
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Dockerエンジンをインストール
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Dockerが正しくインストールされたか確認
sudo docker run hello-world
```

### 基本コマンド

#### イメージの取得

```bash
docker pull イメージ名
# 例: docker pull ubuntu
```

#### コンテナの実行

```bash
docker run -it イメージ名
# 例: docker run -it ubuntu
```

#### 実行中のコンテナを一覧表示

```bash
docker ps
```

#### 停止中のコンテナを含むすべてのコンテナを一覧表示

```bash
docker ps -a
```

#### コンテナの停止

```bash
docker stop コンテナID
```

#### コンテナの削除

```bash
docker rm コンテナID
```

#### イメージの削除

```bash
docker rmi イメージ名
```

### Dockerfileの作成

Dockerfileを使用してカスタムイメージを作成できます。以下は、シンプルなDockerfileの例です。

```dockerfile
# ベースイメージを指定
FROM ubuntu:latest

# メンテナー情報を指定
LABEL maintainer="yourname@example.com"

# パッケージをインストール
RUN apt-get update && apt-get install -y nginx

# コンテナ起動時に実行するコマンドを指定
CMD ["nginx", "-g", "daemon off;"]
```

#### イメージのビルド

```bash
docker build -t イメージ名:タグ .
# 例: docker build -t mynginx:latest .
```

### Docker Composeの利用

Docker Composeを使用すると、複数のコンテナを定義して一括で管理できます。以下は、シンプルな`docker-compose.yml`の例です。

```yaml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "80:80"
  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: example
```

#### Composeファイルの実行

```bash
docker-compose up -d
```

### トラブルシューティング

#### Dockerデーモンへのアクセス権限

エラーメッセージ `permission denied while trying to connect to the Docker daemon socket` が表示された場合、ユーザーが `docker` グループに所属しているか確認し、所属していなければ追加します。

```bash
sudo usermod -aG docker $USER
```

その後、システムからログアウトして再度ログインします。

## 基本操作

### Docker全コマンド集とその解説

Dockerには多くのコマンドがあり、イメージの操作、コンテナの操作、ネットワークの設定など、さまざまな機能を提供します。

### 1. 基本的なDockerコマンド

#### `docker --version`

**説明**: Dockerのバージョンを表示します。

**コマンド:**

```bash
docker --version
```

**出力例:**

```
Docker version 20.10.7, build f0df350
```

**意味**: インストールされているDockerのバージョンが20.10.7であることを示します。

### 2. イメージ関連のコマンド

#### `docker images`

**説明**: ローカルに存在するDockerイメージの一覧を表示します。

**コマンド:**

```bash
docker images
```

**出力例:**

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              2d696327ab2e        2 days ago          73.9MB
nginx               latest              7e4d58f0e5f3        3 days ago          133MB
```

**意味**: ローカルに存在する `ubuntu` と `nginx` イメージの詳細情報（タグ、イメージID、作成日時、サイズ）を示します。

#### `docker pull`

**説明**: Docker Hubなどのリポジトリからイメージを取得します。

**コマンド:**

```bash
docker pull ubuntu:latest
```

**出力例:**

```
latest: Pulling from library/ubuntu
c549ccf8d472: Already exists
Digest: sha256:123456789abcdef...
Status: Downloaded newer image for ubuntu:latest
```

**意味**: `ubuntu:latest` イメージをリポジトリからダウンロードし、既に存在するレイヤーは再ダウンロードしないことを示します。

#### `docker rmi`

**説明**: ローカルのDockerイメージを削除します。

**コマンド:**

```bash
docker rmi ubuntu:latest
```

**出力例:**

```
Untagged: ubuntu:latest
Deleted: sha256:123456789abcdef...
```

**意味**: `ubuntu:latest` イメージのタグが削除され、そのイメージのSHA256ハッシュが削除されたことを示します。

### 3. コンテナ関連のコマンド

#### `docker ps`

**説明**: 実行中のコンテナの一覧を表示します。

**コマンド:**

```bash
docker ps
```

**出力例:**

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
a1b2c3d4e5f6        ubuntu              "/bin/bash"              2 minutes ago       Up 2 minutes                            cool_banach
```

**意味**: `ubuntu` イメージから起動したコンテナが2分前に作成され、現在も実行中であることを示します。

#### `docker ps -a`

**説明**: すべてのコンテナ（停止中のコンテナも含む）の一覧を表示します。

**コマンド:**

```bash
docker ps -a
```

**出力例:**

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                        PORTS               NAMES
a1b2c3d4e5f6        ubuntu              "/bin/bash"              2 minutes ago       Exited (0) 1 second ago                           cool_banach
b7c8d9e0f1g2        nginx               "nginx -g 'daemon of…"   5 minutes ago       Up 5 minutes                                    elegant_turing
```

**意味**: `ubuntu` と `nginx` イメージから作成されたコンテナが存在し、`ubuntu` コンテナは終了（`Exited`）し、`nginx` コンテナは実行中であることを示します。

#### `docker run`

**説明**: 新しいコンテナを作成し、指定したコマンドを実行します。

**コマンド:**

```bash
docker run -it ubuntu /bin/bash
```

**出力例:**

```
root@a1b2c3d4e5f6:/#
```

**意味**: `ubuntu` イメージから新しいコンテナが作成され、インタラクティブモードで `/bin/bash` コマンドが実行されていることを示します。

#### `docker stop`

**説明**: 実行中のコンテナを停止します。

**コマンド:**

```bash
docker stop a1b2c3d4e5f6
```

**出力例:**

```
a1b2c3d4e5f6
```

**意味**: コンテナID `a1b2c3d4e5f6` のコンテナが停止されたことを示します。

#### `docker rm`

**説明**: コンテナを削除します。

**コマンド:**

```bash
docker rm a1b2c3d4e5f6
```

**出力例:**

```
a1b2c3d4e5f6
```

**意味**: コンテナID `a1b2c3d4e5f6` のコンテナが削除されたことを示します。

### 4. ボリューム関連のコマンド

#### `docker volume create`

**説明**: 新しいボリュームを作成します。

**コマンド:**

```bash
docker volume create my_volume
```

**出力例:**

```
my_volume
```

**意味**: 新しいボリューム `my_volume` が作成されたことを示します。

#### `docker volume ls`

**説明**: ボリュームの一覧を表示します。

**コマンド:**

```bash
docker volume ls
```

**出力例:**

```
DRIVER              VOLUME NAME
local               my_volume
```

**意味**: `local` ドライバで作成された `my_volume` ボリュームが存在することを示します。

#### `docker volume rm`

**説明**: ボリュームを削除します。

**コマンド:**

```bash
docker volume rm my_volume
```

**出力例:**

```
my_volume
```

**意味**: `my_volume` ボリュームが削除されたことを示します。

### 5. ネットワーク関連のコマンド

#### `docker network create`

**説明**: 新しいネットワークを作成します。

**コマンド:**

```bash
docker network create my_network
```

**出力例:**

```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7
```

**意味**: 新しいネットワーク `my_network` が作成され、そのネットワークIDが表示されます。

#### `docker network ls`

**説明**: ネットワークの一覧を表示します。

**コマンド:**

```bash
docker network ls
```

**出力例:**

```
NETWORK ID          NAME                DRIVER              SCOPE
a1b2c3d4e5f6        bridge              bridge              local
b7c8d9e0f1g2        host                host                local
h1i2j3k4l5m6        my_network          bridge              local
```

**意味**: `bridge` ドライバで作成された `my_network` ネットワークが存在することを示します。

#### `docker network rm`

**説明**: ネットワークを削除します。

**コマンド:**

```bash
docker network rm my_network
```

**出力例:**

```
my_network
```

**意味**: `my_network` ネットワークが削除されたことを示します。

### 6. Docker Compose関連のコマンド

#### `docker-compose up`

**説明**: `docker-compose.yml` ファイルに基づいてコンテナを起動します。

**コマンド:**

```bash
docker compose up -d
```

**出力例:**

```
Creating network "myapp_default" with the default driver
Creating myapp_db_1 ... done
Creating myapp_web_1 ... done
```

**意味**: `docker-compose.yml` ファイルに定義された `db` および `web` サービスのコンテナがバックグラウンドで起動されたことを示します。

#### `docker-compose down`

**説明**: `docker-compose.yml` ファイルに基づいて起動されたすべてのコンテナを停止し、ネットワークを削除します。

**コマンド:**

```bash
docker compose down
```

**出力例:**

```
Stopping myapp_web_1 ... done
Stopping myapp_db_1  ... done
Removing myapp_web_1 ... done
Removing myapp_db_1  ... done
Removing network myapp_default
```

**意味**: `docker-compose.yml` ファイルに定義されたすべてのコンテナが停止され、ネットワークが削除されたことを示します。

## 主要なオプション一覧

| オプション | 説明 |
|-----------|------|
| `-it` | インタラクティブモードとPTTを割り当てる |
| `-d` | バックグラウンドモードで実行 |
| `-p <host:container>` | ポート番号をマッピング |
| `-v <host:container>` | ボリュームをマウント |
| `-e <key=value>` | 環境変数を設定 |
| `--name <name>` | コンテナ名を指定 |
| `-m <memory>` | メモリ制限を設定 |

## まとめ

Dockerは、アプリケーションの開発からデプロイまでのプロセスを効率化し、環境依存性の問題を解決します。本ガイドを参考に、Dockerを活用して開発環境を整備し、よりスムーズな開発プロセスを実現してください。

これらのコマンドを使用することで、Dockerを効果的に操作し、コンテナの作成、管理、削除、ネットワーク設定などを簡単に行うことができます。各コマンドの出力例とその意味を理解することで、Dockerの操作がより明確になります。
