# CORS: クロスオリジンリソース共有の完全ガイド

## 概要

CORS（コース）とは、「Cross-Origin Resource Sharing」の略で、日本語では「クロスオリジンリソース共有」と呼ばれます。これは、ウェブブラウザが異なるオリジン（ドメイン、プロトコル、ポートが異なるサーバー）からのリソースをリクエストする際に発生するセキュリティ制限を管理する仕組みです。

### CORSが必要な理由

普段、ウェブブラウザはセキュリティのために、異なるオリジン（簡単に言うと、異なるウェブサイトやサーバー）からのデータのやり取りを制限しています。例えば、`http://example.com`というサイトが、`http://another-site.com`という全く別のサイトからデータを取得しようとする場合、ブラウザはセキュリティ上の理由からリクエストをブロックします。

ここで「オリジン」とは、以下の3つの要素の組み合わせを指します：
- **プロトコル**: `http` または `https`
- **ドメイン名**: `example.com` など
- **ポート番号**: `80`、`443` など

これらがすべて同じでないと、異なるオリジンと見なされます。

### CORSの重要性

モダンなウェブアプリケーションでは、異なるオリジン間でのデータ共有が必要になることがよくあります。例えば：
- フロントエンド（React、Vue.jsなど）がバックエンドAPIに別のドメインからアクセス
- 複数のマイクロサービス間の通信
- 異なるサブドメイン間のデータ共有

CORSを適切に設定することで、これらの通信をセキュアに実現できます。

## CORSの仕組み

### シンプルリクエスト vs プリフライトリクエスト

#### シンプルリクエスト

以下の条件をすべて満たすリクエストはシンプルリクエストと呼ばれます：
- **メソッド**: `GET`、`HEAD`、`POST` のいずれか
- **ヘッダー**: `Accept`、`Accept-Language`、`Content-Language`、`Content-Type` のみ
- **Content-Type**: `application/x-www-form-urlencoded`、`multipart/form-data`、`text/plain` のいずれか

#### プリフライトリクエスト

シンプルリクエストの条件を満たさない場合、ブラウザは実際のリクエストの前に`OPTIONS`メソッドでプリフライトリクエストを送信します。

```
OPTIONS /api/users HTTP/1.1
Host: api.example.com
Origin: https://example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

サーバーがこれに対して適切なCORSヘッダーで応答することで、実際のリクエストが許可されます。

## CORSヘッダーの詳細

### レスポンスヘッダー

#### 1. Access-Control-Allow-Origin

**説明**: リソースにアクセス可能なオリジンを指定します

```
Access-Control-Allow-Origin: https://example.com
```

または、すべてのオリジンを許可する場合：

```
Access-Control-Allow-Origin: *
```

**注意**: クレデンシャル付きリクエストを許可する場合は、`*` ではなく具体的なオリジンを指定する必要があります

#### 2. Access-Control-Allow-Methods

**説明**: クライアントが使用可能なHTTPメソッドを指定します

```
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
```

#### 3. Access-Control-Allow-Headers

**説明**: クライアントがリクエストで使用可能なHTTPヘッダーを指定します

```
Access-Control-Allow-Headers: Content-Type, Authorization, X-Custom-Header
```

#### 4. Access-Control-Allow-Credentials

**説明**: クッキーや認証ヘッダーを含むリクエストを許可するかを指定します

```
Access-Control-Allow-Credentials: true
```

**重要**: `Access-Control-Allow-Origin: *` と `Access-Control-Allow-Credentials: true` は同時に使用できません

#### 5. Access-Control-Expose-Headers

**説明**: ブラウザがクライアントに公開することを許可するレスポンスヘッダーを指定します

```
Access-Control-Expose-Headers: Content-Length, X-Custom-Header
```

#### 6. Access-Control-Max-Age

**説明**: プリフライトリクエストの結果をキャッシュできる期間（秒単位）を指定します

```
Access-Control-Max-Age: 600
```

## RailsでのCORS設定

### ステップ1: rack-corsのインストール

Gemfileに以下を追加：

```ruby
gem 'rack-cors'
```

その後、bundle installを実行：

```bash
bundle install
```

### ステップ2: config/application.rbの設定

```ruby
module YourApp
  class Application < Rails::Application
    # CORS設定の追加
    config.middleware.insert_before 0, Rack::Cors do
      allow do
        origins 'example.com'
        resource '*',
          headers: :any,
          methods: [:get, :post, :put, :patch, :delete, :options, :head],
          credentials: true
      end
    end
  end
end
```

### 設定例の詳細

| 項目 | 説明 |
|------|------|
| `origins 'example.com'` | 許可するオリジンを指定 |
| `resource '*'` | すべてのパスを対象 |
| `headers: :any` | すべてのヘッダーを許可 |
| `methods: [...]` | 許可するHTTPメソッド |
| `credentials: true` | クレデンシャル付きリクエストを許可 |

### 複数のオリジンを許可する場合

```ruby
config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'example.com', 'www.example.com', 'localhost:3000'
    resource '*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head]
  end

  allow do
    origins 'api.example.com'
    resource '/api/*',
      headers: :any,
      methods: [:get, :post]
  end
