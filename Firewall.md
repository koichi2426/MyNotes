# Firewall: ネットワークセキュリティの基礎

## 概要

### ファイヤーウォールとは

ファイヤーウォール（Firewall）は、不正アクセスやウイルス、その他のセキュリティ脅威からネットワークを保護するためのシステムまたはソフトウェアです。これは、ネットワークとインターネットの間に「壁」を設けることにより、内部ネットワークへの不正アクセスを防ぎ、内部からの不適切なデータ送出を制限することで機能します。

### ファイヤーウォールの重要性

- **データ保護**：機密情報が外部に漏れることを防ぎます。
- **攻撃防止**：外部からの攻撃、例えばDoS攻撃やマルウェアの侵入をブロックします。
- **アクセス制御**：ユーザーがアクセスできるリソースを制限し、セキュリティを向上させます。
- **コンプライアンス**：法的要件や業界標準を満たすためのセキュリティ基盤。

### ファイヤーウォールの種類

#### 1. パケットフィルタリング型

パケットのヘッダ情報（送信元IPアドレス、送信先IPアドレス、ポート番号など）を検査し、事前に設定されたルールに基づいて通過を許可または拒否します。

**特徴:**
- シンプルで高速
- ただし、パケット内容は検査しない
- 比較的低いセキュリティレベル

#### 2. ステートフルインスペクション型

パケットフィルタリング型の機能に加え、セッション情報を記録し、通信のコンテキストを理解してより精密なアクセス制御を行います。

**特徴:**
- 確立されたセッションのみを許可
- 接続状態を追跡
- より高いセキュリティレベル

#### 3. アプリケーションプロキシ型

各アプリケーションごとに専用のゲートウェイを提供し、アプリケーションレベルでのデータの検査とフィルタリングを行います。

**特徴:**
- 最も高いセキュリティレベル
- アプリケーション層での検査が可能
- 処理速度が低下する場合がある

### ファイヤーウォールの運用

ファイヤーウォールの効果的な運用には、以下の点が重要です：

1. **定期的な更新とメンテナンス**
   - 新たな脅威に対応するため、ソフトウェアとセキュリティポリシーの定期的な更新が必要

2. **ポリシーの設定と管理**
   - 適切なファイヤーウォールポリシーの策定と維持が、セキュリティの効果を最大限に引き出す

3. **モニタリングとログの分析**
   - ネットワークトラフィックを常時監視し、異常な動きを早期に検知

4. **定期的なセキュリティレビュー**
   - ルール設定が最新の脅威に対応しているか定期的に確認

ファイヤーウォールは、その機能と適切な運用によって、企業や個人のデータを守るための最前線に位置します。ネットワークセキュリティを確保するためには、これらのシステムが不可欠であり、適切な設定と管理が求められます。

## UFW (Uncomplicated Firewall)

### UFWの概要

UFW（Uncomplicated Firewall）は、Linuxのセキュリティを強化するためのユーザーフレンドリーなインターフェースを提供するファイヤーウォールツールです。iptablesの複雑さを抑え、簡単にファイヤーウォールの設定ができるように設計されています。特にUbuntuなどのDebian系Linuxディストリビューションで広く使用されています。

### UFWの主な特徴

- **シンプルなコマンドラインインターフェース**：コマンドの構造が単純で覚えやすい
- **ルールベースの構成**：アプリケーションのプロファイルを使用してアクセスを許可または拒否
- **IPv4 と IPv6 のサポート**：両方のプロトコルでのルール設定が可能
- **ステートフルファイアウォール**：接続状態を追跡して管理

### UFWのインストール

Ubuntuの場合、UFWはデフォルトでインストールされていることが多いですが、必要に応じてインストールできます：

```bash
sudo apt update
sudo apt install ufw
```

## UFWの基本操作

### UFWの有効化・無効化

#### UFWの有効化

```bash
sudo ufw enable
```

このコマンドはUFWを有効にし、システム起動時に自動的にファイヤーウォールが起動するよう設定します。

