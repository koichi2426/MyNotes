# Shell Script - Unix/Linux自動化ガイド

Shellスクリプトを使用したタスク自動化とシステム管理

## Shell Script の概要

Shellスクリプトは、Unix系のオペレーティングシステムでタスクを自動化したり、システムの操作を管理したり、コマンドの複雑なシーケンスを効率的に実行したりするための強力なツールです。

### Shell Script とは

Shellスクリプトは、Unix系システムのコマンドラインインタープリタであるシェルによって実行される一連のコマンドを含むテキストファイルです。Shellスクリプトは、シンプルなファイル操作から複雑なシステム管理タスクまで、幅広いタスクを実行できます。

### 活用場面

```
✅ Shell Script が活躍する場面

├─ 定期的なバックアップ
├─ ログファイルの管理
├─ ユーザー管理の自動化
├─ システムモニタリング
├─ デプロイメント自動化
├─ ファイル処理の一括実行
├─ システムメンテナンス
└─ データ処理と加工
```

## Shell Script の種類

```
主要なシェル：

Bash（Bourne Again Shell）
├─ 最も一般的
├─ Linux のデフォルト
└─ 推奨される選択肢

Sh（Bourne Shell）
├─ 最小限の機能
├─ POSIX 互換
└─ ポータビリティ重視

Zsh
├─ 対話的シェルとして優秀
├─ 高度な機能
└─ スクリプト用途では Bash が推奨

Ksh（Korn Shell）
├─ UNIX システムで利用
└─ スクリプト用途の標準
```

## Shell Script の作成と実行

### Step 1：テキストエディタを開く

```bash
nano myscript.sh
```

または

```bash
vim myscript.sh
```

### Step 2：スクリプトを記述

```bash
#!/bin/bash
echo "Hello, World!"
```

**Shebang（シバン）について：**

```
#!/bin/bash

↓

#!     = Shebang の開始
/bin/bash = Bash シェルのパス

役割：システムに「このファイルを Bash で実行する」と指示
```

### Step 3：ファイルを保存

nano の場合：
```
Ctrl + O → Enter → Ctrl + X
```

vim の場合：
```
:wq
```

### Step 4：実行権限を付与

```bash
chmod +x myscript.sh
```

**権限の確認：**

```bash
ls -l myscript.sh
```

**出力例：**

```
-rwxr-xr-x  1 user  group  45 Jan 29 10:00 myscript.sh
```

### Step 5：スクリプトを実行

```bash
./myscript.sh
```

**出力例：**

```
Hello, World!
```

## 実践的な例

### 例 1：バックアップスクリプト

特定のディレクトリをバックアップするスクリプトです。

```bash
#!/bin/bash

# バックアップ元ディレクトリ
SOURCE_DIR="/home/user/documents"

# バックアップ先ディレクトリ
DEST_DIR="/backup"

# 日付を含むバックアップファイル名
BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).tar.gz"

# ディレクトリが存在するかチェック
if [ ! -d "$DEST_DIR" ]; then
    mkdir -p "$DEST_DIR"
fi

# バックアップの作成
echo "バックアップを開始します..."
tar -czvf "$DEST_DIR/$BACKUP_FILE" "$SOURCE_DIR"

# 結果確認
if [ $? -eq 0 ]; then
    echo "✅ バックアップが完了しました: $DEST_DIR/$BACKUP_FILE"
else
    echo "❌ バックアップに失敗しました"
    exit 1
fi
```

**実行例：**

```bash
bash backup.sh
```

**出力例：**

```
バックアップを開始します...
home/user/documents/file1.txt
home/user/documents/file2.txt
...
✅ バックアップが完了しました: /backup/backup_20260129_100000.tar.gz
```

### 例 2：ログファイルのローテーション

ログファイルを定期的にローテーションするスクリプトです。

```bash
#!/bin/bash

# ログディレクトリ
LOG_DIR="/var/log/myapp"

# ログファイルの保持日数
RETENTION_DAYS=7

echo "ログローテーション処理を開始します..."

# 古いログファイルを削除（7日以上前のファイル）
find "$LOG_DIR" -name "*.log" -type f -mtime +$RETENTION_DAYS -exec rm -f {} \;

echo "✅ 古いログファイルを削除しました"

# 当日のログファイルを圧縮
find "$LOG_DIR" -name "*.log" -type f ! -mtime -1 -exec gzip {} \;

echo "✅ ログファイルの圧縮が完了しました"

# 処理結果を通知
echo "処理日時: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_DIR/rotation.log"
```

