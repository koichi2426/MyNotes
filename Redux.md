# Redux

JavaScriptアプリケーションの状態管理ライブラリ

## 概要

[[Redux]]は、JavaScriptアプリケーションの状態管理ライブラリです。特に[[React]]と組み合わせて使用されることが多く、アプリケーションの状態を予測可能に管理するためのツールを提供します。Reduxは、状態の一元管理、予測可能な状態遷移、およびテスト可能なコードの作成を支援します。

## Reduxの基本原則

### 1. シングルソースオブトゥルース（Single Source of Truth）

アプリケーション全体の状態が一つのオブジェクトツリーとしてストア（store）に保存されます。この一元管理されたストアにより、どのコンポーネントからも同じ状態を参照できるようになり、状態の一貫性が保たれます。

### 2. 状態は読み取り専用（State is Read-Only）

状態を直接変更することはできません。状態を変更する唯一の方法は、アクション（action）をディスパッチ（dispatch）することです。アクションは、状態の変更を表すプレーンなJavaScriptオブジェクトで、必ず`type`プロパティを持ちます。

### 3. 純粋関数であるリデューサー（Reducers）

状態の変更を行うロジックは、リデューサー（reducers）と呼ばれる純粋関数に含まれます。リデューサーは、現在の状態とアクションを受け取り、新しい状態を返す関数です。リデューサーは副作用を持たず、同じ入力に対して必ず同じ出力を返すことが求められます。

## 基本的な使い方

### ストアの作成

Reduxでは、まずストアを作成します。ストアは、アプリケーション全体の状態を保持するオブジェクトです。

```javascript
import { createStore } from 'redux';
import rootReducer from './reducers';

const store = createStore(rootReducer);
```

### アクションの定義

アクションは、状態の変更を表すプレーンなJavaScriptオブジェクトです。

```javascript
const increment = {
  type: 'INCREMENT'
};

const decrement = {
  type: 'DECREMENT'
};
```

### リデューサーの作成

リデューサーは、現在の状態とアクションを受け取り、新しい状態を返す関数です。

```javascript
const initialState = { count: 0 };

function counterReducer(state = initialState, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 };
    case 'DECREMENT':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

export default counterReducer;
```

### ストアの使用

```javascript
import { createStore } from 'redux';
import counterReducer from './counterReducer';

const store = createStore(counterReducer);

// 状態の取得
console.log(store.getState()); // { count: 0 }

// アクションのディスパッチ
store.dispatch({ type: 'INCREMENT' });
console.log(store.getState()); // { count: 1 }
```

## Reactとの連携

`react-redux`ライブラリを使用すると、ReactコンポーネントとReduxストアを簡単に接続できます。

```javascript
import React from 'react';
import { Provider, connect } from 'react-redux';
import { createStore } from 'redux';

const Counter = ({ count, increment, decrement }) => (
  <div>
    <h1>{count}</h1>
    <button onClick={increment}>Increment</button>
    <button onClick={decrement}>Decrement</button>
  </div>
);

const mapStateToProps = state => ({ count: state.count });
const mapDispatchToProps = dispatch => ({
  increment: () => dispatch({ type: 'INCREMENT' }),
  decrement: () => dispatch({ type: 'DECREMENT' })
});

const ConnectedCounter = connect(mapStateToProps, mapDispatchToProps)(Counter);
```

## セットアップ手順

### ステップ1: プロジェクトのセットアップ

```bash
npx create-react-app redux-example
cd redux-example
npm install redux react-redux
```

### ステップ2: アクションの定義

```javascript
// src/actions/index.js
export const increment = () => ({
  type: 'INCREMENT'
});

export const decrement = () => ({
  type: 'DECREMENT'
});
```

### ステップ3: リデューサーの作成

```javascript
// src/reducers/counter.js
const initialState = { count: 0 };

const counterReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'INCREMENT':
      return { ...state, count: state.count + 1 };
    case 'DECREMENT':
      return { ...state, count: state.count - 1 };
    default:
      return state;
  }
};

export default counterReducer;
```

### ステップ4: ストアの作成

```javascript
// src/store/index.js
import { createStore } from 'redux';
import rootReducer from '../reducers';

const store = createStore(rootReducer);
export default store;
```

### ステップ5: Providerの設定

```javascript
// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from './App';
import store from './store';

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);
```

## Redux Toolkitを使った簡単な実装

Redux Toolkitは、Reduxの公式ツールキットで、冗長なコードを簡素化します。

### スライスの作成

```typescript
// src/features/counter/counterSlice.ts
import { createSlice } from '@reduxjs/toolkit';

const counterSlice = createSlice({
    name: 'counter',
    initialState: { value: 0 },
    reducers: {
        increment: state => {
            state.value += 1;
        },
        decrement: state => {
            state.value -= 1;
        }
    }
});

export const { increment, decrement } = counterSlice.actions;
export default counterSlice.reducer;
```

### Storeの設定

```typescript
// src/app/store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';

export const store = configureStore({
    reducer: {
        counter: counterReducer,
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### useSelectorとuseDispatch

```typescript
// カウンター表示コンポーネント
import { useSelector } from 'react-redux';
import { RootState } from '../../app/store';

const CounterDisplay = () => {
    const count = useSelector((state: RootState) => state.counter.value);
    return <h1>カウンターの値: {count}</h1>;
};

// カウンター操作コンポーネント
import { useDispatch } from 'react-redux';
import { increment, decrement } from './counterSlice';

const CounterControls = () => {
    const dispatch = useDispatch();
    return (
        <div>
            <button onClick={() => dispatch(increment())}>増やす</button>
            <button onClick={() => dispatch(decrement())}>減らす</button>
        </div>
    );
};
```

## 重要な概念

- **Store**: アプリケーション全体の状態を保持する場所
- **Action**: 状態の変更を表すオブジェクト
- **Reducer**: 現在の状態とアクションから新しい状態を返す純粋関数
- **Dispatch**: アクションを発行して状態を更新する関数
- **Slice**: 状態とリデューサーをひとまとめにしたもの（Redux Toolkit）
- **Provider**: Reactコンポーネント全体にStoreを提供するコンポーネント
- **useSelector**: Storeから状態を取得するフック
- **useDispatch**: アクションをディスパッチするフック

## まとめ

Reduxは、アプリケーションの状態管理をシンプルかつ予測可能にするための強力なツールです。シングルソースオブトゥルース、状態の読み取り専用、純粋関数であるリデューサーという3つの基本原則により、状態管理の一貫性と予測可能性が向上します。[[React]]と組み合わせることで、より効率的で保守しやすいコードベースを実現できます。