**確認メッセージ:**
```
Firewall is active and enabled on system startup
```

#### UFWの無効化

```bash
sudo ufw disable
```

ファイヤーウォールを無効にし、全てのルールが無効になります。ただし、設定は保持されます。

### ステータスの確認

#### シンプル表示

```bash
sudo ufw status
```

**出力例:**
```
Status: active
```

#### 詳細表示

```bash
sudo ufw status verbose
```

**出力例:**
```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), deny (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
443/tcp (v6)               ALLOW       Anywhere (v6)
```

#### ルール番号付き表示

```bash
sudo ufw status numbered
```

**出力例:**
```
     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW       Anywhere
[ 2] 80/tcp                     ALLOW       Anywhere
[ 3] 443/tcp                    ALLOW       Anywhere
```

## UFWのルール管理

### ルールの追加

#### ポート番号でルールを追加

特定のポートをTCPで開放：

```bash
sudo ufw allow 80/tcp
```

特定のポートをUDPで開放：

```bash
sudo ufw allow 53/udp
```

プロトコルを指定しない場合（TCP/UDP両方）：

```bash
sudo ufw allow 22
```

#### サービス名でルールを追加

UFWはアプリケーションプロファイルを持っており、サービス名で直接許可できます：

```bash
# HTTP
sudo ufw allow http

# HTTPS
sudo ufw allow https

# SSH
sudo ufw allow ssh

# DNS
sudo ufw allow dns
```

利用可能なアプリケーションプロファイルを確認：

```bash
sudo ufw app list
```

**出力例:**
```
Available applications:
  Apache
  Apache Full
  Apache Secure
  Cups
  Nginx Full
  Nginx HTTP
  Nginx HTTPS
  OpenSSH
  Postfix
  Postfix SMTP
  Samba
  Samba Web Administration Tool
  This PC
```

#### IPアドレスを指定してルールを追加

特定のIPアドレスからのアクセスを許可：

```bash
# 特定IPアドレスからのSSHを許可
sudo ufw allow from 192.168.1.1 to any port 22

# IPアドレスをコマンド全体で許可
sudo ufw allow from 192.168.1.1
```

特定のIPアドレスからの特定ポートを許可：

```bash
sudo ufw allow from 192.168.1.100 to any port 3306
```

IPv6アドレスでのルール追加：

```bash
sudo ufw allow from 2001:db8::1/128 to any port 22
```

#### サブネットを指定してルールを追加

サブネット内のすべてのIPアドレスからのアクセスを許可：

```bash
sudo ufw allow from 192.168.1.0/24
```

#### ポートレンジを指定してルールを追加

複数のポートに対してルールを追加：

```bash
sudo ufw allow 6000:6007/tcp
sudo ufw allow 6000:6007/udp
```

### ルールの拒否

#### ポート番号でルールを拒否

```bash
sudo ufw deny 25/tcp
```

#### サービス名でルールを拒否

```bash
sudo ufw deny ssh
```

#### IPアドレスからのアクセスを拒否

```bash
sudo ufw deny from 192.168.1.50
```

### ルールの削除

#### ルール番号を使用して削除

先にルール番号を確認：

```bash
sudo ufw status numbered
```

番号でルールを削除：

```bash
sudo ufw delete 2
```

システムが確認を求めます：
```
Do you want to continue? [y/N] y
```

#### ルールの内容を指定して削除

```bash
# ポート番号で削除
sudo ufw delete allow 80/tcp

# サービス名で削除
sudo ufw delete allow http

# IPアドレスで削除
sudo ufw delete allow from 192.168.1.100
```

### デフォルトポリシーの設定

#### 受信接続のデフォルトポリシー

すべての受信接続をデフォルトで拒否（推奨）：

```bash
sudo ufw default deny incoming
```

すべての受信接続をデフォルトで許可（非推奨）：

```bash
sudo ufw default allow incoming
```

#### 送信接続のデフォルトポリシー

