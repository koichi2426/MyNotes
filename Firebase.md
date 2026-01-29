# Firebase - Googleクラウドプラットフォーム

Googleが提供するモバイル・Web開発向けクラウドプラットフォーム

## 概要

Firebase は Google が提供するクラウドベースの開発プラットフォームで、バックエンドインフラストラクチャを管理することなく、高機能なアプリケーションを迅速に構築できます。

### Firebase の位置付け

```
従来：
フロントエンド開発 + バックエンド開発（インフラ管理含む）
                ↑ 複雑・コスト高

Firebase：
フロントエンド開発 + Firebase サービス組み合わせ
         ↑ シンプル・低コスト・スケーラブル
```

### 活用場面

```
✅ Firebase が活躍する場面
├─ スタートアップ（素早い開発）
├─ MVP 構築（最小限のコスト）
├─ リアルタイムアプリ（チャット、コラボツール）
├─ モバイルアプリ（iOS、Android）
├─ PWA（Progressive Web App）
└─ 小～中規模のバックエンド

⚠️ 注意が必要な場面
├─ 複雑なビジネスロジック（カスタム実装困難）
├─ 大規模データ処理（専用設計が必要）
├─ レガシーシステム連携（制限がある）
└─ コスト最適化が重要（スケール時は高コスト化）
```

## Firebase の主要機能

### 1. Firebase Authentication（認証）

**目的：** ユーザー認証を簡単に実装

#### サポートされる認証方式

```
① メール/パスワード認証
   ├─ 最もシンプル
   ├─ カスタムログイン画面が必要
   └─ リセット機能あり

② 電話番号認証
   ├─ SMS を使用
   ├─ グローバル対応
   └─ 2FA として利用可

③ OAuth プロバイダー
   ├─ Google
   ├─ Facebook
   ├─ GitHub
   ├─ Apple
   └─ ワンクリックログイン

④ カスタムトークン
   ├─ バックエンド で JWT 生成
   ├─ カスタム認証システム連携
   └─ エンタープライズ向け

⑤ 匿名認証
   ├─ ログイン不要
   ├─ アプリ試用に最適
   └─ 後から本登録に移行可
```

#### 認証フロー

```
ユーザー入力（メール/パスワード）
         ↓
Firebase Auth が検証
         ↓
成功 → ユーザーオブジェクト + ID Token 返却
         ↓
アプリに保存（自動的に LocalStorage に保存）
         ↓
Firestore へアクセス時に自動的に認証トークンを送信
```

#### セキュリティ機能

```
✅ Firebase Auth が提供
├─ パスワードは暗号化保存
├─ ジョブレート制限（ブルートフォース対策）
├─ デバイス確認（多要素認証）
├─ セッション管理
└─ リアルタイム監視（異常検出）
```

### 2. Cloud Firestore（NoSQL データベース）

**目的：** スケーラブルで リアルタイム同期のデータベース

#### 特徴

```
NoSQL データベース
├─ JSON ライクなドキュメント形式
├─ スキーマレス（柔軟）
└─ 階層構造（collections → documents → fields）

リアルタイム同期
├─ データ変更を自動的に全クライアントに通知
├─ Web Socket 使用
└─ オフライン対応あり

自動スケーリング
├─ サーバーレス
├─ 数十万のリクエスト/秒に対応
└─ 管理不要

セキュリティルール
├─ ドキュメントレベルの細かいアクセス制御
├─ ユーザー認証との統合
└─ リアルタイム検証
```

#### データ構造

```
Project
├─ Collection: users
│  ├─ Document: user123
│  │  ├─ name: "John Doe"
│  │  ├─ email: "john@example.com"
│  │  ├─ createdAt: 2026-01-29
│  │  └─ profile (subcollection)
│  │     └─ Document: settings
│  │        └─ theme: "dark"
│  │
│  └─ Document: user456
│     └─ ...
│
└─ Collection: posts
   ├─ Document: post001
   │  ├─ title: "Hello World"
   │  ├─ content: "..."
   │  ├─ authorId: "user123"
   │  └─ comments (subcollection)
   │     └─ ...
   │
   └─ Document: post002
      └─ ...
```

