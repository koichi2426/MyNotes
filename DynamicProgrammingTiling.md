# Dynamic Programming Tiling - 動的計画法によるタイル塗り分けパターン計算

動的計画法（DP）を用いて、グリッドのタイルを2色で均等に塗り分けるパターンを計算するアルゴリズム

## 問題の言い換え

「グリッドのタイルを2色で均等に塗り分けるパターンの導出問題」を「各色で `half_tiles` 個のタイルを塗る組み合わせを数える問題」に言い換えることができます。

```c
int total_tiles = m * n;
int half_tiles = total_tiles / 2;
```

この言い換えにより、問題は **組み合わせ論的なDP問題** に変換されます。

## 動的計画法の基本概念

### DPとは

動的計画法（Dynamic Programming, DP）は、複雑な問題を解くための効率的な手法です。大きな問題を小さな部分問題に分割し、各部分問題の結果を保存することで、計算の重複を避けます。

### DPの3つの要素

```
① 最適部分構造（Optimal Substructure）
   └─ 全体の最適解が部分問題の最適解から構成される

② 部分問題の重複（Overlapping Subproblems）
   └─ 同じ部分問題が何度も現れる

③ メモ化（Memoization）
   └─ 計算結果を保存して再利用
```

### ボトムアップ vs トップダウン

| 手法 | 処理方向 | 実装 | メモリ |
|------|------|------|------|
| **ボトムアップ** | 小さい問題から大きい問題へ | ループ（反復） | 事前に配列確保 |
| **トップダウン** | 大きい問題から小さい問題へ | 再帰 + メモ化 | 必要な分だけ確保 |

## 問題への適用

### dp配列の定義

```
dp[j][k] = 
  "j個のタイルを色1で塗り、
   k個のタイルを色2で塗った場合の
   組み合わせ数"
```

### 具体例：2×2グリッド

```
total_tiles = 4
half_tiles = 2

dp[0][0] = 1（初期状態：何も塗っていない）
dp[0][1] = 1（タイルなし、色2を1個）→ 1通り
dp[0][2] = 1（タイルなし、色2を2個）→ 1通り
dp[1][0] = 1（色1を1個）→ 1通り
dp[1][1] = 2（色1を1個、色2を1個）→ 2通り
dp[1][2] = 1（色1を1個、色2を2個）→ 1通り
dp[2][0] = 1（色1を2個）→ 1通り
dp[2][1] = 2（色1を2個、色2を1個）→ 2通り
dp[2][2] = 1（色1を2個、色2を2個）→ 1通り

答え：dp[2][2] = 1

実は、これはC(4,2) = 6ではなく...
（注：実装の詳細で説明）
```

### 漸化式

```
dp[j][k] = dp[j-1][k] + dp[j][k-1]

理由：
- dp[j-1][k]：色1をj-1個、色2をk個使った状態から、
             色1を1個追加
- dp[j][k-1]：色1をj個、色2をk-1個使った状態から、
             色2を1個追加

パスカルの三角形と同じ構造
```

## アルゴリズムの実装

### 基本的なC実装

```c
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000000

// 関数のプロトタイプ宣言
long long count_color_patterns(int m, int n);
void handle_input_error();

int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) {
        handle_input_error();
    }

    // m, nの範囲チェック
    if (m < 1 || m > 10 || n < 1 || n > 10) {
        handle_input_error();
    }

    long long result = count_color_patterns(m, n);
    printf("%09lld\\n", result);

    return 0;
}

void handle_input_error() {
    exit(100);
}

long long count_color_patterns(int m, int n) {
    int total_tiles = m * n;

    // タイルの総数が奇数なら均等に塗り分けることはできない
    if (total_tiles % 2 != 0) {
        return 0;
    }

    int half_tiles = total_tiles / 2;

    // dp[i][j] = i個のタイルを色1で、j個のタイルを色2で塗った場合の組み合わせ数
    long long dp[half_tiles + 1][half_tiles + 1];
    
    // DP配列の初期化
    for (int i = 0; i <= half_tiles; ++i) {
        for (int j = 0; j <= half_tiles; ++j) {
            dp[i][j] = 0;
        }
    }

    dp[0][0] = 1; // 初期状態: 何も塗られていない = 1通り

    // DP計算
    for (int i = 1; i <= total_tiles; ++i) {
        for (int j = half_tiles; j >= 0; --j) {      // 降順
            for (int k = half_tiles; k >= 0; --k) {  // 降順
                if (j > 0) {
                    // 色1を使用
                    dp[j][k] = (dp[j][k] + dp[j - 1][k]) % MOD;
                }
                if (k > 0) {
                    // 色2を使用
                    dp[j][k] = (dp[j][k] + dp[j][k - 1]) % MOD;
                }
            }
        }
    }

    return dp[half_tiles][half_tiles];
}
```

