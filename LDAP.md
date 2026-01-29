# LDAP: ディレクトリサービスプロトコル完全ガイド

## 概要

LDAP（Lightweight Directory Access Protocol）は、ディレクトリサービスへのアクセスを提供するプロトコルです。ディレクトリサービスは、ユーザー、グループ、デバイス、その他のリソースに関する情報を一元管理するためのシステムで、ネットワーク内のリソース管理を効率化します。

### LDAPの特徴

- **軽量プロトコル**: X.500より簡潔で実装しやすい
- **階層構造**: ディレクトリ情報ツリー（DIT）による柔軟なデータ管理
- **統一認証**: 組織内のユーザー認証を一元管理
- **スケーラビリティ**: 大規模なディレクトリも効率的に管理
- **標準化**: RFC 4510シリーズで標準化

## LDAPの歴史と発展

LDAPは、1980年代後半から1990年代初頭にかけて開発されたX.500プロトコルに基づいていますが、より軽量で扱いやすいプロトコルとして設計されました。

**主な推移**:
- **1993年**: LDAP仕様がRFC 1487として最初に登場
- **1997年**: LDAP v3（RFC 2251）として標準化
- **2006年**: RFC 4510シリーズとして現在の主要標準が整備

## LDAPの基本構造

### ディレクトリ情報ツリー（DIT: Directory Information Tree）

LDAPは階層構造のディレクトリデータベースを利用します。

```
dc=example,dc=com （ルート）
├── ou=users
│   ├── uid=jdoe
│   └── uid=asmith
├── ou=groups
│   ├── cn=admins
│   └── cn=users
└── ou=services
    └── cn=mail
```

### 主要な概念

#### エントリ（Entry）

ディレクトリ内の各ノード。ユーザー、グループ、デバイスなどの情報を保持します。

```ldif
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
uid: jdoe
cn: John Doe
sn: Doe
givenName: John
mail: jdoe@example.com
```

#### 属性（Attribute）

エントリに含まれる個々のデータフィールド。

| 属性 | 説明 | 例 |
|------|------|-----|
| `uid` | ユーザーID | `jdoe` |
| `cn` | 共通名 | `John Doe` |
| `mail` | メールアドレス | `jdoe@example.com` |
| `sn` | 姓 | `Doe` |
| `givenName` | 名 | `John` |
| `objectClass` | エントリの型 | `inetOrgPerson` |

#### DN（Distinguished Name）

エントリを一意に識別するための名前。エントリのパスに相当します。

```
uid=jdoe,ou=users,dc=example,dc=com
│        │         │    └─ コンポーネント3: dc=com
│        │         └─ コンポーネント2: dc=example
│        └─ コンポーネント1: ou=users
└─ コンポーネント0: uid=jdoe
```

#### RDN（Relative Distinguished Name）

DNの一部で、親エントリ内で相対的に一意な名前。

```
uid=jdoe,ou=users,dc=example,dc=com
 ^^^^^^
 RDN
```

### オブジェクトクラス

エントリの型を定義し、そのエントリが持つべき属性を決定します。

| オブジェクトクラス | 説明 |
|------------------|------|
| `inetOrgPerson` | インターネット組織のユーザー |
| `organizationalUnit` | 組織単位（部門など） |
| `groupOfNames` | グループ |
| `device` | ネットワークデバイス |
| `organizationalRole` | 組織の役割 |

## LDAPの利用シーン

### 認証

ユーザーのログイン認証を一元管理

```
アプリケーション → LDAP → ユーザー認証
```

### 連絡先管理

組織内の連絡先情報を一元管理し、メールクライアントやカスタムアプリケーションから利用

### ネットワークリソース管理

プリンタやファイルサーバーなどのネットワークリソースのアクセス制御

### シングルサインオン（SSO）

複数のアプリケーションに対して、一度のログインで認証を実現

## OpenLDAPのセットアップ

### ステップ1: インストール

Ubuntu/Debianの場合：