#### よく使う操作

```c
// Create（作成）
db.collection("users").add({
  name: "John",
  email: "john@example.com"
})

// Read（読み込み）
db.collection("users").doc("user123").get()

// Update（更新）
db.collection("users").doc("user123").update({
  name: "Jane"
})

// Delete（削除）
db.collection("users").doc("user123").delete()

// リアルタイムリッスン
db.collection("users").onSnapshot(snapshot => {
  snapshot.forEach(doc => {
    console.log(doc.data())
  })
})

// クエリ
db.collection("users")
  .where("age", ">", 18)
  .orderBy("createdAt")
  .limit(10)
  .get()
```

### 3. Firebase Realtime Database

**目的：** リアルタイム同期特化のデータベース

#### Firestore との比較

| 特性 | Firestore | Realtime DB |
|------|------|------|
| **データ形式** | ドキュメント（JSON） | JSON ツリー |
| **クエリ** | 強力（複雑な検索可） | 制限あり（基本的） |
| **スケーラビリティ** | 優れている | 中程度 |
| **リアルタイム性** | 高速 | 非常に高速 |
| **料金** | 読み取り/書き込み/削除 | ダウンロード GB 単位 |
| **推奨用途** | 一般的な用途 | リアルタイムゲーム、コラボ |

#### 選択基準

```
Firestore を選ぶべき場面：
├─ 複雑なクエリが必要
├─ ユーザー管理が複雑
├─ スケール予測が難しい
└─ 一般的な Web/モバイルアプリ

Realtime Database を選ぶべき場面：
├─ シンプルなリアルタイム同期
├─ ゲーム（位置情報、スコア更新）
├─ オンラインコラボツール
└─ チャットアプリ（シンプルな構造）
```

### 4. Firebase Hosting

**目的：** Web サイト・アプリの静的・動的ホスティング

#### 特徴

```
✅ メリット
├─ 自動 SSL 証明書（https）
├─ 高速 CDN（グローバル）
├─ カスタムドメイン対応
├─ リダイレクト・リライト機能
├─ デプロイは1コマンド
└─ 無料プラン あり

【セットアップ】
$ npm install -g firebase-tools
$ firebase init hosting
$ npm run build
$ firebase deploy --only hosting

【料金】
├─ 無料：5GB ストレージ、1GB 転送
├─ 従量課金：$0.15/GB 転送
└─ 小～中規模なら無料で十分
```

### 5. Cloud Functions（サーバーレス関数）

**目的：** バックエンドロジック を実装

#### 実装方式

```
Firestore トリガー
└─ ドキュメント作成・更新時に関数実行

HTTP トリガー
└─ API として関数を呼び出し

Firebase Auth トリガー
└─ ユーザー登録時などに関数実行

Pub/Sub トリガー
└─ メッセージキュー経由で非同期実行
```

#### 実装例

```javascript
// Firestore ドキュメント作成時
exports.onUserCreated = functions.firestore
  .document('users/{userId}')
  .onCreate(async (snap, context) => {
    const user = snap.data();
    // ウェルカムメール送信
    await sendWelcomeEmail(user.email);
  });

// HTTP エンドポイント
exports.api = functions.https.onRequest(async (req, res) => {
  if (req.method === 'POST') {
    const data = req.body;
    // 処理
    res.json({ success: true });
  }
});

// 定期実行（Pub/Sub）
exports.dailyReport = functions.pubsub
  .schedule('every day 09:00')
  .timeZone('Asia/Tokyo')
  .onRun(async (context) => {
    // 毎日9時にレポート生成
    await generateDailyReport();
  });
```

