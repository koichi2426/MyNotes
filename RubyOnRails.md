# RubyOnRails

Ruby on Rails（Rails）は、Webアプリケーションを迅速かつ簡単に開発するためのオープンソースフレームワークです。

## 概要

### はじめに

Ruby on Rails（以下Rails）は、Webアプリケーションを迅速かつ簡単に開発するためのオープンソースフレームワークです。Rubyプログラミング言語をベースにしており、シンプルで直感的なコードを書くことができるため、開発者に非常に人気があります。

### 特徴

#### MVCアーキテクチャ

RailsはModel-View-Controller（MVC）アーキテクチャに基づいています。このアーキテクチャにより、アプリケーションのビジネスロジック、表示ロジック、データ管理を明確に分離することができます。

- **Model**: データベースのテーブルと対応し、データの操作を行います
- **View**: ユーザーに表示するUIを担当します
- **Controller**: ユーザーの入力を処理し、ModelとViewの連携を管理します

#### DRY（Don't Repeat Yourself）

RailsはDRY原則に従って設計されており、同じコードを何度も書くことなく、再利用可能なコンポーネントを作成できます。これにより、コードの重複を避け、保守性を向上させることができます。

#### コンベンションより設定

Railsは「設定よりも規約」を採用しており、デフォルト設定を提供することで、開発者が設定ファイルを手動で編集する必要を最小限に抑えます。これにより、開発の迅速化が可能となります。

#### 強力なジェネレーター

Railsには、コードの雛形を自動生成するジェネレーターが多数用意されています。これにより、CRUD（Create, Read, Update, Delete）操作やスキャフォールディングなどの標準的な機能を素早く実装できます。

### 基本構成要素

#### ActiveRecord

ActiveRecordは、RailsにおけるORM（Object-Relational Mapping）ライブラリです。データベースのテーブルとRubyのクラスをマッピングし、データベース操作を簡素化します。

#### ActionController

ActionControllerは、MVCパターンのコントローラー部分を担当します。ユーザーのリクエストを受け取り、適切なアクションを実行します。

#### ActionView

ActionViewは、アプリケーションの表示ロジックを担当します。ERB（Embedded Ruby）テンプレートエンジンを使用して、動的なHTMLコンテンツを生成します。

#### ActiveSupport

ActiveSupportは、Railsに組み込まれている拡張ライブラリの集合体です。日付や時間の操作、文字列操作、通知システムなど、様々な便利機能を提供します。

## 基本操作

### 新規プロジェクト作成

Railsを使用して新しいプロジェクトを作成するには、以下のコマンドを実行します。

```bash
rails new myapp
cd myapp
```