すべての送信接続をデフォルトで許可（推奨）：

```bash
sudo ufw default allow outgoing
```

すべての送信接続をデフォルトで拒否（非推奨）：

```bash
sudo ufw default deny outgoing
```

## UFWのログ機能

### ログの有効化・無効化

ログを有効にする：

```bash
sudo ufw logging on
```

ログを無効にする：

```bash
sudo ufw logging off
```

### ログレベルの設定

ログレベルを指定：

```bash
sudo ufw logging low
sudo ufw logging medium
sudo ufw logging high
sudo ufw logging full
```

**各レベルの説明:**
- `low`：マッチしたルールのみログ
- `medium`：無効なパケット、疑わしいパケット、および有効なパケットをログ
- `high`：すべてのパケットをログ
- `full`：複製されたパケットを含むすべてのパケットをログ

### ログファイルの確認

UFWのログは通常 `/var/log/ufw.log` に保存されます：

```bash
# ログの最後の20行を表示
tail -20 /var/log/ufw.log

# ログファイル全体を表示
cat /var/log/ufw.log

# ログをリアルタイムで監視
tail -f /var/log/ufw.log

# 特定の日時のログを検索
grep "Jan 29" /var/log/ufw.log
```

**ログの出力例:**
```
Jan 29 10:15:32 ubuntu kernel: [UFW BLOCK] IN=eth0 OUT= MAC=... SRC=203.0.113.45 DST=192.168.1.100 PROTO=TCP SPT=54321 DPT=22 WINDOW=1024 RES=0x00 SYN URGP=0
```

## UFWの実践的な設定例

### 例1: Webサーバーの基本設定

```bash
# UFWを有効化
sudo ufw enable

# デフォルトで受信を拒否
sudo ufw default deny incoming

# 送信は許可
sudo ufw default allow outgoing

# SSH（遠隔管理用）を許可
sudo ufw allow ssh

# HTTP
sudo ufw allow http

# HTTPS
sudo ufw allow https

# 設定確認
sudo ufw status verbose
```

### 例2: 特定のIPアドレスのみアクセス許可

管理ネットワーク（192.168.1.0/24）からのSSH接続のみ許可：

```bash
# デフォルトで受信拒否
sudo ufw default deny incoming

# 特定のサブネットからSSHを許可
sudo ufw allow from 192.168.1.0/24 to any port 22

# インターネットからHTTP/HTTPSは許可
sudo ufw allow http
sudo ufw allow https

# 確認
sudo ufw status verbose
```

### 例3: データベースサーバーの設定

MySQL/MariaDBサーバーの場合：

```bash
# デフォルトで受信拒否
sudo ufw default deny incoming

# アプリケーションサーバー（192.168.1.50）からのみ許可
sudo ufw allow from 192.168.1.50 to any port 3306

# 管理者用SSH
sudo ufw allow from 192.168.1.0/24 to any port 22

# 確認
sudo ufw status numbered
```

### 例4: ポートレンジの開放

ゲームサーバーなどで複数のポートが必要な場合：

```bash
# ポート6000-6010 (TCP/UDP)
sudo ufw allow 6000:6010/tcp
sudo ufw allow 6000:6010/udp

# 確認
sudo ufw status
```

### 例5: インターネット側のWebサーバー + 内部DBサーバー

```bash
# デフォルトポリシー設定
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Web通信（どこからでも）
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# SSH（管理ネットワークのみ）
sudo ufw allow from 192.168.1.0/24 to any port 22

# データベース通信（内部ネットワークのみ）
sudo ufw allow from 192.168.1.0/24 to any port 3306

# 確認
sudo ufw status numbered
```

## UFWのトラブルシューティング

### 設定後、接続できなくなった場合

コンソール経由でアクセスしてSSHを再度許可：

```bash
# SSHを許可（もしUFWが有効ならこれが必要な場合がある）
sudo ufw allow 22/tcp

# UFWを再度確認
sudo ufw status verbose
```

