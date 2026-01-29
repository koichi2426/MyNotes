# Bitwise Tiling - ビットマスクを用いたタイル塗り分けパターン

ビットマスクを用いてグリッドのタイルを2色で均等に塗り分けるパターンを計算するアルゴリズム

## ビットマスクとは？

ビットマスクは、ビット列（0と1の並び）を使ってデータの特定の部分を管理する方法です。各ビットは特定のフラグや状態を表すために使用されます。ここでは、各ビットを使ってタイルがどの色に塗られているかを表します。

### ビットマスクとタイルの関係

以下の図は、ビットマスク `101010` がどのようにタイルの色を表現するかを示しています。

```
ビットマスク:  1  0  1  0  1  0

グリッド:
| 1色目 | 2色目 | 1色目 |
| 2色目 | 1色目 | 2色目 |
```

### ビットマスク操作の基本

```
操作名：説明：例

AND演算：複数ビットが全て1か判定
├─ `mask & (1 << i)` でi番目のビットが1か確認
└─ 結果が0以外なら1、0なら0

OR演算：特定ビットを1に設定
├─ `mask | (1 << i)` でi番目のビットを1に
└─ 既に1なら変わらない

XOR演算：特定ビットを反転
├─ `mask ^ (1 << i)` でi番目のビットを反転
└─ 0→1、1→0

シフト演算：ビット列の左右移動
├─ `mask << 1` で左シフト（2倍）
├─ `mask >> 1` で右シフト（1/2）
└─ `1 << total_tiles` で2^total_tiles生成

ポップカウント：1のビット数を計算
├─ `__builtin_popcount(mask)` で1の数を数える
└─ C++やGCCで使用可能
```

## アルゴリズムの実装

以下のコードは、ビットマスクを使用してタイルの塗り分けパターンを全探索する実装例です。

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

    // 二色で均等に塗り分けるための組み合わせを計算
    long long patterns = 0;
    int half_tiles = total_tiles / 2;

    // グリッドのサイズが小さいため全探索が可能
    // ビットマスクを使用して各組み合わせを試行する
    for (int mask = 0; mask < (1 << total_tiles); ++mask) {
        if (__builtin_popcount(mask) == half_tiles) {
            ++patterns;
            if (patterns >= MOD) {
                patterns -= MOD;
            }
        }
    }

    return patterns;
}
```

### コードの詳細説明

#### 入力処理

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
- `scanf` でグリッドのサイズ `m` と `n` を入力します
- 範囲チェック（1≤m,n≤10）を行います
- 無効な入力の場合は終了コード100で終了します
- 結果を9桁の0パディング付きで出力します

#### パターン計算の核

```c
long long count_color_patterns(int m, int n) {
    int total_tiles = m * n;

    // タイルの総数が奇数なら均等に塗り分けることはできない
    if (total_tiles % 2 != 0) {
        return 0;
    }

    long long patterns = 0;
    int half_tiles = total_tiles / 2;

    // グリッドのサイズが小さいため全探索が可能
    // ビットマスクを使用して各組み合わせを試行する
    for (int mask = 0; mask < (1 << total_tiles); ++mask) {
        if (__builtin_popcount(mask) == half_tiles) {
            ++patterns;
            if (patterns >= MOD) {
                patterns -= MOD;
            }
        }
    }

    return patterns;
}
```

**処理フロー：**

| ステップ | 処理 | 説明 |
|------|------|------|
| 1 | `total_tiles = m * n` | グリッドの総タイル数を計算 |
| 2 | `if (total_tiles % 2 != 0)` | 総数が奇数なら0を返す（均等分割不可） |
| 3 | `half_tiles = total_tiles / 2` | 1色あたりのタイル数を計算 |
| 4 | `for (int mask = 0; mask < (1 << total_tiles); ++mask)` | 全ての2^n個の組み合わせをループ |
| 5 | `if (__builtin_popcount(mask) == half_tiles)` | マスク内の1の数が丁度半分か判定 |
| 6 | `patterns++` | 条件を満たすパターンをカウント |
| 7 | `if (patterns >= MOD) patterns -= MOD` | MODで割った余りを保持 |

#### 具体例：2×2グリッド

```
グリッド：
+---+---+
| 0 | 1 |
+---+---+
| 2 | 3 |
+---+---+

total_tiles = 4
half_tiles = 2

探索するマスク（0000から1111）：

