# async_await

JavaScriptの非同期処理の記法

## 概要

「async」は「function」の前に記述するだけで非同期処理を実行できる関数を定義できます。このような関数はPromiseを返すようになります。awaitはPromiseの処理結果が返ってくるまで**一時停止してくれる**演算子となります。

## 基本構文

```javascript
async function sample() {
    const result = await sampleResolve();
    
    // sampleResolve()のPromiseの結果が返ってくるまで以下は実行されない
    console.log(result);
}
```

## 基本的な使い方

```javascript
async function() { }
```

このように関数の前に「async」を記述すると、この関数はPromiseを返すようになります。

## 連続した非同期処理の例

### パターン1: 連続的に書く場合

```javascript
function sampleResolve(value) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(value);
        }, 1000);
    })
}

async function sample() {
    return await sampleResolve(5) * await sampleResolve(10) + await sampleResolve(20);
}

sample().then((v) => {
    console.log(v); // => 70
});
```

### パターン2: 複数の値を変数に保存

```javascript
async function sample2() {
    const a = await sampleResolve(5);
    const b = await sampleResolve(10);
    const c = await sampleResolve(20);
    return a * b + c;
}

sample2().then((v) => {
    console.log(v); // => 70
});
```

## ポイント

- `async` 関数は常に [[Promise]] を返す
- `await` キーワードは `async` 関数内でのみ使用可能
- `await` は処理が完了するまで実行を一時停止する
- エラーハンドリングは `try-catch` ブロックで行う

## 参考資料

- [【JavaScript入門】5分で理解！async / awaitの使い方と非同期処理の書き方](https://www.sejuku.net/blog/69618)
- [async/await 入門（JavaScript） - Qiita](https://qiita.com/soarflat/items/1a9613e023200bbebcb3)
