# FIDO2 認証 - パスキーとセキュアなユーザー認証

FIDO2（WebAuthn）を使用したパスワードレス認証の実装ガイド

## FIDO 認証とは

FIDO認証（Fast Identity Online）は、インターネット上でのセキュアなユーザー認証を提供するための技術標準です。パスワードだけに依存する従来の認証方法とは異なり、FIDO認証はより安全で使いやすい代替手段を提供します。

### FIDO 認証の背景

インターネットのセキュリティは常に進化していますが、パスワード依存の認証システムは依然として多くの脆弱性を抱えています。

**パスワード認証の問題点：**

```
✗ パスワード盗難のリスク
  └─ フィッシング、データ流出に脆弱

✗ ユーザビリティの低下
  └─ 複雑な要件、頻繁な変更が必要

✗ 管理の負担
  └─ ユーザーが複数のパスワードを管理

✗ リセット業務
  └─ パスワード忘却対応のコスト増加
```

FIDOアライアンスは、これらの問題を解決するために、2013年に設立されました。同アライアンスは、Google、Microsoft、Yubicoなどのテクノロジー企業が参加しており、より安全で使いやすい認証方法の開発を推進しています。

### FIDO 認証の仕組み

FIDO認証は二つの主要な技術仕様、すなわちUAF（Universal Authentication Framework）とU2F（Universal 2nd Factor）に基づいています。これらの仕様は、生体認証（指紋や顔認識など）、物理的なセキュリティデバイス（USBトークンやNFCデバイスなど）、またはPINを用いてユーザーの身元を確認します。

**FIDO認証の基本フロー：**

```
登録フェーズ：
  1. ユーザーがデバイスで生体認証/PIN入力
  2. デバイスが秘密鍵と公開鍵を生成
  3. 公開鍵をサーバーに送信・登録
  4. 秘密鍵はデバイスに保存（外部に出ない）

認証フェーズ：
  1. ユーザーが生体認証/PIN入力
  2. デバイスがチャレンジに秘密鍵で署名
  3. 署名をサーバーに送信
  4. サーバーが公開鍵で署名を検証
  5. 認証成功/失敗を判定
```

### UAF プロトコル

UAFはユーザーがデバイスに初めてログインする際に、生体認証やPINなどの手段で登録を行います。登録時には、公開鍵が生成され、対応する秘密鍵がユーザーのデバイスに保存されます。認証時にはユーザーが登録した手段を使用してデバイスが秘密鍵にアクセスし、サーバーに対して署名された認証応答を提供します。

### U2F プロトコル

U2Fは、既存のパスワードベースのログインに追加のセキュリティ層を提供します。ユーザーはログイン時にパスワードと共に、U2Fデバイス（例えばUSBセキュリティキー）を使用して認証を行います。このデバイスはサーバーによって提示されたチャレンジに対して、デバイス内の秘密鍵を使用して応答を署名します。

### FIDO 認証の利点

#### 1. セキュリティの向上

秘密鍵はユーザーのデバイス内にのみ存在し、サーバー側には公開鍵のみが保存されるため、外部からの攻撃リスクが軽減されます。

```
攻撃シナリオの比較：

パスワード認証：
├─ サーバーのハッシュ化されたパスワードが盗まれる
└─ ブルートフォース攻撃のリスク

FIDO2認証：
├─ 秘密鍵はデバイス内にのみ存在
├─ サーバーには公開鍵のみ（再生成困難）
└─ フィッシング攻撃に強い（署名検証で防止）
```

#### 2. 使いやすさ

生体認証や物理的なセキュリティデバイスを利用することで、パスワードを覚える必要がなくなり、ログインプロセスが簡素化されます。

```
ユーザー体験の改善：

従来のパスワード認証：
├─ パスワード入力
├─ 多要素認証（SMSなど）待機
└─ 時間：30秒～1分

FIDO2認証：
├─ 指紋認証/顔認識
└─ 時間：3～5秒
```

#### 3. プライバシー保護