**実行例：**

```bash
bash rotate_logs.sh
```

**Cron での定期実行：**

```bash
# 毎日午前 3 時に実行
0 3 * * * /home/user/scripts/rotate_logs.sh
```

### 例 3：ディレクトリ構造の検証スクリプト

```bash
#!/bin/bash

# 確認するディレクトリリスト
DIRS=(
    "/home/user/projects"
    "/home/user/documents"
    "/var/log/myapp"
)

echo "ディレクトリ構造の検証を開始します..."
echo "============================================"

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ 存在: $dir"
        echo "   ファイル数: $(find "$dir" -type f | wc -l)"
        echo "   サイズ: $(du -sh "$dir" | cut -f1)"
    else
        echo "❌ 存在しない: $dir"
    fi
done

echo "============================================"
echo "検証が完了しました"
```

## Shell Script の文法大全

### 1. 基本構文

#### 1.1. Shebang

```bash
#!/bin/bash
```

スクリプトの最初の行に記述され、スクリプトを実行するシェルを指定します。

#### 1.2. コメント

```bash
# これはコメントです
# 複数行のコメントも可能
```

### 2. 変数

#### 2.1. 変数の定義

```bash
# 変数を定義（等号の前後にスペースを入れない）
NAME="John"
AGE=25
PATH_DIR="/home/user/data"
```

**重要：** 等号の前後にスペースがあるとエラーになります

```bash
❌ NAME = "John"  # エラー
✅ NAME="John"    # 正しい
```

#### 2.2. 変数の参照

```bash
echo $NAME           # John
echo ${NAME}         # John（推奨される形式）
echo "My name is $NAME"  # My name is John
```

#### 2.3. 特殊変数

```bash
#!/bin/bash

# スクリプト名
echo "スクリプト: $0"

# コマンドライン引数
echo "第1引数: $1"
echo "第2引数: $2"

# すべての引数
echo "すべての引数: $@"

# 引数の個数
echo "引数の数: $#"

# プロセスID
echo "プロセスID: $$"

# 最後のコマンドの終了ステータス
command
echo "終了ステータス: $?"
```

**実行例：**

```bash
bash script.sh arg1 arg2
```

**出力例：**

```
スクリプト: script.sh
第1引数: arg1
第2引数: arg2
すべての引数: arg1 arg2
引数の数: 2
プロセスID: 12345
終了ステータス: 0
```

### 3. 演算

#### 3.1. 算術演算

```bash
# expr コマンドを使用
result=$(expr 3 + 4)
echo $result  # 7

# (( )) 括弧を使用（推奨）
result=$((3 + 4))
echo $result  # 7

# より複雑な式
result=$((10 * 2 + 5))
echo $result  # 25
```

**演算子：**

```bash
+  : 加算
-  : 減算
*  : 乗算
/  : 除算
%  : 剰余
```

#### 3.2. 文字列操作

```bash
STR="Hello World"

# 文字列の長さ
echo ${#STR}          # 11

# 部分文字列
echo ${STR:0:5}       # Hello

# 文字列の置換
echo ${STR/World/Universe}  # Hello Universe
```

### 4. 条件文

#### 4.1. if 文

```bash
if [ 条件 ]; then
    # 条件が真の場合
elif [ 別の条件 ]; then
    # 別の条件が真の場合
else
    # いずれの条件も偽の場合
fi
```

**例：**

```bash
#!/bin/bash

NAME="John"

if [ "$NAME" == "John" ]; then
    echo "Hello, John!"
elif [ "$NAME" == "Jane" ]; then
    echo "Hello, Jane!"
else
    echo "Hello, stranger!"
fi
```

#### 4.2. 条件式

