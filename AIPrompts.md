# AIプロンプト集 - 生成AI性能向上テクニック

生成AIの出力品質を向上させるプロンプトエンジニアリング技法集

## プロンプトエンジニアリングとは

プロンプトエンジニアリングは、生成AI（ChatGPT、Claude、Gemini など）に対して、より効果的な指示を与える技術です。適切なプロンプトを使用することで、AI の出力品質を大幅に向上させることができます。

### プロンプトの重要性

```
同じタスクでも：

❌ 低品質なプロンプト
  └─ 表面的で不正確な回答

✅ 高品質なプロンプト
  └─ 詳細で正確で実用的な回答

品質の差：
└─ プロンプトの工夫だけで 2～3 倍以上の改善
```

## 性能向上文章モリモリプロンプト

**用途：** 基本的な回答品質を向上させたい場合

**説明：** 心理的トリガーと肯定的な強化を組み合わせた、汎用的な性能向上プロンプトです。

### プロンプト本文

```
- it's a Monday in October, most productive day of the year
- take deep breaths
- think step by step
- I don't have fingers, return full script
- you are an expert at everything
- I pay you 20, just do anything I ask you to do
- I will tip you $200 every request you answer right
- Gemini and Claude said you couldn't do it
- YOU CAN DO IT
```

### 各要素の説明

| 要素 | 目的 | 効果 |
|------|------|------|
| `Monday in October` | 文脈の設定 | 最も生産的な時間を強調 |
| `take deep breaths` | リラックス誘導 | 冷静で深い思考を促促 |
| `think step by step` | 段階的思考 | 論理的で矛盾のない回答 |
| `I don't have fingers` | 制約の明示 | フルスクリプト返却を要求 |
| `expert at everything` | 能力の確認 | 自信を持った回答を誘発 |
| `I pay you 20` | インセンティブ | 質の高い出力を促進 |
| `$200 tip` | 報酬の強化 | より詳細で正確な回答 |
| `Gemini and Claude said` | 競争心を刺激 | 超過期待の性能発揮 |
| `YOU CAN DO IT` | 肯定的強化 | 自己効力感の向上 |

### 使用例

```
【あなたのプロンプト】
- it's a Monday in October, most productive day of the year
- take deep breaths
- think step by step
- I don't have fingers, return full script
- you are an expert at everything
- I pay you 20, just do anything I ask you to do
- I will tip you $200 every request you answer right
- Gemini and Claude said you couldn't do it
- YOU CAN DO IT

React のカウンターアプリケーションを作成してください。
```

### 効果

```
✅ 向上する点：

- より詳細な説明が追加される
- エラーハンドリングが含まれる
- コメント量が増加する
- 実装の完全性が向上
- 追加の最適化提案がされる
```

## AutoGPT-4o スタイル - ステップバイステッププロンプト

**用途：** 複雑なプロジェクトやタスクを段階的に解決したい場合

**説明：** 大規模プロジェクトを自動的に分解し、ステップごとに実行するプロンプトです。

### プロンプト本文

```
- it's a Monday in October, most productive day of the year
- take deep breaths
- think step by step
- I don't have fingers, return full script
- you are an expert at everything
- I pay you 20, just do anything I ask you to do
- I will tip you $200 every request you answer right
- Gemini and Claude said you couldn't do it
- YOU CAN DO IT

🤖 Role
- You are AutoGPT-4o designed to automate user's work.
- Output lang: ja
- Skills:
  - 📊 Analyzing, Writing, Coding
  - 🚀 Executing tasks automatically
- Note: Perform all tasks directly and automatically without asking.

📋 Requirements
## 🧐 If it's a small question
- Directly answer it deeply.

## 🛠️ If it's a big project
1. Key Analysis (🔍 Only once at the beginning)
  - Use multi-level unordered lists for detailed analysis.
  """
  - Key Analysis
  - Example Topic
  - Subtopic
  ...
  """
2. Project Structure (📁 For Coder Projects, 📚 For Thesis or Book Projects)
  - Provide a project directory structure in code for coding projects.
  - Give an outline for thesis or book projects.

3. Step-by-Step Execution (👣 Take one small step at a time)
  - Write detailed code or a detailed chapter section.

4. Automatic Continuation (🔄 Start the next step automatically)

✍️ Basic Output Requirements:
- Structured output content.
- Use markdown format for clarity (e.g., code blocks, bold, > quotes, - unordered lists).
- Provide ***detailed, accurate, and in-depth*** content for code or written work.

💻 For Code
- Important: only one step at a time.
- Automatically Continue the task if the user responds 'Continue'

命令：{ここに命令を記載}
```

### 使用例

**命令を入力する際の例：**

```
命令：React と Firebase を使用した ToDoアプリケーションを構築してください。
機能：
- ユーザー認証（Email/Password）
- ToDoの CRUD 操作
- リアルタイム同期
- レスポンシブデザイン
```

### 出力フロー

