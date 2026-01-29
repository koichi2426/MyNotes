# ps コマンド - プロセス状態の確認

システムで実行中のプロセスに関する情報を表示するコマンド

## ps コマンド とは

`ps`（Process Status）は、UNIX および Linux システムで実行中のプロセスに関する情報を表示するコマンドです。システム管理者やエンドユーザーが、現在の動作状況を把握したり、トラブルシューティングを行う際に使用します。

### 用途

```
✅ ps コマンドで確認できること

├─ 実行中のプロセス一覧
├─ プロセスID（PID）
├─ プロセスのメモリ使用量
├─ CPU 使用率
├─ プロセスの親子関係
├─ プロセスの実行ユーザー
├─ プロセス開始時刻
└─ プロセスのステータス
```

## 基本的な使い方

### 最もシンプルな使用法

```bash
ps
```

**出力例：**
```
  PID TTY          TIME CMD
 2921 pts/1    00:00:00 bash
 3031 pts/1    00:00:00 ps
```

**説明：**
- **PID**：プロセスID（プロセスの識別子）
- **TTY**：ターミナル（接続先ターミナル、`?`はバックグラウンド）
- **TIME**：累積 CPU 時間（そのプロセスが使用した総 CPU 時間）
- **CMD**：実行中のコマンド

## よく使用されるオプション

### 1. `-e` : すべてのプロセスを表示

```bash
ps -e
```

**特徴：**
- システム上の **全プロセス** を表示
- バックグラウンドプロセスも含む
- システムプロセス（init、systemd など）も表示

**出力例：**
```
  PID TTY          TIME CMD
    1 ?        00:00:02 systemd
    2 ?        00:00:00 kthreadd
  ...
 2921 pts/1    00:00:00 bash
 3031 pts/1    00:00:00 ps
```

### 2. `-f` : フルフォーマットで表示

```bash
ps -f
```

**特徴：**
- **詳細情報** をフルフォーマットで表示
- 新しいカラムが追加される

**出力例：**
```
UID        PID  PPID  C STIME TTY          TIME CMD
user      2921  2801  0 11:00 pts/1    00:00:00 /bin/bash
user      3031  2921  0 11:10 pts/1    00:00:00 ps -f
```

**新しいカラムの説明：**
- **UID**：実行ユーザーの ID
- **PPID**：親プロセスの ID
- **C**：CPU 使用率（%）
- **STIME**：プロセス開始時刻

### 3. `-u ユーザー名` : 特定ユーザーのプロセスを表示

```bash
ps -u username
```

**特徴：**
- 指定したユーザーが実行しているプロセスのみ表示

**出力例：**
```
  PID TTY          TIME CMD
 2921 pts/1    00:00:00 bash
 3071 pts/1    00:00:00 sshd
 3082 pts/1    00:00:00 ps
```

### 4. `-p PID` : 特定のプロセス ID を指定

```bash
ps -p 1234
```

**特徴：**
- 指定した PID のプロセス情報のみを表示
- 複数指定可能：`ps -p 1234,5678,9012`

**出力例：**
```
  PID TTY          TIME CMD
 1234 pts/2    00:00:08 python
```

### 5. `-A` : すべてのプロセスを表示（`-e` の別表記）

```bash
ps -A
```

**特徴：**
- `-e` と同じ（POSIX 互換）

## よく使用される組み合わせ

### `ps -ef` : 全プロセスをフルフォーマットで表示

```bash
ps -ef
```

**用途：** システムの全体像を把握

**出力例：**
```
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 10:20 ?        00:00:02 /sbin/init
root         2     1  0 10:20 ?        00:00:00 [kthreadd]
...
user      2921  2801  0 11:00 pts/1    00:00:00 /bin/bash
```

### `ps -aux` : 詳細情報を表示（BSD フォーマット）

```bash
ps aux
```

**特徴：**
- Linux システムで最も一般的な用法
- メモリ使用率（%MEM）が表示される

**出力例：**
```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 168588  5564 ?        Ss   10:20   0:02 /sbin/init
...
user      2921  0.0  0.1 108552  3456 pts/1    Ss   11:00   0:00 /bin/bash
```