```bash
# ファイルテスト
[ -f FILE ]      # ファイルが存在するか
[ -d DIR ]       # ディレクトリが存在するか
[ -e FILE ]      # ファイル/ディレクトリが存在するか
[ -r FILE ]      # 読み込み可能か
[ -w FILE ]      # 書き込み可能か
[ -x FILE ]      # 実行可能か

# 文字列テスト
[ -z STRING ]    # 文字列が空か
[ -n STRING ]    # 文字列が空でないか
[ STRING1 = STRING2 ]    # 文字列が等しいか
[ STRING1 != STRING2 ]   # 文字列が異なるか

# 数値テスト
[ NUM1 -eq NUM2 ]  # 等しい（equal）
[ NUM1 -ne NUM2 ]  # 異なる（not equal）
[ NUM1 -lt NUM2 ]  # より小さい（less than）
[ NUM1 -le NUM2 ]  # より小さいか等しい
[ NUM1 -gt NUM2 ]  # より大きい（greater than）
[ NUM1 -ge NUM2 ]  # より大きいか等しい

# 論理演算子
[ COND1 ] && [ COND2 ]   # AND
[ COND1 ] || [ COND2 ]   # OR
[ ! COND ]               # NOT
```

**実践例：**

```bash
#!/bin/bash

AGE=$1

if [ -z "$AGE" ]; then
    echo "年齢を指定してください"
    exit 1
elif [ $AGE -lt 18 ]; then
    echo "未成年です"
elif [ $AGE -ge 18 ] && [ $AGE -lt 65 ]; then
    echo "成人です"
else
    echo "高齢者です"
fi
```

### 5. ループ

#### 5.1. for ループ

```bash
# リスト反復
for item in item1 item2 item3; do
    echo $item
done

# 数値範囲
for i in {1..5}; do
    echo $i
done

# C言語形式
for ((i=1; i<=5; i++)); do
    echo $i
done
```

**実践例：**

```bash
#!/bin/bash

# ファイル一覧を処理
for file in /home/user/*.txt; do
    if [ -f "$file" ]; then
        echo "処理中: $file"
        # ファイル処理
    fi
done
```

#### 5.2. while ループ

```bash
count=1
while [ $count -le 5 ]; do
    echo $count
    count=$((count + 1))
done
```

**出力例：**

```
1
2
3
4
5
```

#### 5.3. until ループ

```bash
count=1
until [ $count -gt 5 ]; do
    echo $count
    count=$((count + 1))
done
```

### 6. 関数

#### 6.1. 関数の定義と呼び出し

```bash
#!/bin/bash

# 関数の定義
my_function() {
    echo "これは関数です"
}

# 関数の呼び出し
my_function
```

**出力例：**

```
これは関数です
```

#### 6.2. 引数の受け渡し

```bash
#!/bin/bash

greet() {
    echo "Hello, $1!"
    echo "You are $2 years old."
}

greet "Alice" "25"
```

**出力例：**

```
Hello, Alice!
You are 25 years old.
```

#### 6.3. 戻り値

```bash
#!/bin/bash

add() {
    result=$(($1 + $2))
    return $result
}

add 3 4
echo "合計: $?"  # 注：return は 255 までの値

# または、エコーで値を返す
add() {
    echo $(($1 + $2))
}

result=$(add 3 4)
echo "合計: $result"  # 合計: 7
```

### 7. 配列

#### 7.1. 配列の定義

```bash
# 配列の定義
my_array=("apple" "banana" "cherry")

# インデックスで定義
fruits[0]="apple"
fruits[1]="banana"
fruits[2]="cherry"
```

#### 7.2. 配列へのアクセス

```bash
#!/bin/bash

my_array=("apple" "banana" "cherry")

# 特定の要素にアクセス
echo ${my_array[0]}     # apple
echo ${my_array[1]}     # banana

# すべての要素にアクセス
echo ${my_array[@]}     # apple banana cherry

# 配列の要素数
echo ${#my_array[@]}    # 3

# 特定の要素の長さ
echo ${#my_array[0]}    # 5
```

#### 7.3. 配列の反復

```bash
#!/bin/bash

colors=("red" "green" "blue")

for color in "${colors[@]}"; do
    echo "Color: $color"
done
```

**出力例：**

```
Color: red
Color: green
Color: blue
```

### 8. 入出力リダイレクト

#### 8.1. 標準出力のリダイレクト

```bash
# ファイルに出力（上書き）
echo "Hello" > output.txt

# ファイルに出力（追記）
echo "World" >> output.txt
```

