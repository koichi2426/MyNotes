# LocalStorage

ブラウザのローカルストレージ

## 概要

ローカルストレージ（LocalStorage）は、HTML5で導入されたWebストレージAPIの一部で、ブラウザにデータを保存するための機能です。セッションストレージとは異なり、ローカルストレージに保存されたデータはブラウザを閉じても保持され、再度開いたときに利用可能です。

## 利点

### 永続性

ローカルストレージに保存されたデータはブラウザを閉じても削除されず、ユーザーが手動で削除するか、JavaScriptを使用して明示的に削除するまで保持されます。

### 大容量

[[クッキー]]よりも多くのデータを保存できます。一般的には5MBのデータを保存可能です。

### 簡単な使用方法

JavaScriptを使って簡単にデータの保存、取得、削除が行えます。

## 欠点

### セキュリティの脆弱性

ローカルストレージはクライアントサイドで動作するため、データはユーザーにアクセス可能です。機密情報の保存には適していません。

### データの同期性の欠如

ローカルストレージはブラウザ固有のため、異なるデバイス間でデータを同期することはできません。

## 基本的な使用方法

### データの保存

```javascript
localStorage.setItem('key', 'value');

// 例: ユーザー名を保存
localStorage.setItem('username', 'John Doe');
```

### データの取得

```javascript
let username = localStorage.getItem('username');
console.log(username); // "John Doe"
```

### データの削除

```javascript
// 特定のデータを削除
localStorage.removeItem('username');

// すべてのデータをクリア
localStorage.clear();
```

## 実装例

### 基本的なHTML/JavaScript例

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>LocalStorage Example</title>
</head>
<body>
    <h1>Welcome, <span id="displayName"></span>!</h1>
    <input type="text" id="nameInput" placeholder="Enter your name">
    <button id="saveButton">Save</button>

    <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            const displayName = document.getElementById('displayName');
            const nameInput = document.getElementById('nameInput');
            const saveButton = document.getElementById('saveButton');

            // ローカルストレージから名前を取得して表示
            const storedName = localStorage.getItem('name');
            if (storedName) {
                displayName.textContent = storedName;
            }

            // ボタンがクリックされたときに名前を保存
            saveButton.addEventListener('click', () => {
                const name = nameInput.value;
                localStorage.setItem('name', name);
                displayName.textContent = name;
            });
        });
    </script>
</body>
</html>
```

## Reactアプリケーションへの導入

### ステップ1: Reactプロジェクトの作成

```bash
npx create-react-app button-state-app
cd button-state-app
```

### ステップ2: コンポーネントの実装

```javascript
// src/App.js
import React, { useState, useEffect } from 'react';

function App() {
    const [inputValue, setInputValue] = useState('');
    const [isButtonClicked, setIsButtonClicked] = useState(false);

    useEffect(() => {
        // コンポーネントがマウントされたときにローカルストレージからデータを読み込む
        const savedInputValue = localStorage.getItem('inputValue');
        const savedButtonState = localStorage.getItem('isButtonClicked') === 'true';
        if (savedInputValue) setInputValue(savedInputValue);
        setIsButtonClicked(savedButtonState);
    }, []);

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
        localStorage.setItem('inputValue', event.target.value); // 入力値をローカルストレージに保存
    };

    const handleButtonClick = () => {
        const newButtonState = !isButtonClicked;
        setIsButtonClicked(newButtonState);
        localStorage.setItem('isButtonClicked', newButtonState); // ボタンの状態をローカルストレージに保存
    };

    return (
        <div>
            <h1>ローカルストレージのデモ</h1>
            <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                placeholder="入力してください"
            />
            <button onClick={handleButtonClick}>
                {isButtonClicked ? 'クリック済み' : 'クリックされていません'}
            </button>
        </div>
    );
}

export default App;
```

### 実装のポイント

1. **状態管理**: `useState`フックを使って入力フィールドの値とボタンの状態を管理
2. **ローカルストレージの読み込み**: `useEffect`フックでコンポーネントマウント時にデータを読み込み
3. **入力変更ハンドラ**: 入力値の変更時にローカルストレージに保存
4. **ボタンクリックハンドラ**: ボタンの状態をローカルストレージに保存

### ステップ3: アプリケーションの実行

```bash
npm start
```

ブラウザで`http://localhost:3000`にアクセスし、動作を確認します。ページを再読み込みしても、入力値とボタンの状態が保持されていることを確認できます。

## クッキーとの違いと使い分け

### クッキーの特徴

**利点:**
- サーバーとクライアント間でデータをやり取り可能
- 有効期限を設定できる
- サーバーサイドのセッション管理に適している

**欠点:**
- データ容量が小さい（約4KB）
- セキュリティリスク（XSS、CSRF攻撃の対象）
- パフォーマンスへの影響（サーバーへの送信が必要）

### ローカルストレージの特徴

**利点:**
- 大容量（一般的に5MB）
- サーバーへのリクエストが不要でパフォーマンスに優れる
- サーバーに送信されないため比較的安全

**欠点:**
- デバイス間でのデータ同期ができない
- データが永続的に残る可能性がある

### 使い分けの指針

**[[Cookie]]を使うべき場合:**
1. サーバーサイドのセッション管理（ログイン情報、ユーザー認証）
2. 短期間のデータ保存（セッション終了後に削除されるべきデータ）
3. サーバーとクライアント間でのデータ共有

**LocalStorageを使うべき場合:**
1. クライアントサイドのデータ保存（ユーザー設定、テーマ、フォーム入力内容）
2. 大容量データの保存（クッキーの容量制限を超える場合）
3. パフォーマンス重視（サーバーリクエストを減らす場合）

## まとめ

ローカルストレージは、ユーザーのデータをブラウザに永続的に保存するための便利な機能です。しかし、セキュリティに注意し、適切なデータを保存するように心がける必要があります。クッキーとローカルストレージは、それぞれ異なる特性を持つため、用途に応じて使い分けることが重要です。

これらの特性を理解し、適切な場面で適切な技術を選択することで、より効率的でユーザーフレンドリーなWebアプリケーションを構築することができます。
