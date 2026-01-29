# export コマンド - 環境変数の設定と管理

シェル環境で環境変数を設定し、子プロセスに継承させるコマンド

## export コマンドの概要

`export` コマンドは、シェル環境において環境変数を設定し、その設定をシェルセッションおよびその子プロセスに適用するために使用される重要なコマンドです。主にシェルスクリプトやシェルセッションの設定に利用されます。

### 環境変数とは

環境変数は、シェルセッション内で利用可能な変数で、設定されたプロセスだけでなく、そこから生成される子プロセスにも継承されます。

```
環境変数の特徴：

親プロセス
  ↓
export VAR_NAME=value
  ↓
子プロセスで VAR_NAME が利用可能
```

### 通常の変数と環境変数の違い

```
通常の変数：
VAR_NAME=value
├─ 現在のシェルセッションのみで有効
└─ 子プロセスには継承されない

環境変数：
export VAR_NAME=value
├─ 現在のシェルセッション + 子プロセスで有効
└─ スクリプト実行時に利用可能
```

## export コマンドの基本的な使い方

### 基本構文

```bash
export VAR_NAME=value
```

**パラメータの説明：**

```
VAR_NAME : 環境変数の名前（大文字が慣例）
value    : 設定する値（文字列や数値）
```

### 1. 環境変数の設定

最もシンプルな使い方は、環境変数に値を設定することです。

```bash
export MY_VAR=hello
```

**出力確認：**

```bash
echo $MY_VAR
```

**出力例：**

```
hello
```

**解説：**
このコマンドは `MY_VAR` という環境変数に `hello` という値を設定し、現在のシェルセッションおよびその子プロセスで利用可能にします。

### 2. 環境変数の確認

設定した環境変数を確認するには `echo` コマンドを使用します。

```bash
echo $MY_VAR
```

**出力例：**

```
hello
```

**解説：**
このコマンドは、`MY_VAR` 環境変数の値を表示します。`export` コマンドで設定した値が反映されています。

### 3. 複数の変数を同時に設定

複数の環境変数をまとめて設定することができます。

```bash
export VAR1=value1 VAR2=value2 VAR3=value3
```

**実践例：**

```bash
export PATH=/usr/local/bin:$PATH EDITOR=vim LANG=en_US.UTF-8
```

**確認：**

```bash
echo "PATH=$PATH"
echo "EDITOR=$EDITOR"
echo "LANG=$LANG"
```

**出力例：**

```
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
EDITOR=vim
LANG=en_US.UTF-8
```

**解説：**
このコマンドは複数の環境変数を同時に設定します。`PATH` 環境変数に新しいディレクトリを追加し、同時に `EDITOR` と `LANG` を設定しています。

## 環境変数の一覧表示

### 全環境変数の表示

```bash
export -p
```

**出力例：**

```
declare -x HOME="/home/user"
declare -x LOGNAME="user"
declare -x PATH="/usr/local/bin:/usr/bin:/bin"
declare -x LANG="en_US.UTF-8"
declare -x SHELL="/bin/bash"
declare -x EDITOR="vim"
declare -x MY_VAR="hello"
...
```

**解説：**
`export -p` コマンドは、現在のシェルセッションで設定されているすべての環境変数を一覧表示します。`declare -x` の形式で出力されます。

### 特定の変数の確認

```bash
env | grep VAR_NAME
```

**実践例：**

```bash
env | grep PATH
```

**出力例：**

```
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
```

**解説：**
`env` コマンドは環境変数を一覧表示し、`grep` で特定の変数を検索します。

## 環境変数の削除

環境変数を削除するには `unset` コマンドを使用します。

```bash
unset VAR_NAME
```

**実践例：**

```bash
export MY_VAR=hello
echo $MY_VAR        # hello
unset MY_VAR
echo $MY_VAR        # （空行）
```

**出力例：**

```
hello

```