```bash
sudo apt update
sudo apt install slapd ldap-utils
```

**出力例:**
```
slapd が既に最新版です。
ldap-utils が既に最新版です。
```

初期設定では対話的なセットアップが行われます。

### ステップ2: slapdの基本設定

設定ファイルディレクトリ：

```bash
ls -la /etc/ldap/slapd.d/
```

### ステップ3: ディレクトリツリーの初期化

LDIFファイル（LDAP Data Interchange Format）を作成：

```bash
cat > init.ldif << 'EOF'
dn: dc=example,dc=com
objectClass: top
objectClass: dcObject
objectClass: organization
o: Example Organization
dc: example

dn: cn=admin,dc=example,dc=com
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: Directory Manager
userPassword: {CRYPT}x

dn: ou=users,dc=example,dc=com
objectClass: organizationalUnit
ou: users

dn: ou=groups,dc=example,dc=com
objectClass: organizationalUnit
ou: groups
EOF
```

LDIFファイルを適用：

```bash
sudo ldapadd -x -D cn=admin,dc=example,dc=com -W -f init.ldif
```

## LDAP操作コマンド集

### ユーザーの追加

```ldif
dn: uid=jdoe,ou=users,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: jdoe
cn: John Doe
sn: Doe
givenName: John
displayName: John Doe
mail: jdoe@example.com
userPassword: password123
uidNumber: 1001
gidNumber: 1001
homeDirectory: /home/jdoe
loginShell: /bin/bash
```

ユーザー追加コマンド：

```bash
ldapadd -x -D cn=admin,dc=example,dc=com -W -f user.ldif
```

**説明**:
- `-x`: シンプルバインド（パスワード認証）
- `-D`: バインドDN（管理者DN）
- `-W`: パスワードプロンプト表示
- `-f`: 入力ファイル

### ユーザーの検索

基本的な検索：

```bash
ldapsearch -x -LLL -b "dc=example,dc=com" "uid=jdoe"
```

**出力例:**
```
dn: uid=jdoe,ou=users,dc=example,dc=com
uid: jdoe
cn: John Doe
sn: Doe
givenName: John
mail: jdoe@example.com
objectClass: inetOrgPerson
```

**オプション説明**:
- `-x`: シンプルバインド
- `-LLL`: LDIF形式で出力（コメント除外）
- `-b`: 検索ベースDN
- `-h`: LDAPサーバーホスト
- `-p`: ポート番号

### 複数条件での検索

```bash
# メールアドレスで検索
ldapsearch -x -LLL -b "dc=example,dc=com" "mail=jdoe@example.com"

# 部門（ou）内のユーザー全員を検索
ldapsearch -x -LLL -b "ou=users,dc=example,dc=com" "objectClass=inetOrgPerson"
```

### ユーザー情報の修正

修正用LDIFファイルを作成：

```ldif
dn: uid=jdoe,ou=users,dc=example,dc=com
changetype: modify
replace: mail
mail: newemail@example.com
-
replace: displayName
displayName: John D. Doe
```

修正を適用：

```bash
ldapmodify -x -D cn=admin,dc=example,dc=com -W -f modify.ldif
```

### ユーザー情報の削除

```bash
ldapdelete -x -D cn=admin,dc=example,dc=com -W "uid=jdoe,ou=users,dc=example,dc=com"
```

### グループの作成と管理

グループ作成：

```ldif
dn: cn=developers,ou=groups,dc=example,dc=com
objectClass: groupOfNames
cn: developers
member: uid=jdoe,ou=users,dc=example,dc=com
member: uid=asmith,ou=users,dc=example,dc=com
```

## LDAPのセキュリティ

### アクセス制御リスト（ACL）

slapd.confでACLを設定：

```
access to dn.base="" by * read
access to dn.base="cn=Subschema" by * read
access to attrs=userPassword by self write by anonymous auth by * none
access to * by self write by users read by * none
```

### TLS/SSL通信