### 6. Firebase Storage（ファイルストレージ）

**目的：** ファイル（画像、動画）の保存

```javascript
// ファイルアップロード
const file = document.getElementById('fileInput').files[0];
const ref = firebase.storage().ref('images/' + file.name);
await ref.put(file);

// ファイルダウンロード URL 取得
const url = await ref.getDownloadURL();

// ファイル削除
await ref.delete();
```

### 7. Firebase Cloud Messaging（FCM）

**目的：** プッシュ通知を送信

```
対応プラットフォーム：
├─ Android
├─ iOS
└─ Web

実装の流れ：
1. サービスワーカー登録（Web）
2. トークン取得
3. トークンをサーバーに保存
4. サーバーから通知送信
```

## Firebase セットアップ

### ステップ1：Firebase プロジェクト作成

```
1. https://console.firebase.google.com/ にアクセス
2. 「プロジェクトを作成」をクリック
3. プロジェクト名を入力
4. Google Analytics（オプション）を有効化
5. 「プロジェクトを作成」をクリック
```

### ステップ2：アプリ登録

```
1. Firebase コンソール → プロジェクト設定
2. 「アプリを追加」をクリック
3. プラットフォーム選択（Web）
4. アプリニックネーム入力
5. Firebase SDK 設定コピー
```

### ステップ3：Web アプリへの導入

#### NPM でのインストール（推奨）

```bash
npm install firebase
```

#### 初期化コード

```javascript
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123def456"
};

// Firebase 初期化
const app = initializeApp(firebaseConfig);

// サービスの取得
export const auth = getAuth(app);
export const db = getFirestore(app);
```

#### HTML での CDN 導入（簡易）

```html
<!-- Firebase App -->
<script src="https://www.gstatic.com/firebasejs/10.0.0/firebase-app.js"></script>

<!-- Firebase Auth -->
<script src="https://www.gstatic.com/firebasejs/10.0.0/firebase-auth.js"></script>

<!-- Firebase Firestore -->
<script src="https://www.gstatic.com/firebasejs/10.0.0/firebase-firestore.js"></script>

<script>
const firebaseConfig = { /* ... */ };
firebase.initializeApp(firebaseConfig);
</script>
```

## React での実装

### Firebase Authentication（メール/パスワード）

#### 基本的な実装

```javascript
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "./firebase-config";

// ユーザー登録
export async function register(email, password) {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    return userCredential.user;
  } catch (error) {
    console.error("登録エラー:", error.message);
    throw error;
  }
}

// ユーザーログイン
export async function login(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return userCredential.user;
  } catch (error) {
    console.error("ログインエラー:", error.message);
    throw error;
  }
}

// ログアウト
export async function logout() {
  try {
    await auth.signOut();
  } catch (error) {
    console.error("ログアウトエラー:", error.message);
  }
}
```

#### React コンポーネント

```javascript
import { useState, useEffect } from 'react';
import { auth } from './firebase-config';
import { onAuthStateChanged } from 'firebase/auth';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // ユーザー認証状態の監視
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  if (loading) return <div>読み込み中...</div>;

  if (!user) {
    return <LoginComponent />;
  }

  return (
    <div>
      <h1>ようこそ {user.email}</h1>
      <LogoutButton />
    </div>
  );
}

export default App;
```

#### ログインフォーム

```javascript
import { useState } from 'react';
import { login } from './auth';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      // ログイン成功 → リダイレクト
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="メール"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="パスワード"
        required
      />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'ログイン中...' : 'ログイン'}
      </button>
    </form>
  );
}
```

### Firestore データベース操作

#### CRUD 操作