**解説：**
このコマンドは、`MY_VAR` 環境変数を削除します。これにより、`MY_VAR` は現在のシェルセッションおよびその子プロセスで使用できなくなります。

## 実践的な使用例

### 例1：PATH 環境変数の拡張

新しいディレクトリをパスに追加します。

```bash
export PATH=/usr/local/go/bin:$PATH
```

**確認：**

```bash
echo $PATH
```

**出力例：**

```
/usr/local/go/bin:/usr/local/bin:/usr/bin:/bin
```

**解説：**
`/usr/local/go/bin` ディレクトリを PATH の最初に追加します。これにより、そのディレクトリのプログラムが優先的に実行されます。

### 例2：JAVA_HOME の設定

Java 開発環境の設定例です。

```bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$JAVA_HOME/bin:$PATH
```

**確認：**

```bash
$JAVA_HOME/bin/java -version
```

**出力例：**

```
openjdk version "11.0.13" 2021-10-19
OpenJDK Runtime Environment (build 11.0.13+8-Ubuntu-0ubuntu1)
```

**解説：**
Java の home ディレクトリを設定し、その bin ディレクトリを PATH に追加します。

### 例3：データベース接続情報の設定

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=mydb
export DB_USER=admin
```

**スクリプトでの利用：**

```bash
#!/bin/bash
psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER
```

**解説：**
データベース接続情報を環境変数として設定することで、スクリプトで柔軟に利用できます。

### 例4：API キーの管理

```bash
export API_KEY="your-secret-api-key"
export API_ENDPOINT="https://api.example.com"
```

**スクリプトでの利用：**

```bash
curl -H "Authorization: Bearer $API_KEY" $API_ENDPOINT/users
```

**解説：**
API キーやエンドポイントを環境変数として設定することで、コード内にハードコードを避けられます。

### 例5：言語ローカライゼーション

```bash
export LANG=ja_JP.UTF-8
export LC_ALL=ja_JP.UTF-8
```

**確認：**

```bash
locale
```

**出力例：**

```
LANG=ja_JP.UTF-8
LANGUAGE=
LC_CTYPE="ja_JP.UTF-8"
LC_NUMERIC="ja_JP.UTF-8"
...
```

**解説：**
システムの言語とロケールを設定します。日本語での出力が必要な場合に有効です。

## 永続的な環境変数の設定

`export` コマンドでシェルセッション中に設定した環境変数は、シェルを終了するとリセットされます。永続的に設定するには、シェルの設定ファイルに追加します。

### シェル設定ファイル

```
Bash : ~/.bashrc（対話的シェル）
       ~/.bash_profile（ログインシェル）

Zsh  : ~/.zshrc

全シェル : ~/.profile

システム全体 : /etc/environment
              /etc/profile