end
```

### 設定の確認

ブラウザの開発者ツール（F12キー）で、Networkタブを開いてレスポンスヘッダーを確認：

```
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Credentials: true
```

## ApacheでのCORS設定

### ステップ1: mod_headersモジュールの有効化

```bash
sudo a2enmod headers
sudo systemctl restart apache2
```

### ステップ2: VirtualHost設定の追加

```apache
<VirtualHost *:443>
    ServerName www.example.com
    DocumentRoot /home/ubuntu/web_app/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.example.com/privkey.pem

    <IfModule mod_headers.c>
        Header always set Access-Control-Allow-Origin "https://www.example.com"
        Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header always set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header always set Access-Control-Allow-Credentials "true"
    </IfModule>

    # Railsアプリケーションへのプロキシ設定
    ProxyPass /api http://localhost:3001/
    ProxyPassReverse /api http://localhost:3001/

    # プリフライトリクエスト処理
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### HTTPからHTTPSへのリダイレクト設定

```apache
<VirtualHost *:80>
    ServerName www.example.com
    DocumentRoot /home/ubuntu/web_app/build

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### ステップ3: 設定の確認

```bash
# 構文確認
sudo apache2ctl configtest

# 再起動
sudo systemctl restart apache2
```

## CORS設定の検証

### curlコマンドでの確認

プリフライトリクエストをシミュレート：

```bash
curl -X OPTIONS -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -i https://www.example.com/api/users
```

**正常な応答例:**

```
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, OPTIONS, PUT, DELETE, PATCH
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Credentials: true
```

### ブラウザの開発者ツールでの確認

1. F12キーで開発者ツールを開く
2. NetworkタブでXHRフィルターを選択
3. API呼び出しを実行
4. リクエストをクリックしてヘッダーを確認
5. レスポンスヘッダーにACLヘッダーが含まれているか確認

## トラブルシューティング

### CORS設定が反映されない場合

#### 問題: 複数の設定ファイルの競合

**症状**: curlで確認すると違うオリジンが返される

```bash
# 設定ファイルで https://example.com を指定しているのに
# http://example.com が返される
```

**原因**: 複数のApache設定ファイルで競合している可能性

**解決方法**:

1. **有効な設定ファイルを確認**:

```bash
ls /etc/apache2/sites-enabled/
```

2. **すべての設定ファイルを確認**:

```bash
grep -r "Access-Control-Allow-Origin" /etc/apache2/
```

3. **不要な設定ファイルを無効化**:

```bash
sudo a2dissite default-ssl
sudo a2dissite 000-default
sudo systemctl restart apache2
```

4. **正しい設定ファイルのみを有効化**:

```bash
sudo a2ensite rails_app
sudo systemctl restart apache2
```

### ヘッダー設定が反映されない場合

**症状**: `Header set` でなく `Header always set` を使用していない

**解決方法**: 以下を使用：

```apache
Header always set Access-Control-Allow-Origin "https://example.com"
```

### 認証情報付きリクエストがブロックされる場合

**問題**: クッキーや認証ヘッダーが送信されない

**原因**: `credentials: true` が設定されていない、または `Origin: *` が使用されている

**解決方法**:

```ruby
# Railsの場合
config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'example.com'  # * ではなく具体的なオリジン
    resource '*',
      credentials: true,
      headers: :any
  end
end
```

```apache
# Apacheの場合
Header always set Access-Control-Allow-Credentials "true"
```

## ベストプラクティス

### セキュリティ上の推奨事項

1. **ワイルドカード(*) の使用を避ける**:
   ```
   # ❌ 避けるべき
   Access-Control-Allow-Origin: *
   
   # ✅ 推奨
   Access-Control-Allow-Origin: https://trusted-domain.com
   ```

2. **HTTPSを使用する**:
   ```
   # ❌ 避けるべき
   Access-Control-Allow-Origin: http://example.com
   
   # ✅ 推奨
   Access-Control-Allow-Origin: https://example.com
   ```

3. **必要最小限のメソッドを許可**:
   ```
   # ❌ 避けるべき
   Access-Control-Allow-Methods: *
   
   # ✅ 推奨
   Access-Control-Allow-Methods: GET, POST, OPTIONS
   ```

4. **キャッシュ時間を適切に設定**:
   ```
   # 本番環境
   Access-Control-Max-Age: 86400  # 24時間
   
   # 開発環境
   Access-Control-Max-Age: 600    # 10分
   ```

### 環境ごとの設定分け

```ruby
# config/environments/development.rb
config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'localhost:3000', 'localhost:3001'
    resource '*', headers: :any, methods: :any
  end
