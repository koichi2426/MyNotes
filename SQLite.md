# SQLite

SQLiteは、軽量でサーバーレスのリレーショナルデータベース管理システム（RDBMS）です。

## 概要

SQLiteは、軽量でサーバーレスのリレーショナルデータベース管理システム（RDBMS）です。そのシンプルさと移植性により、モバイルアプリケーション、デスクトップソフトウェア、およびWebブラウザなど、様々なアプリケーションで広く利用されています。

### SQLiteの特徴

1. **軽量でシンプル**：
   - SQLiteは非常に軽量で、セットアップや管理が不要です。単一のライブラリファイルとして提供され、アプリケーションに組み込むことができます。

2. **サーバーレス**：
   - 他のデータベースシステムとは異なり、SQLiteはクライアント-サーバーモデルを使用しません。データベースは単一のファイルとして保存され、アプリケーションが直接そのファイルにアクセスします。

3. **高い移植性**：
   - SQLiteはC言語で書かれており、ほとんどのプラットフォーム（Windows、macOS、Linux、Android、iOSなど）で動作します。

4. **トランザクションサポート**：
   - ACID特性（Atomicity、Consistency、Isolation、Durability）をサポートしており、信頼性の高いデータ操作が可能です。

5. **自己完結型**：
   - 依存関係がほとんどなく、単一のデータベースファイルにすべてのデータを格納できます。

### データの保存先

SQLiteは、データを単一のファイルに保存します。このファイルは、アプリケーションのディレクトリ内に配置されることが一般的です。Railsアプリケーションの場合、デフォルトのデータベースファイルの場所は`config/database.yml`で設定されています。

例えば、Railsプロジェクトの`config/database.yml`ファイルは以下のように設定されることが多いです：

```yaml
development:
  adapter: sqlite3
  database: db/development.sqlite3
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  timeout: 5000

test:
  adapter: sqlite3
  database: db/test.sqlite3
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  timeout: 5000

production:
  adapter: sqlite3
  database: db/production.sqlite3
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  timeout: 5000
```

この設定では、各環境（development, test, production）ごとに異なるデータベースファイルが使用されます。

### 使用方法

SQLiteを使用する基本的な流れは以下のとおりです。

1. **インストール**：
   - SQLiteは多くのシステムにプリインストールされていますが、インストールされていない場合は公式サイトからダウンロードできます。

2. **データベースの作成**：
   - SQLiteのデータベースは単一のファイルとして保存されるため、簡単に作成できます。

3. **データベースの操作**：
   - SQL（Structured Query Language）を使用してデータの挿入、更新、削除、検索を行います。

4. **管理とメンテナンス**：
   - データのバックアップ、最適化、インデックスの作成などの管理作業が必要です。

## 基本操作

SQLiteは、軽量でサーバーレスのリレーショナルデータベース管理システム（RDBMS）であり、使いやすさとシンプルさから多くのプロジェクトで利用されています。ここでは、SQLiteの基本的な操作について紹介します。

### 1. SQLiteのインストール

SQLiteは多くのシステムにプリインストールされていますが、インストールされていない場合は公式サイトからダウンロードしてインストールできます。

#### macOS/Linuxの場合

```bash
sudo apt-get install sqlite3   # Debian系
sudo yum install sqlite        # RedHat系
brew install sqlite            # macOS
```

#### Windowsの場合

公式サイトからインストーラーをダウンロードしてインストールします。

### 2. SQLiteシェルの起動

SQLiteシェルを起動してデータベースファイルを作成します。

```bash
sqlite3 example.db
```

このコマンドを実行すると、`example.db`という名前のデータベースファイルが作成され、SQLiteシェルが起動します。

### 3. テーブルの作成

SQLiteシェル内でテーブルを作成します。

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER
);
```

### 4. データの挿入

データを挿入するには、`INSERT INTO`文を使用します。

```sql
INSERT INTO users (name, email, age) VALUES ('Alice', 'alice@example.com', 30);
INSERT INTO users (name, email, age) VALUES ('Bob', 'bob@example.com', 25);
```

### 5. データの取得

データを取得するには、`SELECT`文を使用します。

#### 全データを取得

```sql
SELECT * FROM users;
```

#### 特定の条件でデータを取得

例えば、年齢が25歳以上のユーザーを取得するには：

```sql
SELECT * FROM users WHERE age >= 25;
```

### 6. データの更新

既存のデータを更新するには、`UPDATE`文を使用します。

```sql
UPDATE users SET email = 'newbob@example.com' WHERE name = 'Bob';
```

### 7. データの削除

データを削除するには、`DELETE`文を使用します。

```sql
DELETE FROM users WHERE name = 'Alice';
```

### 8. テーブル構造の確認

テーブルの構造を確認するには、`PRAGMA table_info`コマンドを使用します。

```sql
PRAGMA table_info(users);
```

### 9. インデックスの作成

インデックスを作成して検索速度を向上させるには、`CREATE INDEX`文を使用します。

```sql
CREATE INDEX idx_users_email ON users(email);
```

### 10. トランザクション

トランザクションを使用して、一連の操作をまとめて実行することができます。トランザクションを開始するには、`BEGIN TRANSACTION`を使用し、コミットまたはロールバックを行います。

#### トランザクションの開始

```sql
BEGIN TRANSACTION;
```

#### コミット

```sql
COMMIT;
```

#### ロールバック

```sql
ROLLBACK;
```

### 11. データのエクスポートとインポート

#### データのエクスポート

テーブルのデータをCSV形式でエクスポートするには、`.mode csv`および`.output`コマンドを使用します。

```sql
.mode csv
.output users.csv
SELECT * FROM users;
.output stdout
```

#### データのインポート

CSVファイルからデータをインポートするには、`.mode csv`および`.import`コマンドを使用します。

```sql
.mode csv
.import users.csv users
```

### 12. データベースのバックアップ

データベース全体をバックアップするには、`.backup`コマンドを使用します。

```sql
.backup 'backup.db'
```

### 13. データベースのクローズ

データベースを閉じるには、`.quit`コマンドを使用します。

```sql
.quit
```

## まとめ

SQLiteは、軽量でサーバーレスなRDBMSとして多くの用途で利用されています。そのシンプルさと移植性により、小規模なアプリケーションやデスクトップソフトウェア、モバイルアプリケーションに最適です。SQLiteを効果的に使用するためには、その特徴を理解し、適切な設計と管理を行うことが重要です。

基本的な操作をマスターすることで、SQLiteを効果的に利用し、データの管理や操作をスムーズに行うことができます。これらのコマンドを活用して、SQLiteの利便性を最大限に引き出してください。
