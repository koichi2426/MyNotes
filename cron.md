# Cron: タスクスケジューリングの自動化

## 概要

Cronは、UNIX系のオペレーティングシステムでタイムベースのジョブスケジューリングを行うためのデーモンです。定期的なタスクを自動で実行するのに役立ちます。例えば、毎日のバックアップ、定期的なメンテナンススクリプトの実行、定期的なメール送信などが挙げられます。

### Cronの特徴

- **自動実行**: 指定した時間や間隔でコマンドやスクリプトを自動実行
- **柔軟なスケジューリング**: 分、時間、日、月、曜日単位での細かい制御
- **バックグラウンド実行**: ユーザーがログオフしていてもタスク実行継続
- **ログ出力**: 実行結果やエラーをログファイルに記録可能

## Crontabの基本

Cronジョブのスケジューリングは、`crontab`ファイルを通じて行われます。`crontab`ファイルには、実行するコマンドとその実行スケジュールが含まれています。`crontab`ファイルは各ユーザーごとにあり、システム全体にも適用されます。

### Crontabファイルの構造

Crontabファイルの各行は次の形式で構成されています：

```
* * * * * command_to_be_executed
```

各フィールドの意味は以下の通りです：

| フィールド | 範囲 | 説明 |
|-----------|------|------|
| 分 | 0-59 | タスク実行時の分 |
| 時 | 0-23 | タスク実行時の時間（24時間制） |
| 日 | 1-31 | タスク実行時の日 |
| 月 | 1-12 | タスク実行時の月 |
| 曜日 | 0-7 | タスク実行時の曜日（0と7は日曜日） |

### スケジュール指定の例

```
0 2 * * * /path/to/script.sh
```

この例は「毎日午前2時にスクリプトを実行」を意味します。

## 基本操作

### Crontabの編集

Crontabファイルを編集するには、`crontab -e`コマンドを使用します。

```bash
crontab -e
```

これで、現在のユーザーのCrontabファイルがエディタで開きます。ここに新しいジョブを追加します。

### Crontabの確認

設定したCronジョブを確認するには、次のコマンドを使用します。

```bash
crontab -l
```

**出力例:**
```
0 * * * * cd /home/ubuntu/url_performance_api && bundle exec rake fetch_scores:execute
0 0 * * * /path/to/backup.sh
30 2 * * 0 /path/to/maintenance.sh
```

### 特定ユーザーのCrontabを編集

特定のユーザーのCrontabファイルを編集する場合、管理者権限で次のコマンドを使用します。

```bash
sudo crontab -u username -e
```

### Crontabの削除

現在のユーザーのすべてのCronジョブを削除する場合：

```bash
crontab -r
```

## コマンド集

### パターン1: 毎時0分に実行

```bash
0 * * * * command
```

**説明**: 毎時間の0分（1時間ごと）に実行

**実行時刻**: 00:00, 01:00, 02:00, ... 23:00

### パターン2: 毎日午前2時に実行

```bash
0 2 * * * /path/to/your/script.sh
```

**説明**: 毎日午前2時にシェルスクリプトを実行

### パターン3: 毎週月曜日の午前4時に実行

```bash
0 4 * * 1 apt-get update && apt-get upgrade -y
```

**説明**: 毎週月曜日の午前4時にシステムアップデートを実行

### パターン4: 毎月1日の午前1時に実行

```bash
0 1 1 * * tar -zcf /var/log/archive/$(date +\%Y-\%m-\%d).tar.gz /var/log/*.log
```

**説明**: 毎月1日の午前1時にログファイルを圧縮

### パターン5: 毎分実行

```bash
* * * * * cd /home/ubuntu/url_performance_api && bundle exec rake fetch_scores:execute
```

**説明**: 毎分（1分ごと）に実行

**出力例:**
```
00:00, 00:01, 00:02, ... 23:59 に実行
```

### パターン6: 5分ごとに実行

```bash
*/5 * * * * command
```

**説明**: 5分ごとに実行（00:00, 00:05, 00:10, ...）

### パターン7: 毎日の営業時間内（9時-17時）に30分ごと実行

```bash
*/30 9-17 * * * command
```

**説明**: 毎日9時から17時の間、30分ごとに実行

## ログ出力とデバッグ

Cronジョブの実行結果やエラーを確認するために、出力をファイルにリダイレクトします。

### 基本的なログ出力

```bash
* * * * * command >> /var/log/cron.log 2>&1
```

**説明**:
- `>>`: 出力をファイルに追記
- `2>&1`: 標準エラー出力（stderr）を標準出力（stdout）にリダイレクト

### ログファイルの確認

```bash
# リアルタイムでログを表示
tail -f /var/log/cron.log

# 最後の20行を表示
tail -20 /var/log/cron.log

# ログの全内容を表示
cat /var/log/cron.log
```

### タイムスタンプ付きログ

```bash
* * * * * command >> /var/log/cron.log 2>&1 &
echo "$(date '+\%Y-\%m-\%d \%H:\%M:\%S') - Command executed" >> /var/log/cron.log
```

## 実践例

### 例1: Rails Rakeタスクの毎時実行

```bash
0 * * * * export PATH="$HOME/.rbenv/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:$PATH" && eval "$(rbenv init -)" && cd /home/ubuntu/url_performance_api && bundle exec rake fetch_scores:execute >> /home/ubuntu/url_performance_api/cron.log 2>&1
```