```javascript
import { 
  collection, 
  addDoc, 
  getDocs, 
  getDoc, 
  updateDoc, 
  deleteDoc, 
  doc, 
  query, 
  where,
  orderBy,
  limit 
} from "firebase/firestore";
import { db } from "./firebase-config";

// Create（作成）
export async function addPost(title, content) {
  try {
    const docRef = await addDoc(collection(db, "posts"), {
      title,
      content,
      createdAt: new Date(),
      authorId: auth.currentUser.uid
    });
    return docRef.id;
  } catch (error) {
    console.error("投稿エラー:", error);
    throw error;
  }
}

// Read（読み込み）- 全件取得
export async function getAllPosts() {
  try {
    const querySnapshot = await getDocs(collection(db, "posts"));
    const posts = [];
    querySnapshot.forEach((doc) => {
      posts.push({ id: doc.id, ...doc.data() });
    });
    return posts;
  } catch (error) {
    console.error("取得エラー:", error);
    throw error;
  }
}

// Read（読み込み）- 1件取得
export async function getPost(postId) {
  try {
    const docRef = doc(db, "posts", postId);
    const docSnap = await getDoc(docRef);
    if (docSnap.exists()) {
      return { id: docSnap.id, ...docSnap.data() };
    }
    return null;
  } catch (error) {
    console.error("取得エラー:", error);
    throw error;
  }
}

// Read（読み込み）- クエリ
export async function getPostsByAuthor(authorId) {
  try {
    const q = query(
      collection(db, "posts"),
      where("authorId", "==", authorId),
      orderBy("createdAt", "desc"),
      limit(10)
    );
    const querySnapshot = await getDocs(q);
    const posts = [];
    querySnapshot.forEach((doc) => {
      posts.push({ id: doc.id, ...doc.data() });
    });
    return posts;
  } catch (error) {
    console.error("クエリエラー:", error);
    throw error;
  }
}

// Update（更新）
export async function updatePost(postId, updates) {
  try {
    const docRef = doc(db, "posts", postId);
    await updateDoc(docRef, {
      ...updates,
      updatedAt: new Date()
    });
  } catch (error) {
    console.error("更新エラー:", error);
    throw error;
  }
}

// Delete（削除）
export async function deletePost(postId) {
  try {
    await deleteDoc(doc(db, "posts", postId));
  } catch (error) {
    console.error("削除エラー:", error);
    throw error;
  }
}
```

#### リアルタイムリッスン

```javascript
import { onSnapshot } from "firebase/firestore";

// リアルタイムで更新を受け取る
export function subscribeToPosts(callback) {
  const q = query(
    collection(db, "posts"),
    orderBy("createdAt", "desc")
  );
  
  const unsubscribe = onSnapshot(q, (querySnapshot) => {
    const posts = [];
    querySnapshot.forEach((doc) => {
      posts.push({ id: doc.id, ...doc.data() });
    });
    callback(posts);
  });

  return unsubscribe; // 購読解除用
}

// React コンポーネント で使用
function PostList() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const unsubscribe = subscribeToPosts(setPosts);
    return unsubscribe; // クリーンアップ
  }, []);

  return (
    <div>
      {posts.map(post => (
        <div key={post.id}>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
}
```

### Context API での 認証状態管理

```javascript
import { createContext, useContext, useState, useEffect } from 'react';
import { auth } from './firebase-config';
import { onAuthStateChanged } from 'firebase/auth';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const value = {
    user,
    loading,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

// 使用例
function ProtectedComponent() {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <div>ログインが必要です</div>;
  }

  return <div>ウェルカム {user.email}</div>;
}
```

## セキュリティ設定

### Firestore セキュリティルール

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // ユーザーは自分のドキュメントのみアクセス可
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }

    // 投稿：誰でも読む、認証済みユーザーなら書く
    match /posts/{postId} {
      allow read: if true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth.uid == resource.data.authorId;

      // コメントサブコレクション
      match /comments/{commentId} {
        allow read: if true;
        allow create: if request.auth != null;
        allow delete: if request.auth.uid == resource.data.userId;
      }
    }
  }
}
```

### Authentication セキュリティ設定

```
Firebase コンソール → Authentication → 設定