FIDO認証はユーザーの個人情報をデバイス外に送信することなく、ローカルで認証処理を完了するため、プライバシーが保護されます。

## FIDO2 と WebAuthn

FIDO2は最新の FIDO 標準であり、**WebAuthn**（Web Authentication API）として W3C により標準化されています。

### 対応ブラウザと環境

```
デスクトップブラウザ：
├─ Chrome 67+
├─ Firefox 60+
├─ Safari 13+
└─ Edge 18+

モバイルブラウザ：
├─ Chrome for Android 87+
├─ Safari on iOS 14+
└─ Firefox Android 87+

サポート環境：
├─ Windows Hello
├─ Touch ID/Face ID（Apple）
├─ 指紋スキャナー（Android）
├─ セキュリティキー（YubiKey など）
└─ スマートフォン（ローミング認証）
```

### WebAuthn 仕様書

- [Web Authentication: An API for accessing Public Key Credentials - Level 2](https://www.w3.org/TR/webauthn/)
- [Google Codelabs - WebAuthn 入門](https://developers.google.com/codelabs/webauthn-reauth?hl=ja)

## WebAuthn 実装ガイド

### フロントエンド実装（JavaScript/Vue.js）

#### HTML ストラクチャ

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="Content-Security-Policy" content="default-src * data: gap: 'unsafe-eval' 'unsafe-inline'">
  <meta name="viewport" content="user-scalable=no, initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width">
  
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  
  <title>FIDO2 Demo Server</title>
  
  <script src="js/methods_utils.js"></script>
  <script src="js/vue_utils.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>
  <script src="https://unpkg.com/vue"></script>
</head>
<body>
    <div id="top" class="container">
        <h1>FIDO2 Demo Server</h1>
        
        <!-- メッセージ表示エリア -->
        <div class="alert alert-info" role="alert">{{message}}</div>
        
        <!-- ユーザー名入力フォーム -->
        <div class="form-inline">
            <label>username</label> 
            <input type="text" class="form-control" v-model="username">
        </div>
        
        <!-- 登録開始ボタン -->
        <button class="btn btn-default" v-on:click="start_register()">登録開始</button>
        
        <!-- 認証情報表示エリア -->
        <div v-if="attestation != null">
            <label>rp.name</label> {{attestation.rp.name}}<br>
            <label>user.displayName</label> {{attestation.user.displayName}}<br>
            <label>user.id</label> {{attestation_encode.user.id}}<br>
            <label>challenge</label> {{attestation_encode.challenge}}<br>
            <button class="btn btn-default" v-on:click="do_register()">登録実行</button>
        </div>
        
        <!-- 登録完了後の表示エリア -->
        <div v-if="registered">
            <label>credId</label> {{register_credId}}<br>
            <label>counter</label> {{register_counter}}<br>
        </div>
        
        <!-- ログイン開始ボタン -->
        <button class="btn btn-default" v-on:click="start_login()">ログイン開始</button>
        
        <!-- ログイン情報表示エリア -->
        <div v-if="assertion != null">
            <div v-for="(cred, index) of assertion_encode.allowCredentials">
                <label>cred.id[{{index}}]</label> {{cred.id}}<br>
            </div>
            <label>challenge</label> {{assertion_encode.challenge}}<br>
            <button class="btn btn-default" v-on:click="do_login()">ログイン実行</button>
        </div>
        
        <!-- ログイン完了後の表示エリア -->
        <div v-if="logined">
            <label>credId</label> {{login_credId}}<br>
            <label>counter</label> {{login_counter}}<br>
        </div>
        
        <!-- プログレスバー モーダル -->
        <div class="modal fade" id="progress">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">{{progress_title}}</h4>
                    </div>
                    <div class="modal-body">
                        <center><progress max="100" /></center>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="dist/js/base64url-arraybuffer.js"></script>
    <script src="js/start.js"></script>
</body>
</html>
```

#### Vue.js ロジック（start.js）

```javascript
'use strict';

const base_url = "https://your-fido-server.com"; // サーバーURL

var vue_options = {
    el: "#top",
    data: {
        progress_title: '',
        message: "",
        username: 'test',
        attestation: null,
        attestation_encode: {
            user: {}
        },
        register_credId: null,
        register_counter: -1,
        registered: false,
        assertion: null,
        assertion_encode: {
            allowCredentials: []
        },
        login_credId: null,
        login_counter: -1,
        logined: false
    },
    methods: {
        // 登録開始：サーバーから認証オプションを取得
        start_register: function() {
            this.registered = false;
            var param = {
                username: this.username,
                userVerification: true
            };
            this.progress_open();
            do_post(base_url + '/attestation/options', param)
            .then(json => {
                this.progress_close();
                if (json.status != 'ok') {
                    alert(json.message);
                    return;
                }

                // Base64URLエンコードされた値を保存
                this.attestation_encode.challenge = json.challenge;
                this.attestation_encode.user.id = json.user.id;

                // バッファに変換
                json.challenge = base64url.decode(json.challenge);
                json.user.id = base64url.decode(json.user.id);

                this.attestation = json;
                this.message = '登録の準備ができました。';
            })
            .catch(error => {
                this.progress_close();
                alert(error);
            });
        },

        // 登録実行：デバイスで認証器を作成
        do_register: function() {
            return navigator.credentials.create({ 
                publicKey: this.attestation 
            })
            .then(response => {
                var result = publicKeyCredentialToJSON(response);
                this.progress_open();
                return do_post(base_url + '/attestation/result', result)
            })
            .then((response) => {
                this.progress_close();
                if (response.status !== 'ok') {
                    alert(response.message);
                    return;
                }

                this.register_credId = response.credId;
                this.register_counter = response.counter;
                this.registered = true;
                this.message = '登録が完了しました。';
            })
            .catch(error => {
                this.progress_close();
                alert(error);
            });
        },

        // ログイン開始：サーバーからアサーションオプションを取得
        start_login: function() {
            this.logined = false;
            var param = {
                username: this.username,
            };

            this.progress_open();
            do_post(base_url + '/assertion/options', param)
            .then(json => {
                this.progress_close();
                if (json.status != 'ok') {
                    alert(json.message);
                    return;
                }

                this.assertion_encode.challenge = json.challenge;
                json.challenge = base64url.decode(json.challenge);

                // allowCredentials をデコード
                for (var i = 0; i < json.allowCredentials.length; i++) {
                    this.assertion_encode.allowCredentials[i] = { 
                        id: json.allowCredentials[i].id 
                    };
                    json.allowCredentials[i].id = base64url.decode(
                        json.allowCredentials[i].id
                    );
                }

                this.assertion = json;
                this.message = 'ログインの準備ができました。';
            })
            .catch(error => {
                this.progress_close();
                alert(error);
            });
        },

        // ログイン実行：デバイスで認証
        do_login: function() {
            return navigator.credentials.get({ 
                publicKey: this.assertion 
            })
            .then(response => {
                var result = publicKeyCredentialToJSON(response);
                this.progress_open();
                return do_post(base_url + '/assertion/result', result)
            })
            .then((response) => {
                this.progress_close();
                if (response.status !== 'ok')
                    throw new Error(response.message);

                this.login_credId = response.credId;
                this.login_counter = response.counter;
                this.logined = true;
                this.message = 'ログインが成功しました。';
            })
            .catch(error => {
                this.progress_close();
                alert(error);
            });
        },

        // プログレスバーを表示
        progress_open: function() {
            this.progress_title = '処理中...';
            $('#progress').modal('show');
        },

        // プログレスバーを非表示
        progress_close: function() {
            $('#progress').modal('hide');
        }
    },
    mounted: function() {
        console.log('Vue mounted');
    }
};

var vue = new Vue(vue_options);

// POSTリクエストを送信
function do_post(url, body) {
    const headers = new Headers({ 
        "Content-Type": "application/json" 
    });
    
    return fetch(url, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(body),
        headers: headers
    })
    .then((response) => {
        if (!response.ok)
            throw 'HTTP error';
        return response.json();
    });
}

// PublicKeyCredential を JSON に変換
function publicKeyCredentialToJSON(pubKeyCred) {
    if (pubKeyCred instanceof Array) {
        let arr = [];
        for (let i of pubKeyCred)
            arr.push(publicKeyCredentialToJSON(i));
        return arr;
    }

    if (pubKeyCred instanceof ArrayBuffer) {
        return base64url.encode(pubKeyCred);
    }

    if (pubKeyCred instanceof Object) {
        let obj = {};
        for (let key in pubKeyCred) {
            obj[key] = publicKeyCredentialToJSON(pubKeyCred[key]);
        }
        return obj;
    }

    return pubKeyCred;
}
```

### サーバー側実装（Node.js）

#### パッケージのインストール

```bash
npm install fido2-lib base64url crypto express express-session
```

#### サーバーコード（index.js）

```javascript
'use strict';

const base64url = require('base64url');
const crypto = require('crypto');
const { Fido2Lib } = require("fido2-lib");

// FIDO2 設定
const FIDO_RP_NAME = "Sample FIDO Host";
const FIDO_ORIGIN = "https://your-domain.com";

// Fido2Lib インスタンス
var f2l = new Fido2Lib({
  rpName: FIDO_RP_NAME
});

// インメモリデータベース（実装時は実DB を使用）
let database = {};

// ===== 登録処理 =====

// 登録オプション生成
exports.attestation_options = async (req, res) => {
    let username = req.body.username;

    // 既存ユーザーをチェック
    if (database[username] && database[username].registered) {
        return res.json({
            'status': 'failed',
            'message': `Username ${username} already exists`
        });
    }

    // ユーザーIDを生成
    var id = randomBase64URLBuffer();

    // 登録オプションを生成
    var registrationOptions = await f2l.attestationOptions();
    registrationOptions.challenge = base64url.encode(registrationOptions.challenge);
    registrationOptions.user.id = id;
    registrationOptions.user.name = username;
    registrationOptions.user.displayName = username;

    // データベースにユーザーを登録
    database[username] = {
        'name': username,
        'registered': false,
        'id': id,
        'attestation': []
    };

    // セッションに保存
    req.session.challenge = registrationOptions.challenge;
    req.session.username = username;

    registrationOptions.status = 'ok';
    res.json(registrationOptions);
};

// 登録結果の検証
exports.attestation_result = async (req, res) => {
    var body = req.body;

    // 登録期待値
    var attestationExpectations = {
        challenge: req.session.challenge,
        origin: FIDO_ORIGIN,
        factor: "either"
    };

    // ID をバッファに変換
    body.rawId = new Uint8Array(base64url.toBuffer(body.id)).buffer;

    // 登録結果の検証
    var regResult = await f2l.attestationResult(body, attestationExpectations);

    // 認証情報を保存
    var credId = base64url.encode(regResult.authnrData.get('credId'));
    var counter = regResult.authnrData.get('counter');
    database[req.session.username].attestation.push({
        publickey: regResult.authnrData.get('credentialPublicKeyPem'),
        counter: counter,
        fmt: regResult.authnrData.get('fmt'),
        credId: credId
    });

    // 登録完了
    if (regResult.audit.complete) {
        database[req.session.username].registered = true;

        return res.json({
            'status': 'ok',
            credId: credId,
            counter: counter
        });
    } else {
        return res.json({
            'status': 'failed',
            'message': 'Signature verification failed!'
        });
    }
};

// ===== 認証処理 =====

// 認証オプション生成
exports.assertion_options = async (req, res) => {
    var body = req.body;
    let username = body.username;

    // ユーザーが存在するかチェック
    if (!database[username] || !database[username].registered) {
        return res.json({
            'status': 'failed',
            'message': `Username ${username} does not exist`
        });
    }

    // 認証オプションを生成
    var authnOptions = await f2l.assertionOptions();
    authnOptions.challenge = base64url.encode(authnOptions.challenge);

    // allowCredentials を設定
    let allowCredentials = [];
    for (let authr of database[username].attestation) {
        allowCredentials.push({
            type: 'public-key',
            id: authr.credId,
            transports: ['usb', 'nfc', 'ble', 'internal']
        });
    }
    authnOptions.allowCredentials = allowCredentials;

    // セッションに保存
    req.session.challenge = authnOptions.challenge;
    req.session.username = username;

    authnOptions.status = 'ok';
    res.json(authnOptions);
};

// 認証結果の検証
exports.assertion_result = async (req, res) => {
    var body = req.body;

    // 登録済み認証情報を検索
    var attestation = null;
    for (var i = 0; i < database[req.session.username].attestation.length; i++) {
        if (database[req.session.username].attestation[i].credId == body.id) {
            attestation = database[req.session.username].attestation[i];
            break;
        }
    }

    if (!attestation) {
        return res.json({
            'status': 'failed',
            'message': 'Credential not found'
        });
    }

    // 認証期待値
    var assertionExpectations = {
        challenge: req.session.challenge,
        origin: FIDO_ORIGIN,
        factor: "either",
        publicKey: attestation.publickey,
        prevCounter: attestation.counter,
        userHandle: null
    };

    // ID をバッファに変換
    body.rawId = new Uint8Array(base64url.toBuffer(body.id)).buffer;
    if (!body.response.userHandle)
        body.response.userHandle = undefined;

    // 認証結果の検証
    var authnResult = await f2l.assertionResult(body, assertionExpectations);

    if (authnResult.audit.complete) {
        attestation.counter = authnResult.authnrData.get('counter');

        return res.json({
            'status': 'ok',
            credId: body.id,
            counter: attestation.counter
        });
    } else {
        return res.json({
            'status': 'failed',
            'message': 'Signature verification failed!'
        });
    }
};

// ランダムな Base64URL バッファを生成
function randomBase64URLBuffer(len) {
    len = len || 32;
    let buff = crypto.randomBytes(len);
    return base64url(buff);
}
```

## フロント・サーバー処理の詳細フロー

### ユーザー登録の流れ

```
1. ユーザーが username を入力
   ↓
2. 「登録開始」ボタンをクリック
   ↓
3. start_register() メソッド実行
   ├─ サーバーの /attestation/options に POST
   └─ サーバーが登録オプション(challenge, user.id など)を返す
   ↓
4. 登録情報が画面に表示される
   ↓
5. 「登録実行」ボタンをクリック
   ↓
6. do_register() メソッド実行
   ├─ navigator.credentials.create() でデバイスに認証器作成を要求
   ├─ ユーザーが生体認証/PIN を実施
   ├─ デバイスが秘密鍵・公開鍵を生成
   └─ 公開鍵をサーバーに送信
   ↓
7. サーバーが /attestation/result で署名を検証
   ├─ 公開鍵をデータベースに保存
   └─ credId・counter を返す
   ↓
8. 登録完了メッセージを表示
```

### ユーザーログインの流れ

```
1. 「ログイン開始」ボタンをクリック
   ↓
2. start_login() メソッド実行
   ├─ サーバーの /assertion/options に POST
   └─ サーバーがアサーションオプション(challenge など)を返す
   ↓
3. ログイン情報が画面に表示される
   ↓
4. 「ログイン実行」ボタンをクリック
   ↓
5. do_login() メソッド実行
   ├─ navigator.credentials.get() でデバイスに認証を要求
   ├─ ユーザーが生体認証/PIN を実施
   ├─ デバイスが登録済み秘密鍵でチャレンジに署名
   └─ 署名をサーバーに送信
   ↓
6. サーバーが /assertion/result で署名を検証
   ├─ 登録済み公開鍵で署名を確認
   ├─ counter をチェック（リプレイ攻撃防止）
   └─ counter を更新
   ↓
7. ログイン成功メッセージを表示
```

## サーバー側の重要なコンセプト

### Challenge（チャレンジ）

チャレンジはサーバーが生成するランダムな値で、リプレイ攻撃を防ぐために必須です。

```
流れ：
1. サーバーが randomBytes でチャレンジを生成
2. Base64URL エンコードしてクライアントに送信
3. クライアントがチャレンジを受け取り、デバイスに送信
4. デバイスがチャレンジに秘密鍵で署名
5. サーバーが署名時のチャレンジと一致することを確認
```

### Counter（カウンター）

カウンターはデバイスが保持する署名回数で、リプレイ攻撃検出に使用します。

```
セキュリティ効果：

1. 認証時、デバイスから返される counter を取得
2. 前回の counter より増加しているか確認
3. 増加していない場合は攻撃の可能性 → 認証失敗
```

## ベストプラクティス

```
✅ 実装時の推奨

① Challenge の一意性
   └─ すべての認証リクエストで異なる値を生成

② Counter の検証
   └─ リプレイ攻撃を防止するため必須

③ Origin の確認
   └─ HTTPS による通信を必須に

④ 複数デバイス対応
   └─ 1ユーザーが複数の認証器を登録可能

⑤ ユーザーハンドル
   └─ 常駐認証器（パスキー）に対応

❌ 実装時の注意

① Challenge の使い捨て
   └─ 再利用によるセキュリティ低下

② Counter チェックの省略
   └─ リプレイ攻撃に対策不足

③ HTTP での通信
   └─ 中間者攻撃のリスク

④ エラーメッセージの過詳細
   └─ ユーザー列挙攻撃に利用される可能性
```

## トラブルシューティング

### 問題1：「NotSupportedError」

**原因：** ブラウザが WebAuthn に非対応

```javascript
// 対応確認
if (window.PublicKeyCredential === undefined ||
    navigator.credentials === undefined) {
  alert('WebAuthn is not supported');
  return;
}
```

### 問題2：「NotAllowedError」

**原因：** ユーザーが認証をキャンセル

```javascript
.catch(error => {
    if (error.name === 'NotAllowedError') {
        alert('ユーザーがキャンセルしました');
    } else {
        alert(error.message);
    }
});
```

### 問題3：「InvalidStateError」

**原因：** 同じ認証器で複数登録しようとした

```javascript
// 解決：ユーザーに別の認証器の使用を促す
// または、既存登録をスキップする選択肢を提供
```

### 問題4：「Timeout」

**原因：** ユーザーの操作が遅い、またはデバイスが反応しない

```javascript
// オプションでタイムアウト時間を指定
var authnOptions = await f2l.assertionOptions();
authnOptions.timeout = 60000; // 60秒
```

## 参考リソース

### 公式ドキュメント
- [W3C WebAuthn 仕様](https://www.w3.org/TR/webauthn/)
- [Google Developers - WebAuthn](https://developers.google.com/codelabs/webauthn-reauth?hl=ja)

### 実装例
- [WebAuthnを使ったFIDOサーバを立ててみた（Qiita）](https://qiita.com/poruruba/items/243d39c8b77b98a99bab)
- [Spring Security & LINE FIDO2 Server](https://zenn.dev/gebo/articles/spring-security-fido2-login-2)
- [PHP での FIDO2 実装](https://qiita.com/koujimatsuda11/items/47f00c9c4d6953377668)
- [Rails（Devise）+ パスキー実装](https://zenn.dev/takeyuwebinc/articles/ddae19db3aa9a6)

### 動画解説
- [#15【サクッと学べる支援士対策】FIDO認証](https://youtu.be/UvCazcKoOUU?si=QyrPGm4rMhsFVNYM)
- [【#38 ネスペ直前対策】FIDO](https://youtu.be/eBMPddnX170?si=L9gaxj2y0PJpURhK)
- [はじめての WebAuthn](https://youtu.be/yNuCWqATf7U?si=WG6dKFn2jp119dNy)

## 関連トピック

- [[Security]]：セキュリティ全般
- [[Authentication]]：認証方式
- [[WebAPI]]：Web API 仕様
- [[CloudSecurity]]：クラウドセキュリティ