### コード実行フロー

| ステップ | 処理 |
|------|------|
| 1 | 入力読み込み、範囲チェック |
| 2 | `total_tiles = m × n` を計算 |
| 3 | 奇数チェック：奇数なら0を返す |
| 4 | `half_tiles = total_tiles / 2` を計算 |
| 5 | `dp[half_tiles+1][half_tiles+1]` の配列を確保 |
| 6 | 全要素を0で初期化 |
| 7 | `dp[0][0] = 1` で初期状態を設定 |
| 8 | DP更新ループ実行 |
| 9 | `dp[half_tiles][half_tiles]` を返す |

### 入力処理

```c
int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) {
        handle_input_error();
    }

    // m, nの範囲チェック
    if (m < 1 || m > 10 || n < 1 || n > 10) {
        handle_input_error();
    }

    long long result = count_color_patterns(m, n);
    printf("%09lld\\n", result);

    return 0;
}

void handle_input_error() {
    exit(100);
}
```

**処理内容：**
- `scanf` でグリッドサイズ m, n を入力
- 範囲チェック（1 ≤ m, n ≤ 10）
- 無効入力で終了コード100
- 結果を9桁0パディングで出力

## 内側のループが降順である理由

### 降順ループが必須な理由

降順でループすることで、**同じイテレーション内で既に更新された値を再利用しない** ようにします。

### 昇順でループした場合の問題

```c
// ❌ 間違ったコード（昇順）
for (int i = 1; i <= total_tiles; ++i) {
    for (int j = 0; j <= half_tiles; ++j) {      // 昇順
        for (int k = 0; k <= half_tiles; ++k) {  // 昇順
            if (j > 0) {
                dp[j][k] = (dp[j][k] + dp[j - 1][k]) % MOD;
            }
            if (k > 0) {
                // ⚠️ 同じイテレーション内で既に更新された dp[j][k-1] を使用
                dp[j][k] = (dp[j][k] + dp[j][k - 1]) % MOD;
            }
        }
    }
}
```

**問題点：**
```
j=1, k=1 を計算時：

1. dp[1][1] += dp[0][1]  （OK：前のイテレーション）
2. dp[1][1] += dp[1][0]  （⚠️：同じイテレーション内で更新済み）

結果：dp[1][0]の新しい値が使われてしまう
     → 二重カウント発生
```

### 降順でループする利点

```c
// ✅ 正しいコード（降順）
for (int i = 1; i <= total_tiles; ++i) {
    for (int j = half_tiles; j >= 0; --j) {      // 降順
        for (int k = half_tiles; k >= 0; --k) {  // 降順
            if (j > 0) {
                dp[j][k] = (dp[j][k] + dp[j - 1][k]) % MOD;
            }
            if (k > 0) {
                // ✓ まだ更新されていない dp[j][k-1] を使用
                dp[j][k] = (dp[j][k] + dp[j][k - 1]) % MOD;
            }
        }
    }
}
```

**利点：**
```
j=2, k=2 を計算時（降順）：

1. dp[2][2] += dp[1][2]  （✓：高いインデックス）
2. dp[2][2] += dp[2][1]  （✓：高いインデックス）

結果：前のイテレーションの値のみを使用
     → 正確な計算
```

### メモリ最適化版（1次元DP）

```c
long long count_color_patterns_optimized(int m, int n) {
    int total_tiles = m * n;
    
    if (total_tiles % 2 != 0) {
        return 0;
    }
    
    int half_tiles = total_tiles / 2;
    
    // 1次元配列を使用（メモリ削減）
    long long dp[half_tiles + 1];
    
    for (int i = 0; i <= half_tiles; ++i) {
        dp[i] = 0;
    }
    
    dp[0] = 1;
    
    // 色の数（1～total_tiles）だけループ
    for (int i = 1; i <= total_tiles; ++i) {
        // 降順で更新（重要）
        for (int j = half_tiles; j >= 1; --j) {
            dp[j] = (dp[j] + dp[j - 1]) % MOD;
        }
    }
    
    return dp[half_tiles];
}
```

**最適化の効果：**
```
2次元版：O((half_tiles+1)^2) メモリ
例：10×10グリッド → dp[50][50] = 2,500要素

1次元版：O(half_tiles) メモリ
例：10×10グリッド → dp[50] = 50要素

削減率：98%
```

## Python実装例

### 基本実装