```bash
# TLSで接続
ldapsearch -x -LLL -b "dc=example,dc=com" -H ldaps://ldap.example.com:636
```

### パスワードハッシング

安全なパスワード保存方法：

```bash
# SHAハッシュ生成
slappasswd -h {SHA}

# SSHA（Salted SHA）ハッシュ生成
slappasswd -h {SSHA}
```

## LDAP連携の実例

### アプリケーションでのLDAP認証

```python
# Python例（ldap3ライブラリ使用）
from ldap3 import Server, Connection, ALL

server = Server('ldap.example.com', get_info=ALL)
conn = Connection(server, user='uid=jdoe,ou=users,dc=example,dc=com', password='password')

if conn.bind():
    print("認証成功")
else:
    print("認証失敗")
```

### Linuxシステムの統合

`/etc/ldap.conf`（または`/etc/nslcd.conf`）を設定：

```
base dc=example,dc=com
uri ldap://ldap.example.com:389
binddn cn=admin,dc=example,dc=com
bindpw password
```

### Sambaとの連携

LDAPバックエンド上でSamba（Windows互換ファイルサーバー）を構築

## トラブルシューティング

### 接続できない場合

```bash
# 接続テスト
ldapwhoami -x -h ldap.example.com -p 389

# 詳細ログ
ldapwhoami -x -h ldap.example.com -v
```

### 検索結果が返されない場合

1. **ベースDNを確認**:
```bash
ldapsearch -x -s base -b "" namingContexts
```

2. **スキーマを確認**:
```bash
ldapsearch -x -LLL -b "cn=Subschema" -s base objectClass
```

### パスワード認証に失敗する場合

1. **パスワード形式を確認**:
```bash
# 新しいハッシュを生成
slappasswd -h {SSHA}
```

2. **ACLを確認**:
```bash
slapcat | grep -A5 "userPassword"
```

## 主要なオプション一覧

| コマンド | 説明 | 使用例 |
|---------|------|--------|
| `ldapsearch` | LDAP検索 | `ldapsearch -x -b "dc=example,dc=com" "uid=jdoe"` |
| `ldapadd` | エントリ追加 | `ldapadd -x -D cn=admin,... -W -f file.ldif` |
| `ldapmodify` | エントリ修正 | `ldapmodify -x -D cn=admin,... -W -f modify.ldif` |
| `ldapdelete` | エントリ削除 | `ldapdelete -x -D cn=admin,... -W "dn=..."` |
| `ldapwhoami` | 認証確認 | `ldapwhoami -x -h ldap.example.com` |
| `slappasswd` | パスワード生成 | `slappasswd -h {SSHA}` |
| `slapcat` | ディレクトリダンプ | `slapcat -l backup.ldif` |

## ベストプラクティス

### セキュリティ

1. **TLS/SSLの使用**:
```bash
# LDAPS（ポート636）を使用
uri ldaps://ldap.example.com:636
```

2. **Strong Password Policy**:
```
ppolicy_default "cn=default,ou=policies,dc=example,dc=com"
```

3. **アクセス制限**:
```
# 認証ユーザーのみ読み取り可能
access to * by users read by * none
```

### 運用

1. **定期的なバックアップ**:
```bash
sudo slapcat -l backup-$(date +%Y%m%d).ldif
```

2. **ログの確認**:
```bash
sudo tail -f /var/log/syslog | grep slapd
```

3. **リプリケーション設定**:
災害対策として複数のLDAPサーバーを構成

## まとめ

LDAPは、ネットワーク内のリソース管理とユーザー認証を一元管理するための強力なプロトコルです。

重要なポイント：
- **階層構造**: DITにより柔軟なデータ管理が可能
- **標準化**: 多くのシステムで採用される標準プロトコル
- **セキュリティ**: TLS/SSLとACLにより安全な運用が実現
- **統一認証**: 複数のアプリケーションでSSO実現
- **スケーラビリティ**: 大規模な組織にも対応可能

適切に構成・管理することで、組織全体のITリソース管理を大幅に効率化できます。