```

### ~/.bashrc に追加

```bash
echo 'export MY_VAR=hello' >> ~/.bashrc
```

**設定ファイルの内容：**

```bash
# ~/.bashrc
export PATH=/usr/local/bin:$PATH
export EDITOR=vim
export MY_VAR=hello
```

**設定を反映：**

```bash
source ~/.bashrc
```

または

```bash
. ~/.bashrc
```

**確認：**

```bash
echo $MY_VAR
```

**出力例：**

```
hello
```

**解説：**
設定ファイルに `export` コマンドを記述することで、シェル起動時に自動的に環境変数が設定されます。`source` コマンドで現在のセッションに反映させます。

### ~/.zshrc に追加（Zsh ユーザー）

```bash
cat >> ~/.zshrc << 'EOF'
export LANG=ja_JP.UTF-8
export EDITOR=vim
export PATH=/usr/local/bin:$PATH
EOF
```

**設定を反映：**

```bash
source ~/.zshrc
```

### システム全体に設定（管理者権限が必要）

```bash
sudo bash -c 'echo "export MY_VAR=hello" >> /etc/environment'
```

**確認：**

```bash
grep MY_VAR /etc/environment
```

**出力例：**

```
export MY_VAR=hello
```

**注意：** システム全体の設定は、すべてのユーザーとプロセスに適用されます。

## コマンド実行時の一時的な環境変数設定

特定のコマンド実行時に、一時的に環境変数を設定することができます。

### 基本形式

```bash
VAR_NAME=value command
```

**実践例：**

```bash
MY_VAR=hello echo $MY_VAR
```

**出力例：**

```
hello
```

**解説：**
このコマンドは、`echo` コマンドを実行する際に一時的に `MY_VAR` 環境変数に `hello` を設定します。`echo` コマンドが終了すると `MY_VAR` の設定は元に戻ります。

### 複数の環境変数を設定

```bash
VAR1=value1 VAR2=value2 command
```

**実践例：**

```bash
LANG=ja_JP.UTF-8 EDITOR=nano bash
```

**解説：**
複数の環境変数を同時に設定してコマンドを実行できます。この例では、日本語ロケールと nano エディタを指定した新しい bash シェルを起動します。

### スクリプト実行時の設定

```bash
DATABASE_URL=postgres://localhost/mydb python app.py
```

**解説：**
Python スクリプト実行時に `DATABASE_URL` 環境変数を設定します。スクリプト内で `os.environ['DATABASE_URL']` で参照できます。

## シェルスクリプト内での使用

### 例1：スクリプト内で環境変数を定義

```bash
#!/bin/bash

export SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export SCRIPT_NAME=$(basename "$0")
export LOG_FILE="$SCRIPT_DIR/script.log"

echo "Script directory: $SCRIPT_DIR"
echo "Script name: $SCRIPT_NAME"
echo "Log file: $LOG_FILE"
```

**実行例：**

```bash
bash ./script.sh
```

**出力例：**

```
Script directory: /home/user/scripts
Script name: script.sh
Log file: /home/user/scripts/script.log
```

**解説：**
スクリプト内で環境変数を定義し、その環境変数をスクリプト全体で利用できます。

### 例2：子スクリプトへの環境変数の継承

**親スクリプト（parent.sh）：**

```bash
#!/bin/bash
export MESSAGE="Hello from parent"
./child.sh
```

**子スクリプト（child.sh）：**

```bash
#!/bin/bash
echo "Received: $MESSAGE"
```

**実行例：**

```bash
bash parent.sh
```

**出力例：**

```
Received: Hello from parent
```

**解説：**
親スクリプトで設定した環境変数は、子スクリプトで自動的に利用可能になります。

### 例3：条件付き環境変数設定

```bash
#!/bin/bash

if [ "$1" = "production" ]; then
    export NODE_ENV=production
    export DEBUG=false
else
    export NODE_ENV=development
    export DEBUG=true
fi

echo "Environment: $NODE_ENV"
echo "Debug: $DEBUG"
```

**実行例：**

```bash
bash script.sh production
```

**出力例：**

```
Environment: production
Debug: false
```

**解説：**
条件に応じて異なる環境変数を設定します。

## export コマンドの応用

### 1. 関数を環境変数として設定

```bash
export -f my_function() {
    echo "Function called"
}
```

**解説：**
`-f` オプションで関数を環境変数として設定し、子シェルで利用可能にします。

### 2. 配列変数の設定

```bash
export MY_ARRAY=(value1 value2 value3)
echo ${MY_ARRAY[0]}  # value1
echo ${MY_ARRAY[1]}  # value2
```

**出力例：**

```
value1
value2
```

**解説：**
配列変数を環境変数として設定できます。

### 3. 変数展開での利用

```bash
export BASE_PATH=/usr/local
export BIN_PATH=$BASE_PATH/bin
export LIB_PATH=$BASE_PATH/lib

echo $BIN_PATH  # /usr/local/bin
echo $LIB_PATH  # /usr/local/lib
```

**出力例：**

```
/usr/local/bin
/usr/local/lib
```

**解説：**
既存の環境変数を利用して新しい環境変数を定義できます。

## ベストプラクティス

```
✅ 推奨される使い方