```python
def count_color_patterns(m, n):
    """
    動的計画法を使ってタイル塗り分けパターン数を計算
    
    Args:
        m: グリッドの高さ
        n: グリッドの幅
    
    Returns:
        2色で均等に塗り分けるパターン数
    """
    MOD = 1000000000
    total_tiles = m * n
    
    if total_tiles % 2 != 0:
        return 0
    
    half_tiles = total_tiles // 2
    
    # DP配列初期化
    dp = [[0] * (half_tiles + 1) for _ in range(half_tiles + 1)]
    dp[0][0] = 1
    
    # DP計算
    for i in range(1, total_tiles + 1):
        for j in range(half_tiles, -1, -1):      # 降順
            for k in range(half_tiles, -1, -1):  # 降順
                if j > 0:
                    dp[j][k] = (dp[j][k] + dp[j - 1][k]) % MOD
                if k > 0:
                    dp[j][k] = (dp[j][k] + dp[j][k - 1]) % MOD
    
    return dp[half_tiles][half_tiles]

# 使用例
m, n = map(int, input().split())
result = count_color_patterns(m, n)
print(f"{result:09d}")
```

### メモリ最適化版

```python
def count_color_patterns_optimized(m, n):
    """1次元DPを使った最適化版"""
    MOD = 1000000000
    total_tiles = m * n
    
    if total_tiles % 2 != 0:
        return 0
    
    half_tiles = total_tiles // 2
    
    # 1次元配列
    dp = [0] * (half_tiles + 1)
    dp[0] = 1
    
    for i in range(1, total_tiles + 1):
        for j in range(half_tiles, 0, -1):  # 降順
            dp[j] = (dp[j] + dp[j - 1]) % MOD
    
    return dp[half_tiles]
```

## ビットマスク全探索との比較

### 計算量比較

| 手法 | 時間計算量 | 空間計算量 | 実用範囲 |
|------|------|------|------|
| **ビットマスク全探索** | O(2^(m×n)) | O(1) | m,n ≤ 5 |
| **動的計画法** | O(m×n×(m×n)^2) | O((m×n/2)^2) | m,n ≤ 10 |
| **メモリ最適化DP** | O(m×n×(m×n)) | O(m×n) | m,n ≤ 20 |

### 実行時間の目安

```
グリッド       タイル数   ビットマスク      DP          最適化DP
2×2            4         < 1ms          < 1ms        < 1ms
3×3            9         < 1ms          < 1ms        < 1ms
4×4            16        1-10ms         1-10ms       < 1ms
5×5            25        1-10秒         10-100ms     < 1ms
6×6            36        実用的でない     100-500ms    10-50ms
10×10          100       実用的でない     実用的でない   1-5秒
```

### 手法の選択基準

```
グリッドが小さい（4×4以下）
  → どちらでも可、シンプルなビットマスク推奨

グリッドが中程度（5×5～10×10）
  → DP推奨（計算量が現実的）

グリッドが大きい（10×10以上）
  → メモリ最適化DP または 数学的アプローチ

グリッドが非常に大きい（20×20以上）
  → 数学的公式 or 近似アルゴリズム
```

## 具体例：段階的な計算

### 3×2グリッド（6タイル）の例

```
total_tiles = 6
half_tiles = 3

初期状態：
dp[0][0] = 1

i=1（1個目のタイル）後：
dp[0][0] = 1
dp[1][0] = 1（色1を使用）
dp[0][1] = 1（色2を使用）

i=2後：
dp[0][0] = 1
dp[1][0] = 1
dp[2][0] = 1
dp[0][1] = 1
dp[1][1] = 2
dp[0][2] = 1

i=3後：
dp[0][0] = 1
dp[1][0] = 1
dp[2][0] = 1
dp[3][0] = 1
dp[0][1] = 1
dp[1][1] = 2
dp[2][1] = 3
dp[0][2] = 1
dp[1][2] = 3
dp[0][3] = 1

...（省略）...

最終：
dp[3][3] = C(6,3) = 20
```

## トラブルシューティング

### よくある間違い

#### 1. 昇順でループしている

```c
// ❌ 間違い
for (int j = 0; j <= half_tiles; ++j) {
    for (int k = 0; k <= half_tiles; ++k) {
        // 処理
    }
}

// ✅ 正解
for (int j = half_tiles; j >= 0; --j) {
    for (int k = half_tiles; k >= 0; --k) {
        // 処理
    }
}
```

#### 2. 初期化漏れ