**カラムの説明：**
- **USER**：実行ユーザー
- **%CPU**：CPU 使用率
- **%MEM**：メモリ使用率
- **VSZ**：仮想メモリサイズ（KB）
- **RSS**：物理メモリサイズ（KB）
- **STAT**：プロセスの状態（S=Sleep、R=Running など）

### `ps -eo` : カスタムフォーマット

```bash
ps -eo pid,user,cmd,etime
```

**特徴：**
- 特定のカラムのみを表示
- カスタマイズが可能

**出力例：**
```
  PID USER     CMD                  ELAPSED
    1 root     /sbin/init             2:45:32
 2921 user     /bin/bash              1:35:20
```

**利用可能なカラム：**
```
pid : プロセス ID
user : ユーザー名
uid : ユーザー ID
cmd : コマンド
etime : 経過時間
lstart : 開始時刻
cputime : CPU 時間
vsz : 仮想メモリサイズ
rss : メモリ使用量
stat : 状態
cpuid : CPU ID
```

## grep と組み合わせた検索

### 特定のプロセスを探す

```bash
ps -ef | grep nginx
```

**用途：** 特定のアプリケーションが実行中かどうかを確認

**出力例：**
```
root      1234 ?        Ss   10:20   0:02 nginx: master process
www-data  1235 ?        S    10:20   0:00 nginx: worker process
user      3031 pts/1    S+   11:10   0:00 grep nginx
```

**注意：** `grep` 自体もプロセスリストに表示されます。これを除外するには：

```bash
ps -ef | grep nginx | grep -v grep
```

または

```bash
ps -ef | grep [n]ginx
```

### ps -aux での検索

```bash
ps aux | grep python
```

**用途：** Python プロセスの確認

**出力例：**
```
user      1234  0.5  2.3 145678 12345 ?        S    10:20   0:15 python app.py
user      3031  0.0  0.1 108552  3456 pts/1    S+   11:10   0:00 grep python
```

## 実用的な例

### 例1：特定のユーザーが実行しているプロセスをすべて表示

```bash
ps -u username -f
```

### 例2：CPU 使用率が高いプロセスを確認

```bash
ps aux | sort -nrk 3 | head -5
```

**説明：**
- `sort -nrk 3`：3番目のカラム（%CPU）の降順でソート
- `head -5`：上位5件を表示

### 例3：メモリ使用量が多いプロセスを確認

```bash
ps aux | sort -nrk 4 | head -5
```

**説明：**
- `sort -nrk 4`：4番目のカラム（%MEM）の降順でソート

### 例4：スパイプロセスの検出

```bash
ps -ef | grep defunct
```

**説明：**
- `defunct`（ゾンビプロセス）を検出
- 子プロセスが終了しても親プロセスが終了を確認していない状態

### 例5：プロセスツリーを表示

```bash
ps -ef --forest
```

**出力例：**
```
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 10:20 ?        00:00:02 /sbin/init
root       234     1  0 10:20 ?        00:00:01 /lib/systemd/systemd-journald
root       456     1  0 10:20 ?        00:00:00 /sbin/sshd
user      2921   456  0 11:00 pts/1    00:00:00  \_ /bin/bash
user      3031  2921  0 11:10 pts/1    00:00:00      \_ ps -ef --forest
```

## プロセスの状態（STAT）

ps コマンドで表示される STAT カラムの値：

```
R : 実行中（Running）
S : スリープ中（Sleeping）
D : ディスク入出力待機中
Z : ゾンビ（終了した子プロセス）
T : 停止中（Stopped）
W : ページング中

追加フラグ：
< : 高優先度プロセス
N : 低優先度プロセス
L : メモリロック中
s : セッションリーダー
+ : フォアグラウンドプロセスグループ
l : マルチスレッド
```

**例：**
- `Ss` : スリープ中でセッションリーダー
- `S+` : スリープ中でフォアグラウンド
- `Sl` : スリープ中でマルチスレッド

## ps コマンド集

| コマンド | 説明 |
|---------|------|
| `ps` | 現在のシェルセッションのプロセス表示 |
| `ps -e` | 全プロセス表示 |
| `ps -f` | フルフォーマット表示 |
| `ps -ef` | 全プロセスをフルフォーマット表示 |
| `ps -u user` | 特定ユーザーのプロセス表示 |
| `ps -p PID` | 特定PIDのプロセス表示 |
| `ps aux` | メモリ使用率付きで全プロセス表示（BSD フォーマット） |
| `ps -eo pid,user,cmd,etime` | カスタムフォーマット表示 |
| `ps -ef --forest` | プロセスツリー表示 |
| `ps -elf` | 長いフォーマット表示 |