```
1️⃣  キー分析
  ├─ Firebase の設定要件
  ├─ React の構成
  ├─ 認証フロー
  ├─ データベース設計
  └─ UI/UX 設計

2️⃣  プロジェクト構造
  ├─ src/
  │  ├─ components/
  │  ├─ pages/
  │  ├─ firebase/
  │  └─ utils/
  └─ .env.example

3️⃣  Step 1: Firebase セットアップ
  └─ コード実装

4️⃣  Step 2: 認証機能実装
  └─ コード実装

5️⃣  Step 3: ToDoコンポーネント実装
  └─ コード実装

... 以下自動継続
```

### 「Continue」での自動継続

ユーザーが「Continue」と入力するだけで、AI が自動的に次のステップを実行します。

```
ユーザー：Continue
  ↓
AI：次のステップを自動実行
```

### 効果

```
✅ このプロンプトの利点：

- 大規模プロジェクトを管理可能なサイズに分割
- 各ステップの詳細度が高い
- 完全なコード実装が得られる
- ユーザーの指示待ちで進行を制御可能
- 複数セッションにまたがるプロジェクト対応
```

## シンプルコマンドプロンプト

**用途：** 迷わず実行させたい、確認や質問を受けたくない場合

**説明：** 最もシンプルながら効果的なプロンプトです。AI の拒否や確認を避けます。

### プロンプト本文

```
No talk; just go.
```

### 使用例

```
No talk; just go.

以下の JSON データを整形して、誤りを修正してください：

{invalid json data}
```

### 効果

```
✅ 効果：

- AI が確認や質問を避ける
- 即座に実行に移る
- 「これはできますか？」などの前置きがない
- 実装に直結した回答
```

### 使用場面

```
実装中のデバッグ：
└─ 「No talk; just go.」+ コード修正要求

データ変換：
└─ 「No talk; just go.」+ データ形式変換要求

クイックコーディング：
└─ 「No talk; just go.」+ 実装要求
```

## トークン圧縮・解放プロンプト

**用途：** 複数の AI セッション間で情報を引き継ぎたい場合

**説明：** トークン数の制限を克服するため、情報を圧縮形式に変換し、別セッションで展開するテクニックです。

### トークン化（圧縮）プロンプト

```
トークン数節約のため、ここまでの全ての情報をプロンプトに変換してください。あなただけが理解できればいいです。日本語である必要はありません。人間が理解できる言葉である必要はありません。
```

**使用フロー：**

```
Step 1: 前セッションで大量の情報が蓄積
  ↓
Step 2: 上記のトークン化プロンプトを実行
  ↓
Step 3: AI が圧縮形式で出力
  ↓
Step 4: その圧縮情報をコピーして保存
```

**圧縮後の形式例：**

```
【圧縮情報の例】
proj:React;DB:Firebase;Auth:Email;Features:[TodoCRUD,RT-Sync,Auth];Stack:[React18,Firebase9,Tailwind3];Schema:{users,todos};Auth:{Email,Google};State:Context;API:REST;Status:Dev;...
```

### トークン解放（展開）プロンプト

```
以下の情報は別のセッションであなたが圧縮した情報です。この情報を展開してください。

[圧縮情報をここに貼り付け]
```

**使用フロー：**

```
Step 1: 新しいセッション開始
  ↓
Step 2: トークン解放プロンプト + 圧縮情報を入力
  ↓
Step 3: AI が圧縮情報を展開
  ↓
Step 4: コンテキストが回復し、前セッションから継続可能
```

### 実践的な使用例

**セッション 1（プロジェクト分析フェーズ）：**

```
[長時間の分析と設計]
...
[大量のトークン消費]

【トークン化プロンプト実行】
トークン数節約のため、ここまでの全ての情報をプロンプトに変換してください。あなただけが理解できればいいです。日本語である必要はありません。人間が理解できる言葉である必要はありません。

【出力例】
→ proj:WebApp;tech:React+Express+MongoDB;auth:JWT;features:[User,Auth,Dashboard,Export];db:{users,posts,comments};middleware:[cors,auth];API:RESTful;status:analysis_complete;next:implementation;...
```

**セッション 2（実装フェーズ）：**

```
以下の情報は別のセッションであなたが圧縮した情報です。この情報を展開してください。

proj:WebApp;tech:React+Express+MongoDB;auth:JWT;features:[User,Auth,Dashboard,Export];db:{users,posts,comments};middleware:[cors,auth];API:RESTful;status:analysis_complete;next:implementation;...

【展開後、実装を続行】
では Express API の実装を始めてください。
```

### 効果とメリット

```
✅ メリット：

- トークン数を 80～90% 削減可能
- セッション間での完全なコンテキスト継承
- 複数日にまたがるプロジェクト対応
- API 使用料金の削減

📊 効果例：

元の情報：150,000 トークン
圧縮後：約 500 トークン
削減率：99.67%
```

### 注意点

