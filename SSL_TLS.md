# SSL/TLS: セキュアな通信プロトコルの完全ガイド

## 概要

SSL（Secure Sockets Layer）およびTLS（Transport Layer Security）は、インターネット上で安全にデータを送受信するためのプロトコルです。これらのプロトコルは、データの暗号化、認証、データの完全性を確保し、通信のプライバシーを保護します。TLSはSSLの後継バージョンであり、より強力なセキュリティ機能を提供します。

### 歴史と進化

- **SSL 1.0**: 初期版（リリースされず）
- **SSL 2.0**: 1995年（セキュリティ脆弱性がある）
- **SSL 3.0**: 1996年（改善されたバージョン）
- **TLS 1.0**: 1999年（SSL 3.0の改名・改良版）
- **TLS 1.1**: 2006年
- **TLS 1.2**: 2008年（現在の標準）
- **TLS 1.3**: 2018年（最新で最も安全）

### 推奨事項

- **使用すべき**: TLS 1.2以上
- **避けるべき**: SSL 2.0、SSL 3.0、TLS 1.0、TLS 1.1

## SSL/TLSの3つの主要機能

### 1. 暗号化（Encryption）

データを暗号化して、第三者による傍受を防ぎます。

```
平文データ → 暗号化 → 暗号文 → ネットワーク → 復号化 → 平文データ
```

**使用される暗号化方式**:
- **対称鍵暗号**: AES（Advanced Encryption Standard）
- **非対称鍵暗号**: RSA、ECDSA

### 2. 認証（Authentication）

サーバーおよびクライアントの身元を確認し、なりすましを防ぎます。

```
クライアント → サーバーの証明書受け取り → 証明書検証 → 身元確認
```

**検証項目**:
- ドメイン名
- 発行認証局（CA）
- 証明書有効期限
- 証明書署名

### 3. データの完全性（Integrity）

送受信されるデータが改ざんされていないことを保証します。

```
データ → ハッシュ値生成 → 送信 → ハッシュ値検証 → 改ざん検出
```

**使用されるハッシュ関数**:
- SHA-256（推奨）
- SHA-384
- SHA-512

## SSL/TLSハンドシェイクプロセス

SSL/TLSの通信が始まる前に、クライアントとサーバー間で「ハンドシェイク」と呼ばれる初期設定が行われます。

### ステップバイステップの流れ

```
クライアント                                    サーバー
   │                                             │
   ├─── 1. ClientHello ───────────────────────>│
   │     - TLSバージョン                        │
   │     - サポート暗号スイート               │
   │     - クライアントランダム                 │
   │                                             │
   │<─── 2. ServerHello ───────────────────────│
   │       - 選択されたTLSバージョン             │
   │       - 選択された暗号スイート             │
   │       - サーバーランダム                   │
   │                                             │
   │<─── 3. Certificate ──────────────────────│
   │       - サーバーX.509証明書                │
   │                                             │
   │<─── 4. ServerKeyExchange (オプション) ──│
   │       - DHパラメータ等                     │
   │                                             │
   │<─── 5. ServerHelloDone ──────────────────│
   │                                             │
   ├─── 6. ClientKeyExchange ─────────────────>│
   │       - プリマスターシークレット            │
   │                                             │
   ├─── 7. ChangeCipherSpec ──────────────────>│
   │       - 以降暗号化開始                     │
   │                                             │
   ├─── 8. Finished ──────────────────────────>│
   │       - ハンドシェイク完了メッセージ      │
   │                                             │
   │<─── 9. ChangeCipherSpec ──────────────────│
   │       - 以降暗号化開始                     │
   │                                             │
   │<─── 10. Finished ────────────────────────│
   │        - ハンドシェイク完了メッセージ      │
   │                                             │
   ├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─>│
   │     暗号化されたApplicationDataの送受信  │
   │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
   │                                             │
```

### 詳細な説明