### ルールが反映されない場合

UFWを再起動：

```bash
sudo ufw reload
```

### すべてのルールをリセットしたい場合

```bash
# デフォルト設定にリセット（確認が必須）
sudo ufw reset
```

**警告**: このコマンドはすべてのルール設定を削除します。

### ファイアウォール経由でのトラフィック確認

tcpdumpを使用してUFWでブロックされているトラフィックを確認：

```bash
# UFWログを監視
sudo tail -f /var/log/ufw.log

# grep で特定のポートをフィルター
sudo grep "DPT=22" /var/log/ufw.log
```

## UFWコマンドリファレンス

| コマンド | 説明 |
|---------|------|
| `sudo ufw enable` | UFWを有効化 |
| `sudo ufw disable` | UFWを無効化 |
| `sudo ufw status` | ステータス確認（シンプル） |
| `sudo ufw status verbose` | ステータス確認（詳細） |
| `sudo ufw status numbered` | ステータス確認（ルール番号付き） |
| `sudo ufw allow [ポート/サービス]` | ルール追加（許可） |
| `sudo ufw deny [ポート/サービス]` | ルール追加（拒否） |
| `sudo ufw delete [ルール]` | ルール削除 |
| `sudo ufw default allow/deny [incoming/outgoing]` | デフォルトポリシー設定 |
| `sudo ufw logging on/off` | ログの有効化/無効化 |
| `sudo ufw logging [low/medium/high/full]` | ログレベル設定 |
| `sudo ufw reload` | 設定の再読み込み |
| `sudo ufw reset` | デフォルト設定にリセット |
| `sudo ufw allow from [IP/CIDR]` | IPアドレス/サブネットを許可 |
| `sudo ufw app list` | 利用可能なアプリケーションプロファイル表示 |

## セキュリティベストプラクティス

### ファイアウォール設定時の注意点

1. **デフォルトで受信を拒否**
   - `sudo ufw default deny incoming` を設定し、必要なポートのみ開放

2. **SSH接続を確保**
   - 遠隔管理の場合、UFW有効化前にSSHを許可することで接続喪失を防止

3. **定期的なルール見直し**
   - 使用していないサービスのポートは閉じる
   - 不要になったルールは削除する

4. **ログの監視**
   - 定期的にファイアウォールログを確認し、不正なアクセス試行を検出

5. **段階的なルール追加**
   - 一度に多くのルールを追加するのではなく、必要に応じて段階的に追加

6. **インターナルネットワークのセキュリティ**
   - 内部ネットワークでもデータベースなどへのアクセスは制限すべき

7. **バージョン管理**
   - 重要な設定変更前に現在の設定をバックアップ

## DNS・NTPサーバーの開放例

### DNS（ポート53）の開放

```bash
# DNSサーバーの場合（TCP/UDP）
sudo ufw allow 53/tcp
sudo ufw allow 53/udp

# または
sudo ufw allow 53
```

### NTP（ポート123）の開放

```bash
# NTPサーバーの場合
sudo ufw allow 123/udp
```

## ファイアウォール設定の保存と復元

UFWの設定は自動的に保存されますが、手動でバックアップすることも推奨されます：

```bash
# ルール一覧をテキストで保存
sudo ufw show added > ~/ufw_backup.txt

# または
sudo iptables-save > ~/iptables_backup.txt

# 復元（必要な場合）
# ルールは手動で ufw コマンドで再度追加する必要があります
```

## まとめ

UFWはUbuntuおよびDebian系Linuxディストリビューションで簡単にファイアウォール管理ができるツールです。適切に設定することで、システムのセキュリティを大幅に向上させることができます。以下のポイントを常に意識してください：

- デフォルトで受信を拒否し、必要なポートのみ開放する
- ルール設定時にSSH接続を失わないよう注意する
- 定期的にログを確認し、不正アクセス試行を監視する
- 不要になったルールは削除して、ファイアウォール設定を整理する