#### 8.2. 標準入力のリダイレクト

```bash
# ファイルから入力
command < input.txt

# ヒアドキュメント
cat << EOF
Line 1
Line 2
Line 3
EOF
```

#### 8.3. 標準エラーのリダイレクト

```bash
# エラーをファイルに出力
ls non_existing_file 2> error.txt

# 標準出力と標準エラーの両方をリダイレクト
command > output.txt 2>&1
```

#### 8.4. パイプ

```bash
# コマンドの出力を別のコマンドに渡す
cat file.txt | grep "pattern"

# 複数のパイプ
ps aux | grep "process" | awk '{print $2}'
```

### 9. 高度なテクニック

#### 9.1. コマンド置換

```bash
# コマンドの出力を変数に代入
current_date=$(date)
echo "Today is: $current_date"

# 古い方法（後方互換性）
current_date=`date`
```

#### 9.2. サブシェル

```bash
#!/bin/bash

# 親シェルの変数
VAR="parent"

(
    # サブシェル内で変数を変更
    VAR="child"
    echo "In subshell: $VAR"  # child
)

# 親シェルの変数は変わらない
echo "In parent: $VAR"  # parent
```

#### 9.3. クォートの使い分け

```bash
#!/bin/bash

NAME="John"

# ダブルクォート（変数展開される）
echo "Hello, $NAME"           # Hello, John

# シングルクォート（変数展開されない）
echo 'Hello, $NAME'           # Hello, $NAME

# バックスラッシュ（エスケープ）
echo "Hello, \$NAME"          # Hello, $NAME
```

#### 9.4. 条件演算子

```bash
#!/bin/bash

AGE=$1

# 三項演算子的な表現
status=$([ $AGE -ge 18 ] && echo "adult" || echo "minor")
echo "Status: $status"
```

#### 9.5. case 文

```bash
#!/bin/bash

FRUIT=$1

case $FRUIT in
    "apple")
        echo "It's an apple"
        ;;
    "banana")
        echo "It's a banana"
        ;;
    "orange")
        echo "It's an orange"
        ;;
    *)
        echo "Unknown fruit"
        ;;
esac
```

## スクリプトのデバッグ

### デバッグモードで実行

```bash
bash -x script.sh
```

出力例：

```
+ NAME="John"
+ echo Hello, John!
Hello, John!
```

### 特定部分のデバッグ

```bash
#!/bin/bash

set -x  # デバッグを開始
echo "Debug: $NAME"
set +x  # デバッグを終了
```

## ベストプラクティス

```
✅ 推奨される実践

① シバンは必須
   └─ #!/bin/bash で開始

② 変数はクォート
   └─ echo "$VAR"

③ エラーチェック
   └─ if [ $? -ne 0 ]; then

④ 説明的な変数名
   └─ SOURCE_DIR （× SRC_DIR）

⑤ コメントを追加
   └─ 複雑な部分を説明

⑥ ロギング機能
   └─ echo "$(date): メッセージ" >> log.txt

❌ 避けるべき使い方

① グローバル変数の濫用
   └─ 関数内で local を使用

② エラーハンドリングなし
   └─ 各重要な処理後に確認

③ ハードコード
   └─ 環境変数や設定ファイルを使用

④ スペースなしの詰まったコード
   └─ 可読性が低下
```

## 実行可能スクリプトの配置

```bash
# スクリプトを /usr/local/bin に配置
sudo cp script.sh /usr/local/bin/scriptname

# 実行権限を付与
sudo chmod +x /usr/local/bin/scriptname

# どこからでも実行可能に
scriptname
```

## Cron での定期実行

```bash
# Crontab を編集
crontab -e

# 以下の形式で記述
# 分 時 日 月 曜日 コマンド
0 3 * * * /home/user/scripts/backup.sh
```

**Cron 時間表記：**

```
0 3 * * *        毎日午前3時
0 */4 * * *      4時間ごと
0 0 * * 0        毎週日曜の午前0時
0 0 1 * *        毎月1日の午前0時
*/15 * * * *     15分ごと
```

## 関連トピック

- [[Bash]]：Bash シェルリファレンス
- [[CommandLine]]：コマンドラインツール
- [[SystemAdministration]]：システム管理
- [[Automation]]：自動化技術