参考: [Rails をはじめよう - Railsガイド](https://railsguides.jp/getting_started.html)

### スキャフォールディング

スキャフォールディングを使用して、基本的なCRUD機能を自動生成します。

```bash
rails generate scaffold Article title:string body:text
rails db:migrate
```

### サーバーの起動

Railsサーバーを起動して、アプリケーションをローカルで実行します。

```bash
rails server
```

ブラウザで `http://localhost:3000` にアクセスすると、生成されたArticleリソースを確認できます。

## データベース

### テーブル作成

#### 手順

Railsでテーブルを定義するための手順は、以下のステップに従って進めます。

**1. モデルの作成**

まず、Railsジェネレーターを使用してモデルを作成します。モデルはテーブルの構造を定義するためのものであり、対応するマイグレーションファイルも自動的に生成されます。

```bash
rails generate model モデル名 カラム名:データ型 カラム名:データ型 ...
```

例：ユーザー（User）モデルを作成し、名前（name）とメールアドレス（email）カラムを追加します。

```bash
rails generate model User name:string email:string
```

これにより、`app/models/user.rb` ファイルと `db/migrate/YYYYMMDDHHMMSS_create_users.rb` というマイグレーションファイルが生成されます。

**2. マイグレーションファイルの編集**

マイグレーションファイルを開き、テーブルの定義を確認および編集します。

```ruby
# db/migrate/YYYYMMDDHHMMSS_create_users.rb
class CreateUsers < ActiveRecord::Migration[6.1]
  def change
    create_table :users do |t|
      t.string :name
      t.string :email

      t.timestamps
    end
  end
end
```

**3. マイグレーションの実行**

マイグレーションを実行して、データベースにテーブルを作成します。

```bash
rails db:migrate
```

**4. モデルの編集**

生成されたモデルファイルを開き、必要に応じてバリデーションや関連付けを追加します。

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # バリデーションの追加
  validates :name, presence: true
  validates :email, presence: true, uniqueness: true

  # 他のモデルとの関連付けの追加
  # has_many :posts
  # belongs_to :account
end
```

**5. テーブルの確認**

Railsコンソールを使用して、テーブルが正しく作成されているか確認します。

```bash
rails console
```

コンソールが開いたら、以下のコマンドを実行してテーブルの内容を確認します。

```ruby
# テーブルの一覧を表示
ActiveRecord::Base.connection.tables

# Userモデルの最初のレコードを表示
User.first
```

参考: [Railsで新しくテーブルを作成するときの基本的な流れ](https://zenn.dev/tmasuyama1114/articles/rails-create-table)

### テーブルの関連付け

Railsでは、データベースのテーブル同士の関連付け（アソシエーション）を簡単に設定できます。

#### モデルとマイグレーションの作成

**Userモデルの作成**：

```bash
rails generate model User name:string email:string
```

**Postモデルの作成**：

```bash
rails generate model Post title:string body:text user:references
```

`user:references` は、`Post` モデルに `user_id` という外部キーを追加し、`User` モデルとの関連付けを自動的に設定します。

#### マイグレーションファイルの確認

**ポストマイグレーションファイル**：

```ruby
# db/migrate/YYYYMMDDHHMMSS_create_posts.rb
class CreatePosts < ActiveRecord::Migration[6.1]
  def change
    create_table :posts do |t|
      t.string :title
      t.text :body
      t.references :user, null: false, foreign_key: true

      t.timestamps
    end
  end
end
```

#### モデルの編集

**Userモデル**：

```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_many :posts

  validates :name, presence: true
  validates :email, presence: true, uniqueness: true
end
```

**Postモデル**：

```ruby
# app/models/post.rb
class Post < ApplicationRecord
  belongs_to :user

  validates :title, presence: true
  validates :body, presence: true
end
```

#### データベースの確認

```ruby
# ユーザーを作成
user = User.create(name: "John Doe", email: "john@example.com")

# ポストを作成し、ユーザーに関連付ける
post = Post.create(title: "First Post", body: "This is the body of the first post", user: user)

# 関連付けを確認
user.posts
post.user
```

#### アソシエーションの種類

1. **`belongs_to`**: モデルが他のモデルに属していることを示します。外部キーを持ちます
2. **`has_many`**: モデルが他のモデルを複数持つことを示します
3. **`has_one`**: モデルが他のモデルを一つだけ持つことを示します
4. **`has_many :through`**: 多対多の関係を表現するために中間テーブルを使用します
5. **`has_and_belongs_to_many`**: 中間テーブルを直接使用して多対多の関係を表現します

参考: [【Rails】references型について - Qiita](https://qiita.com/mmaumtjgj/items/cdc76572d392957c4299)

### データベース操作

#### CRUD操作

RailsにおけるCRUD操作は、データベース内の情報を作成(Create)、読み取り(Read)、更新(Update)、削除(Delete)するための基本的な操作です。

**Create (作成)**:

```ruby
# 新しいレコードを作成して保存
ModelName.create(attributes)

# 例: 新しいブログポストを作成
Post.create(title: "新しい投稿", content: "これは新しい投稿です。")
```

**Read (読み取り)**:

```ruby
# IDで単一のレコードを取得
ModelName.find(id)

# 条件に合致する複数のレコードを取得
ModelName.where(conditions)

# 例:
Post.find(1)
Post.where(title: "Rails")
```

**Update (更新)**:

```ruby
# 特定のレコードを更新
instance.update(attributes)

# 例:
post = Post.find(1)
post.update(title: "更新された投稿", content: "これは更新された投稿です。")
```

**Delete (削除)**:

```ruby
# 特定のレコードを削除
instance.destroy

# 例:
post = Post.find(1)
post.destroy
```

#### 関連テーブルの参照方法

`references`を使用して関連づけられたテーブルを参照する方法は、Active Recordの関連付けを通じて行います。

```ruby
# Postモデル
class Post < ApplicationRecord
  belongs_to :user # Userモデルに属することを示す
end

# Userモデル
class User < ApplicationRecord
  has_many :posts # 複数のPostモデルを持つことを示す
end
```

```bash
rails generate model Post title:string content:text user:references
```

```ruby
# ユーザーに関連付けられたポストの作成
user = User.first
post = user.posts.create(title: "New Post", content: "This is a new post.")

# 特定のポストに関連付けられたユーザーの取得
post = Post.first
user = post.user
```

#### コンソールからデータベース操作

参考: [【Webサービス開発】Ruby on Railsでデータ操作をしてみよう](https://pikawaka.com/curriculums/web-service-development/rails-active-record)

#### MySQLサーバー接続

**1. MySQLのインストール**

Ubuntuの場合：

```bash
sudo apt-get update
sudo apt-get install mysql-server
```

MacOSの場合（Homebrewを使用）：

```bash
brew install mysql
brew services start mysql
```

**2. MySQLサーバーの設定**

```bash
sudo mysql_secure_installation
mysql -u root -p
```

**3. データベースとユーザーの作成**

```sql
CREATE DATABASE myapp_development;
CREATE DATABASE myapp_test;
CREATE DATABASE myapp_production;

CREATE USER 'myapp_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON myapp_development.* TO 'myapp_user'@'localhost';
GRANT ALL PRIVILEGES ON myapp_test.* TO 'myapp_user'@'localhost';
GRANT ALL PRIVILEGES ON myapp_production.* TO 'myapp_user'@'localhost';
FLUSH PRIVILEGES;
```

**4. Railsアプリケーションの設定**

Gemfileの編集：

```ruby
# Gemfile
gem 'mysql2', '>= 0.4.4'
```

```bash
bundle install
```

database.ymlの編集：

```yaml
# config/database.yml
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  username: myapp_user
  password: <%= ENV['MYAPP_DATABASE_PASSWORD'] %>
  host: localhost
  port: 3306
  ssl_mode: :disabled

development:
  <<: *default
  database: myapp_development

test:
  <<: *default
  database: myapp_test

production:
  <<: *default
  database: myapp_production
  username: myapp_user
  password: <%= ENV['MYAPP_DATABASE_PASSWORD'] %>
```

環境変数の設定：

```ruby
# Gemfile
gem 'dotenv-rails', groups: [:development, :test]
```

```bash
bundle install
```

`.env` ファイルを作成：

```
# .env
MYAPP_DATABASE_PASSWORD=your_password
```

**5. データベースの作成**

```bash
rails db:create
rails db:migrate
```

**6. 接続の確認**

```bash
rails console
```

```ruby
ActiveRecord::Base.connection
```

参考: [【Rails】【DB】database.yml - Qiita](https://qiita.com/ryouya3948/items/ba3012ba88d9ea8fd43d)

#### 既存のテーブルにカラムを追加する手順

**手順1: マイグレーションファイルの生成**

```bash
rails generate migration AddPlanToUsers plan:integer
```

生成されたファイル：

```ruby
class AddPlanToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :plan, :integer, default: 0, null: false
  end
end
```

**手順2: マイグレーションの実行**

```bash
rails db:migrate
```

**手順3: スキーマの確認**

`db/schema.rb`ファイルが自動的に更新されます。

**手順4: バリデーションの追加**

```ruby
class User < ApplicationRecord
  validates :plan, inclusion: { in: [0, 1, 2, 3] }
end
```

## API作成

### ルーティング

config/routes.rbにAPIのルートを追加します。

```ruby
Rails.application.routes.draw do
  post 'urls', to: 'urls#create'
end
```

**コードの解説**

- `post`: HTTPメソッド`POST`がリクエストに使用されることを示します
- `'urls'`: URLのパスを指定します（例: `http://localhost:3000/urls`）
- `to`: どのコントローラとアクションにルーティングするかを示します
- `'urls#create'`: `urls`コントローラの`create`アクションを指定します

### コントローラー作成

Rails（Ruby on Rails）で新しいコントローラを作成するには、コマンドラインから `rails generate controller` コマンドを使用します。

形式：

```ruby
rails generate controller [コントローラ名] [アクション名1 アクション名2 ...]
```

例：

```bash
rails generate controller Users new edit
```

このコマンドにより以下のファイルが生成されます：

- `app/controllers/users_controller.rb`（コントローラファイル）
- `app/views/users/new.html.erb`（newアクションのビューファイル）
- `app/views/users/edit.html.erb`（editアクションのビューファイル）
- テストファイル、ヘルパーファイル、JavaScript、CSSファイル（設定によります）

**オプションと注意点**

- モデルと異なり、コントローラ名は通常、複数形で命名します（例: Users）
- アクション名は省略可能です。省略した場合、コントローラファイルのみが生成されます
- コントローラの生成を取り消す場合は、以下のコマンドを使用します：

```ruby
rails destroy controller [コントローラ名]
```

## 定期実行

### UbuntuサーバーでRakeファイルを定期実行する手順

Rakeタスクを定期実行することは、定期的なメンテナンスやデータ処理を自動化するのに便利です。ここでは、`cron`と`whenever` gemを使った方法を紹介します。

#### 方法 1: `cron`を使う

**ステップ 1: Rakeタスクの確認**

```bash
cd /path/to/your/app
bundle exec rake fetch_scores:execute
```

**ステップ 2: `cron`設定ファイルの編集**

Vimエディターの選択：

```bash
select-editor
```

`2`を選択してVimを使用します。

`cron`設定ファイルの編集：

```bash
crontab -e
```

設定を追加（毎時間0分に実行する例）：

```
0 * * * * /bin/bash -l -c 'cd /path/to/your/app && bundle exec rake fetch_scores:execute >> /path/to/your/app/log/fetch_scores.log 2>&1'
```

実際の設定例：

```
* * * * * export PATH="$HOME/.rbenv/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:$PATH" && eval "$(rbenv init -)" && cd /home/ubuntu/url_performance_api && bundle exec rake fetch_scores:execute >> /home/ubuntu/url_performance_api/cron.log 2>&1
```

各部分の解説：

- `0 * * * *`：毎時間の0分に実行
- `/bin/bash -l -c '...'`：bashシェルでコマンドを実行
- `cd /path/to/your/app`：アプリケーションのディレクトリに移動
- `bundle exec rake fetch_scores:execute`：Rakeタスクを実行
- `>> /path/to/your/app/log/fetch_scores.log 2>&1`：実行結果をログファイルに出力

保存して閉じる：Vimで`Esc`キーを押してから`:wq`と入力してEnterキーを押します。

**ステップ 3: `cron`ジョブの確認**

```bash
crontab -l
```

#### 環境の指定

特定の環境（例えば、プロダクション環境）でタスクを実行する場合は、`RAILS_ENV=production`を指定します。

```bash
RAILS_ENV=production bundle exec rake fetch_scores:execute
```

参考: [【Rails】定期実行をしてみよう！（whenever, cron）](https://blog.to-ko-s.com/rails-periodic-execution/)

## Railsの`database.yml`の書き方ガイド

Railsの`database.yml`ファイルは、アプリケーションのデータベース設定を管理する重要なファイルです。

### `database.yml`の基本構成

`database.yml`ファイルは、Railsプロジェクトの`config`ディレクトリ内にあります。通常、`development`、`test`、`production`の3つの環境で異なる設定を行います。

```yaml
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  username: dbuser
  password: <%= ENV["DATABASE_PASSWORD"] %>
  host: localhost
  port: 3306

development:
  <<: *default
  database: myapp_development

test:
  <<: *default
  database: myapp_test

production:
  <<: *default
  database: myapp_production
  username: myapp
  password: <%= ENV["MYAPP_DATABASE_PASSWORD"] %>
  host: db.production.example.com
  pool: 10
```

### セクションごとの解説

#### `default`セクション

- **adapter**: 使用するデータベースの種類を指定（例: `mysql2`、`postgresql`、`sqlite3`）
- **encoding**: データベースの文字エンコーディングを指定（例: `utf8mb4`）
- **pool**: データベースコネクションプールのサイズを指定。デフォルトは`5`
- **username**: データベース接続に使用するユーザー名
- **password**: データベース接続に使用するパスワード。環境変数を使って設定することが推奨されます
- **host**: データベースサーバーのホスト名やIPアドレス
- **port**: データベースサーバーのポート番号

#### 環境変数の使用

セキュリティの観点から、パスワードやユーザー名などの機密情報はコード内に直接書かず、環境変数を使用することが推奨されます。

```yaml
password: <%= ENV["DATABASE_PASSWORD"] %>
```

環境変数は、`dotenv` や他の環境変数管理ツールを使用して設定できます。

#### 他の一般的なオプション

- **reconnect**: データベース接続が切れたときに自動的に再接続するかどうかを指定。通常は `true` に設定します
- **timeout**: データベース接続のタイムアウト時間（ミリ秒）を指定

## RailsでのセキュアなAPIキー管理：`credentials.yml.enc`と`master.key`の活用方法

### はじめに

Webアプリケーションの開発では、APIキーやデータベースのパスワードなど、セキュリティに関わる機密情報をどのように管理するかが重要です。Railsでは、これらの機密情報を安全に管理するために、`credentials.yml.enc` と `master.key` を使用することが推奨されています。

### `credentials.yml.enc` と `master.key` の概要

#### `credentials.yml.enc` とは？

`credentials.yml.enc` は、Rails 5.2以降で導入された機密情報を暗号化して管理するためのファイルです。このファイルは暗号化されているため、リポジトリにコミットしてもセキュリティが保たれます。復号するためには `master.key` が必要です。

#### `master.key` とは？

`master.key` は、`credentials.yml.enc` を復号するために使用されるキーです。このキーは、開発チーム内で共有する必要があり、リポジトリにはコミットしません。通常、`config/master.key` に保存されます。

### `credentials.yml.enc` の設定方法

#### 1. `credentials.yml.enc` の作成・編集

```bash
EDITOR="code --wait" rails credentials:edit
```

コマンドを実行すると、以下のようなYAML形式のファイルが開きます。

```yaml
# example credentials.yml.enc
stripe:
  secret_key: sk_test_XXXXXXXXXXXXXXXXXXXX
  publishable_key: pk_test_XXXXXXXXXXXXXXXXXXXX
aws:
  access_key_id: YOUR_ACCESS_KEY_ID
  secret_access_key: YOUR_SECRET_ACCESS_KEY
```

実際の設定例：

```yaml
stripe:
  secret_key: pk_test_51PSW8kRrToHo46OJaSzrOAmflB44sGwTClAg7QaZYRc6ZgoNKO5b9eFePNZ8OABRM9JWCYN5gbjSvI38UWWFJ2CE00GjKD43qH
  publishable_key: pk_test_51PSW8kRrToHo46OJaSzrOAmflB44sGwTClAg7QaZYRc6ZgoNKO5b9eFePNZ8OABRM9JWCYN5gbjSvI38UWWFJ2CE00GjKD43qH
```

#### 2. `master.key` の管理

`master.key` は、通常 `config/master.key` に保存されます。このキーは非常に重要であり、リポジトリにコミットしないよう `.gitignore` に含める必要があります。

```bash
echo 'config/master.key' >> .gitignore
```

#### 3. APIキーの読み込み

アプリケーションでAPIキーを使用する際は、以下のように`Rails.application.credentials` を使って読み込みます。

例：StripeのAPIキーを設定する

```ruby
# config/initializers/stripe.rb
Stripe.api_key = Rails.application.credentials.dig(:stripe, :secret_key)
```

#### 4. 環境ごとの設定

Rails 6以降では、環境ごとに異なるcredentialsを設定することができます。

```bash
EDITOR="code --wait" rails credentials:edit --environment=production
```

これにより、`config/credentials/production.yml.enc` のように環境ごとのcredentialsが作成されます。

### `credentials.yml.enc` の利用ケース

- **本番環境でのAPIキー管理**: StripeやAWSなどのAPIキーを安全に管理
- **データベースのパスワード管理**: 複数の環境で異なるデータベースのパスワードを安全に管理
- **第三者サービスの認証情報**: 外部サービスとの連携に必要な認証情報を安全に管理

### まとめ

Railsの`credentials.yml.enc`と`master.key`を利用することで、アプリケーションにおけるAPIキーやその他の機密情報を安全に管理することができます。開発チーム内でのキーの共有や、本番環境でのセキュリティ対策において、これらの機能を活用しましょう。

## まとめ

Ruby on Railsは、シンプルかつ強力なフレームワークであり、Webアプリケーション開発を効率化します。MVCアーキテクチャ、DRY原則、強力なジェネレーターなどの特徴を活かして、迅速に高品質なアプリケーションを構築することができます。初心者から経験豊富な開発者まで、幅広い層に支持されているRailsをぜひ活用してみてください。