```c
// ❌ 間違い：初期化していない
long long dp[half_tiles + 1][half_tiles + 1];
dp[0][0] = 1;

// ✅ 正解：全て0で初期化
long long dp[half_tiles + 1][half_tiles + 1];
for (int i = 0; i <= half_tiles; ++i) {
    for (int j = 0; j <= half_tiles; ++j) {
        dp[i][j] = 0;
    }
}
dp[0][0] = 1;
```

#### 3. MOD処理漏れ

```c
// ❌ オーバーフロー可能
dp[j][k] = dp[j][k] + dp[j - 1][k] + dp[j][k - 1];

// ✅ 各ステップでMOD
dp[j][k] = (dp[j][k] + dp[j - 1][k]) % MOD;
dp[j][k] = (dp[j][k] + dp[j][k - 1]) % MOD;
```

### デバッグ方法

```c
// DP計算中にテーブルを出力
printf("After i=%d:\n", i);
for (int j = 0; j <= half_tiles; ++j) {
    for (int k = 0; k <= half_tiles; ++k) {
        printf("%lld ", dp[j][k]);
    }
    printf("\n");
}
printf("\n");
```

## 最適化戦略

### 1. 行プロファイル最適化（Advanced）

```c
// グリッドを行ごとに処理
// メモリ：O(2^n) に削減（n=グリッド幅）

long long count_patterns_row_profile(int m, int n) {
    int row_masks = 1 << n;
    
    // dp[row][mask] = row番目までで状態maskの場合の数
    long long dp[row_masks];
    long long next_dp[row_masks];
    
    // 初期化
    dp[0] = 1;
    memset(&dp[1], 0, (row_masks - 1) * sizeof(long long));
    
    for (int row = 0; row < m; ++row) {
        memset(next_dp, 0, sizeof(next_dp));
        
        for (int mask = 0; mask < row_masks; ++mask) {
            if (dp[mask] == 0) continue;
            
            for (int next_mask = 0; next_mask < row_masks; ++next_mask) {
                // マスク遷移が有効か確認
                if (is_valid_transition(mask, next_mask, n)) {
                    next_dp[next_mask] = (next_dp[next_mask] + dp[mask]) % MOD;
                }
            }
        }
        
        memcpy(dp, next_dp, sizeof(dp));
    }
    
    return dp[0];  // 最後に全て色1の状態
}
```

### 2. 並列化

```c
// OpenMP を使った並列化
#pragma omp parallel for collapse(2)
for (int j = half_tiles; j >= 0; --j) {
    for (int k = half_tiles; k >= 0; --k) {
        if (j > 0) {
            dp[j][k] = (dp[j][k] + dp[j - 1][k]) % MOD;
        }
        if (k > 0) {
            dp[j][k] = (dp[j][k] + dp[j][k - 1]) % MOD;
        }
    }
}
```

## パスカルの三角形との関係

### DP テーブル ≒ パスカルの三角形

```
パスカルの三角形：
        1
       1 1
      1 2 1
     1 3 3 1
    1 4 6 4 1

DP テーブル dp[i][j]：
     0  1  2  3  4
   +--+--+--+--+--+
 0 | 1| 1| 1| 1| 1|
   +--+--+--+--+--+
 1 | 1| 2| 3| 4| 5|
   +--+--+--+--+--+
 2 | 1| 3| 6|10|15|
   +--+--+--+--+--+
 3 | 1| 4|10|20|35|
   +--+--+--+--+--+
 4 | 1| 5|15|35|70|
   +--+--+--+--+--+

dp[i][j] = C(i+j, i) = C(i+j, j)
```

### 数学的意味

```
dp[half_tiles][half_tiles] = C(2×half_tiles, half_tiles)
                           = C(total_tiles, half_tiles)

つまり、total_tiles個から half_tiles個を選ぶ組み合わせ
```

## まとめ

### DP手法の特徴

```
✅ メリット
├─ 計算量が予測可能 O((m×n)^3)
├─ ビットマスクより大きいグリッドに対応
├─ ボトムアップで実装が直感的
└─ メモ化で最適化容易

❌ デメリット
├─ 2次元配列のメモリ必要
├─ 内側ループが降順の理由理解が必要
└─ 大規模グリッドではまだ非効率
```

### ビットマスク vs DP

```
ビットマスク：
├─ 小規模グリッド向け（≤5×5）
├─ 実装シンプル
└─ 計算量が指数的

DP：
├─ 中規模グリッド向け（≤10×10）
├─ 実装がやや複雑
└─ 計算量が多項式的
```

### 関連トピック

- [[BitwiseTiling]]：ビットマスク全探索アプローチ
- [[Algorithm]]：アルゴリズム基礎
- [[AlgorithmTheory]]：アルゴリズム理論
- 組み合わせ論
- パスカルの三角形
- 二項係数