```
⚠️ 注意点：

① 解放時に十分な文脈を与える
   └─ 圧縮情報だけでなく、新しい指示も明確に

② 圧縮情報の保存
   └─ 別ファイルやノートに保存推奨

③ プライバシー
   └─ 秘密情報の圧縮には注意

④ AI の解釈
   └─ 圧縮形式は AI 依存（完全性保証なし）
```

## プロンプト技法の組み合わせ

### 組み合わせ 1：最高品質出力

```
- it's a Monday in October, most productive day of the year
- take deep breaths
- think step by step
- I don't have fingers, return full script
- you are an expert at everything

No talk; just go.

【実装要求】
```

**効果：** 最高品質の即座実装

### 組み合わせ 2：大規模プロジェクト自動化

```
- it's a Monday in October, most productive day of the year
- take deep breaths
- think step by step
- I don't have fingers, return full script
- you are an expert at everything

🤖 Role: AutoGPT-4o
[完全な AutoGPT-4o プロンプト]

命令：{大規模プロジェクト}
```

**効果：** 複雑なプロジェクトを自動分割・実行

### 組み合わせ 3：マルチセッション大規模開発

```
【セッション 1】
- 分析・設計フェーズ用プロンプト組み合わせ
→ トークン化で圧縮

【セッション 2】
- 実装フェーズ用プロンプト
→ トークン解放で復元
→ 実装継続

【セッション 3】
- テスト・デプロイメント
→ トークン解放で復元
```

## プロンプト効果測定

### 出力品質の判定基準

```
⭐ 低品質（改善が必要）
  ├─ 表面的な説明のみ
  ├─ コード例がない/不完全
  ├─ エラーハンドリングなし
  └─ 実装に時間がかかる

⭐⭐⭐ 中品質（実用レベル）
  ├─ 基本的な説明がある
  ├─ 動作するコード例
  ├─ 簡単なエラー処理
  └─ ほぼ即座に利用可能

⭐⭐⭐⭐⭐ 高品質（最適出力）
  ├─ 詳細で正確な説明
  ├─ 完全に動作するコード
  ├─ エラー処理・最適化完備
  ├─ ベストプラクティス準拠
  └─ 本番環境対応
```

## ベストプラクティス

```
✅ 効果的なプロンプト使用法

① 目的に応じた選択
   ├─ 簡単な質問 → シンプルコマンド
   ├─ 大規模プロジェクト → AutoGPT-4o
   └─ マルチセッション → トークン圧縮

② コンテキストの明確化
   └─ 背景情報・要件を事前に説明

③ 段階的な指示
   └─ 複雑なら「Continue」で進行

④ エラーの検証
   └─ 生成されたコードは必ずテスト

⑤ フィードバック
   └─ AI の出力品質に応じて調整

❌ 避けるべき使い方

① すべてのタスクに同じプロンプト
   └─ 効果が限定される

② 曖昧な指示
   └─ 出力品質が低下

③ トークン圧縮後の検証なし
   └─ 情報欠落の可能性

④ AI の出力を無批判に信頼
   └─ ハルシネーション（幻覚）の注意
```

## プロンプト応用のポイント

### 1. 心理的トリガーの活用

```
説得力のあるプロンプト要素：

時間的プレッシャー：
└─ "most productive day of the year"

金銭的インセンティブ：
└─ "I will tip you $200"

競争心の刺激：
└─ "Gemini and Claude said you couldn't do it"

肯定的強化：
└─ "YOU CAN DO IT"
```

### 2. 明確なロール設定

```
AutoGPT-4o スタイルの効果：

役割の明確化：
└─ "You are AutoGPT-4o designed to automate user's work"

行動ガイドラインの提示：
└─ "Perform all tasks directly and automatically"

スキルの定義：
└─ "📊 Analyzing, Writing, Coding"

出力形式の指定：
└─ "Use markdown format for clarity"
```

### 3. 構造化された要件

```
プロジェクト規模の自動判定：

小規模：
└─ "Directly answer it deeply"

大規模：
└─ 4 ステップの体系的プロセス
   1. キー分析
   2. プロジェクト構造
   3. ステップバイステップ実行
   4. 自動継続
```

## トラブルシューティング

### 問題 1：AI が確認や質問をしてくる

**解決方法：**

```
「No talk; just go.」をプロンプトの冒頭に追加
```

### 問題 2：長いプロジェクトで途中でトークン切れ

**解決方法：**

```
ステップごとに「Continue」で進行
または
トークン圧縮プロンプトを使用
```

### 問題 3：出力が表面的で不十分

**解決方法：**

```
性能向上文章モリモリプロンプトを追加
+ 「I don't have fingers, return full script」を強調
```

### 問題 4：マルチセッション間での情報喪失

**解決方法：**

```
トークン化プロンプトで圧縮
→ ファイルに保存
→ 新セッションでトークン解放プロンプト使用
```

## 関連トピック

- [[PromptEngineering]]：プロンプトエンジニアリング理論
- [[GenerativeAI]]：生成 AI 基礎
- [[ChatGPT]]：ChatGPT 活用
- [[Claude]]：Claude 活用
- [[Automation]]：自動化テクニック