✅ 推奨設定：
├─ 複数アカウント禁止（同じメール）
├─ メール確認を必須化
├─ パスワード リセット確認を必須化
├─ 異常ログイン検出を有効化
└─ 2要素認証をサポート
```

## Firebase 料金体系

### 無料プラン

```
Authentication：
├─ 無制限ユーザー（認証）
└─ OAuth プロバイダー無制限

Firestore：
├─ 50,000 読み取り/日
├─ 20,000 書き込み/日
├─ 20,000 削除/日
├─ 1GB ストレージ
└─ 自動削除機能あり

Storage：
├─ 5GB ストレージ
└─ 1GB ダウンロード/日

Cloud Functions：
├─ 125,000 呼び出し/月
└─ 40,000 コンピュートセコンド/月

Hosting：
├─ 無制限 HTTPS
├─ 5GB ストレージ
└─ 1GB 転送
```

### 従量課金（有料）

```
Firestore：
├─ 読み取り：$0.06/100,000
├─ 書き込み：$0.18/100,000
├─ 削除：$0.02/100,000
└─ ストレージ：$0.18/GB

Storage：
├─ ストレージ：$0.025/GB
├─ ダウンロード：$0.12/GB
└─ アップロード：無料

Cloud Functions：
├─ 呼び出し：$0.40/100万
├─ GB・秒：$0.0025/GB・秒
└─ vCPU・秒：$0.01/vCPU・秒
```

## Firebase ベストプラクティス

### 1. セキュリティ

```
❌ してはいけないこと
├─ API キーをクライアント側で公開（やむを得ない）
├─ セキュリティルール設定なし
└─ 全員に読み書き権限

✅ すべきこと
├─ セキュリティルール厳格化
├─ 認証ユーザーのみアクセス許可
├─ ユーザー ID で所有権確認
└─ 定期的なセキュリティ監査
```

### 2. パフォーマンス

```
最適化ポイント：

① インデックス設定
   └─ よく検索するフィールドにインデックス

② ページング
   └─ limit() で大量データ取得回避

③ バッチ処理
   └─ writeBatch() で複数の書き込みを効率化

④ キャッシング
   └─ ローカル状態管理で不要なリクエスト削減

⑤ リアルタイムリッスン削減
   └─ 不要になった時点で購読解除
```

### 3. コスト最適化

```
コスト削減策：

① Firestore 選択基準
   └─ 本当に Firestore が必要か検討

② クエリ最適化
   └─ 不要なデータ取得しない

③ バッチ削除
   └─ 古いデータ自動削除

④ Cloud Functions の最適化
   └─ コールドスタート最小化

⑤ 従量課金の監視
   └─ 予算アラート設定
```

## トラブルシューティング

### よくあるエラー

| エラー | 原因 | 解決策 |
|--------|------|--------|
| `PERMISSION_DENIED` | セキュリティルール問題 | ルール確認、テストモード試行 |
| `UNAUTHENTICATED` | ユーザー未認証 | ログイン確認 |
| `QUOTA_EXCEEDED` | 無料プラン上限超過 | プラン移行またはコスト最適化 |
| `DEADLINE_EXCEEDED` | クエリが遅い | インデックス追加、クエリ最適化 |
| `NETWORK_ERROR` | ネットワーク接続問題 | オフライン対応、リトライ設定 |

## 参考資料

- [Firebase 公式ドキュメント](https://firebase.google.com/docs)
- [Firebase JavaScript SDK](https://firebase.google.com/docs/web/setup)
- [React での Firebase Authentication](https://reffect.co.jp/react/react-firebase-auth)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/start)

## 関連トピック

- [[CloudPlatforms]]：クラウドプラットフォーム全般
- [[BackendServices]]：バックエンド サービス
- [[React]]：React フレームワーク
- [[AgileDevelopment]]：アジャイル開発（迅速な開発に適している）