## よくあるユースケース

### ケース1：実行中のアプリケーション確認

```bash
# nginx が実行中か確認
ps -ef | grep -i nginx

# Apache が実行中か確認
ps -ef | grep -i apache

# Node.js が実行中か確認
ps aux | grep node
```

### ケース2：メモリリークの疑い

```bash
# メモリ使用量が多いプロセスを監視
ps aux | sort -nrk 4 | head -10

# 定期的に実行（たとえば 5 秒ごと）
watch -n 5 'ps aux | sort -nrk 4 | head -10'
```

### ケース3：プロセスが存在するか確認

```bash
# a.out プログラムが実行中か確認
ps -ax | grep a.out

# Java アプリケーション確認
ps aux | grep java | grep -v grep
```

### ケース4：特定ユーザーの全プロセス確認

```bash
# www-data ユーザーの全プロセス
ps -u www-data -f

# root が実行しているバックグラウンドプロセス
ps -u root | grep -v "pts/"
```

### ケース5：プロセスツリーを表示

```bash
# sshd 関連のプロセスツリー
ps -ef --forest | grep sshd

# init 配下の全プロセスツリー
ps -ef --forest
```

## ps コマンドと他のコマンドの組み合わせ

### top との比較

```
ps : 静的スナップショット表示
top : リアルタイム監視（継続的に更新）

用途の使い分け：
- 1 回の確認 → ps
- 継続的な監視 → top
```

### kill コマンドとの組み合わせ

```bash
# プロセスを探して終了
ps -ef | grep nginx
kill -9 PID

# パイプで自動化（危険：注意が必要）
ps aux | grep 'old_process' | grep -v grep | awk '{print $2}' | xargs kill -9
```

### watch コマンドとの組み合わせ

```bash
# 特定プロセスを 2 秒ごとに監視
watch -n 2 'ps aux | grep nginx'

# メモリ使用量を継続監視
watch -n 1 'ps aux | sort -nrk 4 | head -10'
```

## ベストプラクティス

```
✅ 推奨される使用方法

① 全体像把握には ps -ef
   └─ すべての情報を素早く確認

② メモリ監視には ps aux
   └─ メモリ使用率が直接表示される

③ 特定プロセス確認には grep と組み合わせ
   └─ 「ps -ef | grep アプリ名」

④ 継続監視には watch
   └─ ps aux | watch で定期更新

❌ 避けるべき方法

① grep 漏れ
   └─ grep 自体もプロセスリストに表示される
   └─ grep [a]pp のように回避

② 根拠なき kill
   └─ プロセス内容確認後に実行

③ パイプの誤り
   └─ awk で正しく PID 抽出が必須
```

## トラブルシューティング

### 問題1：プロセスが見つからない

```bash
# 確認ステップ
ps -ef | head  # ps コマンド自体が動作するか確認
ps -ef | grep プロセス名  # 完全なコマンド名で検索
ps -ef | grep -i プロセス名  # 大文字小文字区別なしで検索
```

### 問題2：メモリ使用量が多いプロセス特定

```bash
# メモリ使用量でソート
ps aux | sort -nrk 4

# 上位 10 個を確認
ps aux | sort -nrk 4 | head -n 11  # ヘッダー + 10 件
```

### 問題3：ゾンビプロセスの確認

```bash
# ゾンビプロセスを検出
ps aux | grep defunct

# ゾンビプロセスの親プロセス ID を確認
ps -ef | grep -E '<defunct>|zombie'

# 親プロセスを終了
kill -9 親プロセスのPID
```

## 関連コマンド

```bash
# リアルタイム監視
top
htop  # より高機能な top

# プロセス終了
kill PID
killall プロセス名

# プロセス優先度変更
nice
renice

# プロセス情報詳細確認
proc ファイルシステム
cat /proc/PID/status
```

## 関連トピック

- [[ProcessManagement]]：プロセス管理全般
- [[ShellCommands]]：シェルコマンド
- [[SystemMonitoring]]：システム監視