① 大文字で命名
   └─ export MY_VAR (× my_var)

② 説明的な名前を使用
   └─ export DATABASE_URL （× DB_URL）

③ パスの場合は絶対パス
   └─ export SCRIPT_DIR=/home/user/scripts

④ センシティブ情報は.env ファイルで管理
   └─ export $(cat .env)

⑤ スクリプト先頭で環境変数を定義
   └─ 初期化と依存関係を明確化

❌ 避けるべき方法

① ハードコードされた秘密情報
   └─ export API_KEY="secret123"をスクリプトに直書き

② 重複した定義
   └─ 複数ファイルで同じ変数を設定

③ 無制限に環境変数を増やす
   └─ 管理が複雑になる

④ グローバルスコープでの設定
   └─ テストやローカル開発に影響
```

## トラブルシューティング

### 問題1：環境変数が反映されない

**原因：** シェル設定ファイルの変更を反映していない

**解決方法：**

```bash
source ~/.bashrc
```

または再度ログイン

### 問題2：子プロセスで環境変数が利用できない

**原因：** `export` を使わずに通常の変数として設定している

```bash
❌ MY_VAR=hello  # 子プロセスで利用不可
✅ export MY_VAR=hello  # 子プロセスで利用可能
```

### 問題3：永続設定がすべてのシェルに反映されない

**原因：** 異なるシェル設定ファイルに追加している

**解決方法：**

```bash
# bash の場合
echo 'export MY_VAR=hello' >> ~/.bashrc

# zsh の場合
echo 'export MY_VAR=hello' >> ~/.zshrc

# 両方のシェルで共通
echo 'export MY_VAR=hello' >> ~/.profile
```

### 問題4：PATH に追加したディレクトリが最後に参照される

**原因：** PATH の末尾に追加している

```bash
❌ export PATH=$PATH:/new/path  # 末尾に追加（優先度低い）
✅ export PATH=/new/path:$PATH  # 先頭に追加（優先度高い）
```

## export コマンド集

| コマンド | 説明 |
|---------|------|
| `export VAR=value` | 環境変数を設定 |
| `echo $VAR` | 環境変数の値を表示 |
| `export VAR1=v1 VAR2=v2` | 複数の環境変数を設定 |
| `export -p` | すべての環境変数を表示 |
| `unset VAR` | 環境変数を削除 |
| `env` | 環境変数一覧を表示 |
| `env VAR=value command` | 一時的に環境変数を設定 |
| `source ~/.bashrc` | シェル設定ファイルを反映 |
| `export -f function_name` | 関数を環境変数化 |
| `env \| grep VAR` | 特定の環境変数を検索 |

## 関連コマンド

```bash
# 環境変数の確認・管理
env          # 環境変数一覧表示
printenv     # 環境変数の値を表示
unset        # 環境変数を削除

# シェル設定の反映
source       # シェル設定ファイルを読み込み

# 子プロセス実行
bash         # 新しいシェルを起動
sh           # POSIX シェルを起動

# スクリプト実行
chmod +x     # スクリプトに実行権限を付与
./script.sh  # スクリプトを実行（environment 継承）
```

## まとめ

**`export` コマンドの主要な機能：**

```
基本形式：
export VAR_NAME=value

使用場面：
├─ シェル環境の設定
├─ 子プロセスへの値の継承
├─ スクリプト実行環境の構築
└─ システム全体の設定

設定の永続化：
├─ ~/.bashrc
├─ ~/.zshrc
├─ ~/.profile
└─ /etc/environment

一時設定：
└─ VAR=value command 形式
```

`export` コマンドを使用することで、シェル環境の設定を柔軟に管理できます。これにより、シェルスクリプトや開発環境の構築が容易になります。

## 関連トピック

- [[ShellCommands]]：シェルコマンド全般
- [[BashScripting]]：Bash スクリプティング
- [[EnvironmentSetup]]：環境構築
- [[CommandLine]]：コマンドラインツール