0000 → 0個が色1  ❌（必要：2個）
0001 → 1個が色1  ❌
0010 → 1個が色1  ❌
0011 → 2個が色1  ✓ パターン1
0100 → 1個が色1  ❌
0101 → 2個が色1  ✓ パターン2
0110 → 2個が色1  ✓ パターン3
0111 → 3個が色1  ❌
1000 → 1個が色1  ❌
1001 → 2個が色1  ✓ パターン4
1010 → 2個が色1  ✓ パターン5
1011 → 3個が色1  ❌
1100 → 2個が色1  ✓ パターン6
1101 → 3個が色1  ❌
1110 → 3個が色1  ❌
1111 → 4個が色1  ❌

答え：6パターン

実は、これはC(4,2) = 6 と同じです
```

## Python実装例

```python
def count_color_patterns(m, n):
    """
    ビットマスクを使ってタイルの塗り分けパターンを計算
    
    Args:
        m: グリッドの高さ
        n: グリッドの幅
    
    Returns:
        2色で均等に塗り分けるパターン数
    """
    MOD = 1000000000
    total_tiles = m * n
    
    # 奇数個のタイルは均等分割不可
    if total_tiles % 2 != 0:
        return 0
    
    half_tiles = total_tiles // 2
    patterns = 0
    
    # 全てのビットマスク組み合わせを試行
    for mask in range(1 << total_tiles):
        # mask内の1のビット数をカウント
        if bin(mask).count('1') == half_tiles:
            patterns += 1
            patterns %= MOD
    
    return patterns

# 使用例
m, n = map(int, input().split())
result = count_color_patterns(m, n)
print(f"{result:09d}")
```

**Python特有の実装：**
- `bin(mask).count('1')` でビット数をカウント
- `range(1 << total_tiles)` で0から2^n-1までループ
- モジュロ演算で値の範囲を制御

## アルゴリズムの計算量分析

### 時間計算量

```
ビットマスクのループ：O(2^(m*n))
├─ m=2, n=2 → 2^4 = 16 回
├─ m=3, n=3 → 2^9 ≈ 512 回
├─ m=4, n=4 → 2^16 ≈ 65,536 回
└─ m=5, n=5 → 2^25 ≈ 33,554,432 回

ポップカウント操作：O(1)
├─ CPUの組み込み命令
└─ 単一サイクル

全体：O(2^(m*n))
```

### 空間計算量

```
使用メモリ：O(1)
├─ マスク変数：8バイト
├─ パターンカウント：8バイト
├─ ループ変数：4バイト
└─ その他定数
```

### 実行時間の目安

| グリッド | タイル数 | 組み合わせ | 実行時間 |
|------|------|------|------|
| 2×2 | 4 | 2^4 = 16 | < 1ms |
| 2×3 | 6 | 2^6 = 64 | < 1ms |
| 3×3 | 9 | 2^9 = 512 | < 1ms |
| 3×4 | 12 | 2^12 = 4,096 | < 1ms |
| 4×4 | 16 | 2^16 = 65,536 | 1-10ms |
| 5×5 | 25 | 2^25 ≈ 33M | 1-10秒 |
| 6×6 | 36 | 2^36 ≈ 68B | 実用的でない |

## 最適化方法

### 1. ビット演算の活用

```c
// 遅い：ポップカウントを毎回計算
for (int mask = 0; mask < (1 << n); ++mask) {
    if (__builtin_popcount(mask) == target) {
        count++;
    }
}

// 高速：組み合わせを直接生成
int mask = 0;
for (int i = 0; i < target; ++i) {
    mask |= (1 << i);  // 最初のtarget個のビットを1に
}

// 次の組み合わせを生成するゴスパー法
do {
    // maskを処理
    int c = mask & -mask;
    int r = mask + c;
    mask = (((r ^ mask) >> 2) / c) | r;
} while (mask < (1 << total_tiles));
```

### 2. 対称性の活用

```c
// 回転・反転対称性を考慮
long long count_unique_patterns(int m, int n) {
    // 半分のマスクだけチェック
    // 残りは対称性から計算可能
    
    long long all_patterns = count_color_patterns(m, n);
    
    // 対称性係数で割る
    // （実装は複雑）
    
    return all_patterns;
}
```

### 3. メモ化の導入

```c
// DP + ビットマスク
long long dp[1 << MAX_TILES];

long long count_with_memo(int mask, int target, int counted) {
    if (counted == target) {
        return 1;  // 条件を満たすパターン
    }
    
    if (dp[mask] != -1) {
        return dp[mask];  // メモから取得
    }
    
    long long result = 0;
    // 再帰的に次のビットを試行
    
    return dp[mask] = result;
}
```

## 数学的背景

### 組み合わせ数との関係

```
ビットマスク方式の答え = C(total_tiles, half_tiles)

