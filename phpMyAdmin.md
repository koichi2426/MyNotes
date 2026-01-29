# phpMyAdmin

MySQLをGUIで管理するWebアプリケーション

## 概要

phpMyAdminは、ウェブブラウザ上でMySQLを管理するためのアプリケーションです。本来MySQLはCUI（コマンドラインインターフェース）ですが、phpMyAdminは**GUI**（グラフィカルユーザーインターフェース）であるため、MySQLを簡単に操作できます。

## 起動方法

[[XAMPP]]から起動します。

### 関連リンク
- [XAMPP](https://www.notion.so/XAMPP-551cd31d16984d3296beeebf332d1d42?pvs=21)

## 操作方法

### データベースの作成

1. **新規データベースの作成**
   - phpMyAdminのトップページで「新規作成」タブを選択
   - データベース名を入力（例: `blog_app`）
   - 照合順序を選択（通常は `utf8mb4_general_ci` を推奨）
   - 「作成」ボタンをクリック

2. **作成の確認**
   - 左側のサイドバーに新しく作成したデータベース名が表示される
   - データベース名をクリックすると、そのデータベース内のテーブル一覧画面に移動

### phpMyAdminで直接データベースを操作する

phpMyAdminを使用すると、ブラウザ上でデータベースの作成、テーブルの管理、データの挿入・更新・削除などを視覚的に行うことができます。

**参考資料:**
- [ゼロから始めるPHP講座Vol21 phpMyAdminの基礎と使い方①](https://blog.codecamp.jp/phpmyadmin01)
- [ゼロから始めるPHP講座Vol22 phpMyAdminの基礎と使い方②](https://blog.codecamp.jp/phpmyadmin02)

## DBMS（データベース管理システム）

リレーショナルデータベースとRDBMSについての理解も重要です。

**参考資料:**
- [ゼロから始めるPHP講座Vol20 リレーショナルデータベースとRDBMS](https://blog.codecamp.jp/php_database02)

## PHPからのデータベース接続

PHPファイルからphpMyAdminで作成したデータベースへの接続方法は以下の手順で行います。

### 手順1: データベース接続情報の取得

phpMyAdminで作成したデータベースに接続するために、以下の情報が必要です：
- ホスト名
- データベース名
- ユーザー名
- パスワード

これらの情報は通常、phpMyAdminの設定ファイル（`config.inc.php`）やユーザーが作成したデータベース情報から取得します。

### 手順2: PHPでの接続コードの作成

MySQLiを使用してデータベースに接続するコード例：

```php
<?php
// データベース接続情報
$servername = "localhost"; // データベースのホスト名
$username = "ユーザー名"; // データベースのユーザー名
$password = "パスワード"; // データベースのパスワード
$dbname = "データベース名"; // データベース名

// MySQLiオブジェクトの作成
$conn = new mysqli($servername, $username, $password, $dbname);

// 接続の確認
if ($conn->connect_error) {
    die("データベース接続エラー: " . $conn->connect_error);
} else {
    echo "データベース接続成功";
}

// データベースへのクエリや操作を行うことができる
?>
```

### コードの解説

- **`$servername`**: データベースのホスト名（通常は "localhost"）
- **`$username`**: データベースのユーザー名
- **`$password`**: データベースのパスワード
- **`$dbname`**: 接続するデータベース名
- **接続確認**: 接続が成功すれば「データベース接続成功」というメッセージが表示され、失敗した場合はエラーメッセージが表示されます

## 参考リソース

- [[Q&A] PHPファイルからphpMyAdminにデータベース接続する方法 - Qiita](https://qiita.com/IwataRisa/questions/634df267866cea66363d)

## まとめ

phpMyAdminは、[[MySQL]]データベースを視覚的に管理できる強力なツールです。[[PHP]]開発において、データベースの管理やテスト、デバッグ作業を効率化するために広く使用されています。