**説明**:

| 要素 | 内容 | 役割 |
|------|------|------|
| `0 * * * *` | スケジュール | 毎時0分に実行 |
| `export PATH=...` | 環境変数設定 | rbenvが見つかるようにPATHを設定 |
| `eval "$(rbenv init -)"` | rbenv初期化 | 正しいRubyバージョンを設定 |
| `cd /home/ubuntu/...` | ディレクトリ移動 | 作業ディレクトリをRailsアプリに変更 |
| `bundle exec rake fetch_scores:execute` | メインコマンド | URLパフォーマンス評価タスク実行 |
| `>> ... 2>&1` | ログ出力 | 出力をログファイルに記録 |

**実行結果**:
```
毎時間の0分（00:00, 01:00, 02:00, ...）にRakeタスクが実行され、
結果が /home/ubuntu/url_performance_api/cron.log に記録される
```

### 例2: Rails Rakeタスクの毎日00:00実行

```bash
0 0 * * * export PATH="$HOME/.rbenv/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:$PATH" && export PASSWORD="password_here" && eval "$(rbenv init -)" && cd /home/ksato/pronavi-backend && RAILS_ENV=development bundle exec rake update_status:update_status >> /home/ksato/pronavi-backend/log/cron.log 2>&1
```

**説明**:

| 要素 | 内容 | 役割 |
|------|------|------|
| `0 0 * * *` | スケジュール | 毎日00:00に実行 |
| `export PASSWORD=...` | 環境変数 | データベース接続用パスワード設定 |
| `RAILS_ENV=development` | Rails環境指定 | 開発環境で実行 |
| `bundle exec rake update_status:update_status` | メインコマンド | ステータス更新タスク実行 |
| `>> ... 2>&1` | ログ出力 | 結果をログファイルに記録 |

**実行結果**:
```
毎日00:00にRakeタスクが実行され、結果がログファイルに記録される
```

**ログ確認**:
```bash
tail -f /home/ksato/pronavi-backend/log/cron.log
```

## 設定の手順

### ステップ1: crontabを編集

```bash
crontab -e
```

### ステップ2: 設定を追加

エディタ内で新しい行にジョブを追加します。

### ステップ3: 保存して終了

エディタの保存コマンドを使用（vimの場合は`:wq`）

### ステップ4: 設定の確認

```bash
crontab -l
```

設定したジョブが表示されれば成功です。

### ステップ5: ログで動作確認

```bash
tail -f /path/to/cron.log
```

## トラブルシューティング

### Cronジョブが実行されない場合

1. **crontab設定の確認**:
```bash
crontab -l
```

2. **スケジュール形式の確認**:
   - 5つのフィールドが正しく記述されているか確認
   - 値が正しい範囲内か確認

3. **環境変数の確認**:
   - `PATH`が正しく設定されているか確認
   - 必要な環境変数をexportしているか確認

4. **ログの確認**:
```bash
tail -f /var/log/syslog  # Linuxの場合
tail -f /var/log/cron.log  # 専用cronログファイル
```

### Cronジョブがエラーで失敗する場合

1. **ログの詳細確認**:
```bash
cat /path/to/cron.log | grep error
```

2. **コマンドを手動実行**:
同じ環境変数でコマンドを実行してエラーを特定

3. **権限の確認**:
スクリプトが実行可能か確認
```bash
ls -l /path/to/script.sh
chmod +x /path/to/script.sh  # 必要に応じて実行権限を付与
```

## セキュリティに関する注意

### パスワードの管理

Cronジョブにパスワードを含める場合は、セキュリティに注意してください：

```bash
# ❌ 危険: パスワードが見える
export PASSWORD="my_password"

# ✅ より安全: 環境ファイルを使用
source /home/user/.env
```

### ファイルのセキュリティ

Crontabファイルとログファイルのアクセス権限を適切に設定：

```bash
chmod 600 ~/.crontab
chmod 600 /path/to/cron.log
```

## 主要なオプション一覧

| コマンド | 説明 |
|---------|------|
| `crontab -e` | Crontabファイルを編集 |
| `crontab -l` | Crontabファイルの内容を表示 |
| `crontab -r` | Crontabファイルを削除 |
| `crontab -u username -e` | 特定ユーザーのCrontabを編集（root権限必須） |
| `crontab -u username -l` | 特定ユーザーのCrontabを表示（root権限必須） |

## スケジュール指定の特殊文字

| 記号 | 説明 | 例 |
|------|------|-----|
| `*` | すべての値 | `*` = 毎時間 |
| `,` | リスト区切り | `0,30` = 00分と30分 |
| `-` | 範囲 | `9-17` = 9時から17時 |
| `/` | ステップ値 | `*/5` = 5ごと |

## まとめ

Cronを使用することで、定期的なタスクを自動化し、システム管理を効率化することができます。Crontabの設定は非常に柔軟で、細かいスケジュール調整が可能です。

重要なポイント：
- ログ出力を必ず設定して、実行状況を監視
- 環境変数を適切に設定して、スクリプトが正常に動作
- セキュリティに注意してパスワードや機密情報を管理
- 定期的にログファイルをチェックして問題を早期に発見

これらのベストプラクティスを従うことで、信頼性の高い自動化タスクを実現できます。