#### 1-2. ハンドシェイク開始（ClientHello/ServerHello）

**ClientHello**:
```
- Protocol Version: TLS 1.2
- Supported Cipher Suites: [
    TLS_RSA_WITH_AES_128_CBC_SHA256,
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
    ...
  ]
- Client Random: 32-byte random value
```

**ServerHello**:
```
- Protocol Version: TLS 1.2
- Selected Cipher Suite: TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
- Server Random: 32-byte random value
```

#### 3. 証明書送信（Certificate）

サーバーがX.509形式の公開鍵証明書を送信

```
Certificate Chain:
  - Leaf Certificate (www.example.com)
  - Intermediate CA Certificate
  - Root CA Certificate
```

#### 4. 鍵交換（ClientKeyExchange）

クライアントが鍵交換用データを暗号化して送信

```
Pre-Master Secret
  ↓
Both Client and Server generate:
Master Secret = PRF(Pre-Master Secret, 
                    "master secret",
                    Client Random + Server Random)
  ↓
Session Keys (Encryption Key, MAC Key, IV)
```

#### 5. ハンドシェイク完了（Finished）

双方が検証メッセージを交換して、ハンドシェイク完了を確認

## SSL/TLSの暗号スイート

### 暗号スイートの構成

```
TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
│         │       │        │    │
│         │       │        │    └─ メッセージ認証コード（HMAC）
│         │       │        └────── 暗号化アルゴリズム
│         │       └───────────── 暗号化モード
│         └──────────────────── 公開鍵認証
└───────────────────────────── 鍵交換プロトコル
```

### 推奨される暗号スイート

```
TLS 1.3:
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_GCM_SHA256

TLS 1.2:
- TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
- TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
- TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
```

### 避けるべき暗号スイート

```
❌ DES
❌ MD5
❌ SHA-1（ハッシュとして）
❌ RC4
❌ 暗号スイートなし（NULL）
```

## SSL/TLSの使用例

### 1. HTTPS（ウェブブラウザ×ウェブサーバー）

最も一般的なSSL/TLSの使用例

```
ユーザー → ブラウザ → HTTPS → ウェブサーバー
                   ↓
            TLS 1.2/1.3で暗号化
```

**プロトコル**: `https://`（デフォルトポート: 443）

### 2. メール通信

```
SMTPS（Simple Mail Transfer Protocol Secure）
  - ポート: 465 または 587
  
IMAPS（Internet Message Access Protocol Secure）
  - ポート: 993
  
POP3S（POP3 Secure）
  - ポート: 995
```

### 3. VPN（Virtual Private Network）

```
ローカルネットワーク → VPN Client → TLS/SSL → VPN Server → 本社ネットワーク
```

### 4. API通信

```
クライアント → HTTPS → API Server
              (JSON/XML)
```

### 5. データベース接続

```
アプリケーション → SSL/TLS → データベースサーバー
（MySQL, PostgreSQL等）
```

## Apacheでのセットアップ

### ステップ1: SSLモジュルの有効化

```bash
sudo a2enmod ssl
sudo systemctl restart apache2
```

### ステップ2: 証明書ファイルの配置

```bash
sudo cp yourdomain.crt /etc/ssl/certs/
sudo cp yourdomain.key /etc/ssl/private/
sudo chmod 600 /etc/ssl/private/yourdomain.key
```

### ステップ3: VirtualHost設定

`/etc/apache2/sites-available/ssl.conf`:

```apache
<VirtualHost *:443>
    ServerAdmin webmaster@yourdomain.com
    ServerName yourdomain.com
    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/yourdomain.crt
    SSLCertificateKeyFile /etc/ssl/private/yourdomain.key
    SSLCertificateChainFile /etc/ssl/certs/chain.crt

    # TLS設定
    SSLProtocol -all +TLSv1.2 +TLSv1.3
    SSLCipherSuite HIGH:!aNULL:!MD5:!3DES

    # セッション設定
    SSLSessionCacheTimeout 300

    # セキュリティヘッダー
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### ステップ4: Apache再起動

```bash
sudo apachectl configtest
sudo systemctl reload apache2
```

## SSL/TLSの検証

### OpenSSLコマンド

**サーバーの証明書情報を取得**:

```bash
openssl s_client -connect www.example.com:443
```

**出力例**:
```
subject=CN = www.example.com
issuer=C = US, O = Let's Encrypt, CN = R3
Not Before: Jun 12 10:00:00 2024 GMT
Not After : Sep 10 10:00:00 2024 GMT
```

**証明書ファイルを確認**:

```bash
openssl x509 -in /path/to/cert.pem -noout -text
```

**証明書の有効期限を確認**:

```bash
openssl x509 -noout -dates -in /path/to/cert.pem
```

### ブラウザでの確認

1. アドレスバーの鍵マークをクリック
2. 証明書情報を確認
3. 発行認証局、有効期限を確認

## セキュリティベストプラクティス

### 1. TLSバージョンの指定

```apache
# TLS 1.2 以上のみ
SSLProtocol -all +TLSv1.2 +TLSv1.3
```

### 2. 強力な暗号スイートの選択

```apache
SSLCipherSuite 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384'
```

### 3. HSTS（HTTP Strict Transport Security）

```apache
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
```

### 4. 完全前方秘匿性（Perfect Forward Secrecy）

```apache
# 鍵交換に楕円曲線ディフィ・ヘルマン鍵交換を優先
SSLHonorCipherOrder on
SSLCipherSuite "EECDH+ECDSA+AES128:RSA+AES128:EECDH+aRSA+AES128:RSA+aRSA+AES128"
```

### 5. セッション設定

```apache
SSLSessionCache shmcb:/var/cache/apache2/ssl_scache(512000)
SSLSessionCacheTimeout 300
SSLSessionTickets off
```

### 6. X-Frame-Options

```apache
Header always set X-Frame-Options "SAMEORIGIN"
```

## トラブルシューティング

### 証明書の有効期限切れ

```bash
# 有効期限確認
openssl x509 -noout -dates -in /path/to/cert.pem

# 結果例:
# notBefore=Jun 12 10:00:00 2024 GMT
# notAfter=Sep 10 10:00:00 2024 GMT
```

**対処方法**: 新しい証明書を取得し、設定ファイルを更新

### 証明書が信頼されていない

```bash
# 中間証明書チェーンを確認
openssl s_client -connect www.example.com:443 -showcerts
```

**対処方法**: チェーン証明書をSSLCertificateChainFileで指定

### 暗号スイートエラー

```bash
# サポートされている暗号スイートを確認
openssl ciphers -v 'HIGH:!aNULL:!MD5'
```

## SSL/TLSの監視

### 証明書有効期限の監視

```bash
#!/bin/bash
CERT_FILE="/path/to/cert.pem"
EXPIRY_DATE=$(openssl x509 -noout -dates -in $CERT_FILE | grep notAfter | cut -d= -f2)
echo "証明書有効期限: $EXPIRY_DATE"
```

### TLSハンドシェイク時間の計測

```bash
curl -w "TLS Handshake: %{time_appconnect}s\n" https://www.example.com
```

## まとめ

SSL/TLSは、インターネット上で安全にデータを送受信するための重要なプロトコルです。

重要なポイント：
- **暗号化**: データのプライバシーを保護
- **認証**: サーバーとクライアントの身元確認
- **完全性**: データの改ざん検出

推奨事項：
- **TLS 1.2以上を使用**
- **強力な暗号スイートを選択**
- **定期的に証明書を更新**
- **セキュリティヘッダーを設定**
- **ハンドシェイク時間を監視**

適切に設定・管理することで、信頼性の高いセキュアな通信環境を構築できます。