end

# config/environments/production.rb
config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'example.com', 'www.example.com'
    resource '*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete],
      credentials: true
  end
end
```

## Apache設定集

### default-ssl.conf（標準設定）

```apache
<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem

    # CORSヘッダーの追加
    <IfModule mod_headers.c>
        Header always set Access-Control-Allow-Origin "https://www.pagespeedmonitor.jp"
        Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header always set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header always set Access-Control-Allow-Credentials "true"
    </IfModule>

    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Railsアプリケーションへのプロキシ設定
    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    # Preflightリクエストを処理
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### default-ssl.conf（localhost開発環境）

```apache
<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem

    # CORSヘッダーの追加（開発環境用：localhost:3000のみ許可）
    <IfModule mod_headers.c>
        Header always set Access-Control-Allow-Origin "http://localhost:3000"
        Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header always set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header always set Access-Control-Allow-Credentials "true"
    </IfModule>

    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Railsアプリケーションへのプロキシ設定
    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    # Preflightリクエストを処理
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### default-ssl.conf（CORS無効）

```apache
<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem
    
    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Railsアプリケーションへのプロキシ設定
    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    # Preflightリクエストを処理
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### default-ssl.conf（ワイルドカード許可）

```apache
<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem

    # CORSヘッダーの追加（注意：セキュリティ上は推奨されません）
    <IfModule mod_headers.c>
        Header always set Access-Control-Allow-Origin "*"
        Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header always set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header always set Access-Control-Allow-Credentials "true"
    </IfModule>

    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Railsアプリケーションへのプロキシ設定
    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    # Preflightリクエストを処理
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### rails_app.conf（HTTP→HTTPS統合設定）

```apache
<VirtualHost *:80>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem

    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    <IfModule mod_headers.c>
        Header set Access-Control-Allow-Origin "https://www.pagespeedmonitor.jp"
        Header set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header set Access-Control-Allow-Credentials "true"
    </IfModule>

    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### rails_app.conf（localhost開発環境）

```apache
<VirtualHost *:80>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem

    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    <IfModule mod_headers.c>
        Header set Access-Control-Allow-Origin "http://localhost:3000"
        Header set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header set Access-Control-Allow-Credentials "true"
    </IfModule>

    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### rails_app.conf（CORS無効）

```apache
<VirtualHost *:80>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem

    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### pagespeedmonitor.conf（統合設定ファイル）

```apache
<VirtualHost *:80>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    # HTTPをHTTPSにリダイレクト
    RewriteEngine On
    RewriteCond %{HTTPS} off
    RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName www.pagespeedmonitor.jp
    DocumentRoot /home/ubuntu/UI_pagespeedinsights/build

    # SSL設定
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/www.pagespeedmonitor.jp/chain.pem

    # CORSヘッダーの追加
    <IfModule mod_headers.c>
        Header always set Access-Control-Allow-Origin "*"
        Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header always set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header always set Access-Control-Allow-Credentials "true"
    </IfModule>

    <Directory /home/ubuntu/UI_pagespeedinsights/build>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Railsアプリケーションへのプロキシ設定
    ProxyPass /railsapp http://localhost:3001/
    ProxyPassReverse /railsapp http://localhost:3001/

    # Preflightリクエストを処理
    <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_METHOD} OPTIONS
        RewriteRule ^(.*)$ $1 [R=200,L]
    </IfModule>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

## 実装例

### 例1: localhost:3000 からのアクセスを許可

```apache
<VirtualHost *:443>
    ServerName www.example.com
    
    <IfModule mod_headers.c>
        Header always set Access-Control-Allow-Origin "http://localhost:3000"
        Header always set Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE, PATCH"
        Header always set Access-Control-Allow-Headers "Authorization, Content-Type"
        Header always set Access-Control-Allow-Credentials "true"
    </IfModule>
    
    ProxyPass /api http://localhost:3001/
    ProxyPassReverse /api http://localhost:3001/
</VirtualHost>
```

### 例2: 複数のオリジンを許可

```ruby
config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'example.com', 'www.example.com', 'app.example.com'
    resource '*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head]
  end
end
```

### 例3: 特定のパスのみCORSを有効化

```ruby
config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'example.com'
    resource '/api/*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete]
  end
end
```

## まとめ

CORSはモダンなウェブアプリケーション開発に不可欠な仕組みです。以下のポイントを押さえることが重要です：

- **セキュリティ**: 具体的なオリジンを指定し、`*` の使用を避ける
- **環境分け**: 開発環境と本番環境で異なる設定を使用
- **検証**: 実装後に curlやブラウザの開発者ツールで確認
- **ログ確認**: 問題が発生した場合はApacheやRailsのログを確認
- **キャッシュ**: プリフライトリクエストのキャッシュを適切に設定

これらを理解し実装することで、セキュアで効率的なクロスオリジン通信が実現できます。