例：
m=2, n=2 → 4タイル
答え = C(4, 2) = 4! / (2! × 2!) = 6

m=3, n=3 → 9タイル（奇数）
答え = 0（均等分割不可）

m=3, n=2 → 6タイル
答え = C(6, 3) = 6! / (3! × 3!) = 20
```

### パスカルの三角形を利用した計算

```
C(n, k) = C(n-1, k-1) + C(n-1, k)

例：C(6, 3) = C(5, 2) + C(5, 3)
         = 10 + 10
         = 20
```

## 制限事項と改善提案

### 現在の制限

```
❌ グリッドサイズが限定（10×10まで）
❌ 2^(m*n) の指数計算量
❌ 大きなグリッドで実行不可（6×6以上で困難）
❌ メモリ効率が悪い（大規模ビットマスク）
```

### 改善方向

| 改善方法 | 効果 | 難易度 |
|------|------|------|
| **動的計画法** | O(m×n×2^min(m,n)) に削減 | 高 |
| **行プロファイル最適化** | メモリ効率化 | 中 |
| **並列化** | CPU複数コアで高速化 | 中 |
| **数学的公式** | O(1)で計算（特殊ケース） | 低 |
| **ゴスパー法** | ポップカウント固定で高速化 | 中 |

#### 行プロファイルDP（高度な最適化）

```c
// グリッドを行単位で処理
// メモリ：O(2^n) に削減（n = グリッド幅）

long long count_patterns_optimized(int m, int n) {
    int row_masks = 1 << n;
    
    // dp[row][mask] = row番目までで状態maskの場合の数
    long long dp[m + 1][row_masks];
    
    memset(dp, 0, sizeof(dp));
    dp[0][0] = 1;
    
    for (int row = 0; row < m; ++row) {
        for (int mask = 0; mask < row_masks; ++mask) {
            if (dp[row][mask] == 0) continue;
            
            // 次の行の全パターンを試行
            for (int next_mask = 0; next_mask < row_masks; ++next_mask) {
                // マスクが有効か確認
                if (is_valid_transition(mask, next_mask, n)) {
                    dp[row + 1][next_mask] += dp[row][mask];
                    dp[row + 1][next_mask] %= MOD;
                }
            }
        }
    }
    
    // 全体がバランスしているmaskをカウント
    long long result = 0;
    for (int mask = 0; mask < row_masks; ++mask) {
        if (is_balanced(mask, m, n)) {
            result += dp[m][mask];
            result %= MOD;
        }
    }
    
    return result;
}
```

## 応用例

### 1. チェッカーボード生成

```
ビットマスク：交互パターン
├─ 010101010101...
└─ 101010101010...

用途：テクスチャ生成、ゲーム盤
```

### 2. パリティチェック

```
ビットマスク：誤り検出符号（ECC）
├─ データのビット数をチェック
└─ 偶数パリティ or 奇数パリティ
```

### 3. ナップサック問題

```
ビットマスク：部分集合選択
├─ n個の品物から部分集合を選択
└─ 最大価値を求める
```

### 4. グラフの部分グラフ列挙

```
ビットマスク：頂点選択
├─ n個の頂点から部分集合を選択
└─ 連結性、独立集合など性質チェック
```

## まとめ

### ビットマスク方式の特徴

```
✅ メリット
├─ 実装がシンプル
├─ 全パターン必ず列挙
└─ デバッグが容易

❌ デメリット
├─ 指数時間かかる
├─ 大規模データ不可
└─ メモリ効率が悪い
```

### 使い分けの目安

```
グリッドサイズ判定：

小規模（2×2 ～ 4×4）
└─ ビットマスク全探索で十分

中規模（5×5 ～ 10×10）
├─ 行プロファイルDP検討
└─ 最適化版ビットマスク

大規模（10×10 以上）
├─ 高度なDP
├─ 数学的アプローチ
└─ 近似アルゴリズム
```

### 学習価値

ビットマスクを用いたアルゴリズムは、競技プログラミングやアルゴリズム学習において重要な技巧です。

**学べること：**
- ビット演算の実践的活用
- 全探索の考え方
- 計算量分析の重要性
- 大規模問題への段階的アプローチ

**関連トピック：**
- [[Algorithm]]：アルゴリズム基礎
- [[AlgorithmTheory]]：アルゴリズム理論
- 動的計画法（DP）
- グラフアルゴリズム
