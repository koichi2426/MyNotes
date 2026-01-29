# ComfyUI: ノードベース画像生成ツール

## 概要

### ComfyUIとは

ComfyUIは、Stable Diffusion などの画像生成AI を簡単に使用できるノードベースのユーザーインターフェースです。複雑なコマンドラインやプログラミングを必要とせず、ビジュアルノードを組み合わせることで、強力な画像生成ワークフローを構築できます。

オープンソースプロジェクトとして開発されており、GPU の最適化とマルチプロセッシングにより、高速な画像生成処理が可能です。

### ComfyUIの特徴

#### 1. ノードベースのインターフェース

- **視覚的なワークフロー設計**：ノードをドラッグ&ドロップで接続
- **複雑な処理を直感的に**：パイプラインを可視化して構築
- **再利用可能な設定**：ワークフローを保存して再利用

#### 2. 高速処理

- **GPU 最適化**：NVIDIA CUDA、AMD ROCm に対応
- **効率的なメモリ管理**：大規模モデルも動作可能
- **バッチ処理**：複数の画像を同時生成

#### 3. 拡張性

- **カスタムノード対応**：独自のノードを作成可能
- **プラグイン機能**：コミュニティが作成したノード・機能が豊富
- **API 対応**：スクリプトから制御可能

#### 4. 完全無料・オープンソース

- **ライセンス**：GPL v3
- **GitHub で公開**：誰でも改造・拡張可能
- **月額費用なし**：ローカルで完全に動作

## 対応する画像生成モデル

### 主要なモデル

| モデル | 説明 | 用途 |
|--------|------|------|
| **Stable Diffusion 1.5** | 基準モデル | テキスト→画像 |
| **Stable Diffusion XL** | 高品質版 | 高解像度画像 |
| **ControlNet** | 構図制御 | ポーズ・レイアウト指定 |
| **LCM** | 高速生成 | リアルタイム処理 |
| **Flux** | 最新モデル | 高精度画像生成 |

## システム要件

### 必須

```
OS: Windows 10/11、macOS、Linux
Python: 3.8 以上
RAM: 8GB 以上（16GB 推奨）
GPU: NVIDIA（CUDA）または AMD（ROCm）
```

### GPU 別推奨スペック

| GPU | VRAM | 対応 | 推奨設定 |
|-----|------|------|---------|
| RTX 4090 | 24GB | ✅ | 最高品質 |
| RTX 4080 | 16GB | ✅ | 高品質 |
| RTX 4070 | 12GB | ✅ | 標準 |
| RTX 3080 | 10GB | ✅ | 低～標準 |
| RTX 3060 | 12GB | ✅ | 低品質 |
| CPU のみ | - | △ | 非常に遅い |

## インストール

### Windows での インストール

#### 1. Git のインストール

```bash
# Git for Windows をダウンロード
https://git-scm.com/download/win

# または Chocolatey を使用
choco install git
```

#### 2. ComfyUI のダウンロード

```bash
# リポジトリをクローン
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

#### 3. Python 環境の構築

```bash
# Python 仮想環境を作成
python -m venv venv

# 環境を有効化
.\venv\Scripts\activate

# 必要なパッケージをインストール
pip install -r requirements.txt
```

#### 4. GPU サポートのインストール

**NVIDIA CUDA の場合:**

```bash
# CUDA ツールキットをインストール
# https://developer.nvidia.com/cuda-downloads から最新版をダウンロード

# Python パッケージをインストール
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**AMD ROCm の場合:**

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
```

#### 5. Stable Diffusion モデルのダウンロード

```bash
# models フォルダを作成
mkdir models\checkpoints

# モデルをダウンロード
# https://huggingface.co/runwayml/stable-diffusion-v1-5 から
# model.safetensors をダウンロードして models\checkpoints に配置
```

### macOS でのインストール

```bash
# Homebrew からインストール
brew install git python

# リポジトリをクローン
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 仮想環境を作成
python3 -m venv venv
source venv/bin/activate

# 依存パッケージをインストール
pip install -r requirements.txt

# PyTorch をインストール（Apple Silicon の場合）
pip install torch torchvision torchaudio
```

### Linux でのインストール

```bash
# Ubuntu/Debian の場合
sudo apt-get install python3-venv python3-pip git

# リポジトリをクローン
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 仮想環境を構築
python3 -m venv venv
source venv/bin/activate

# パッケージをインストール
pip install -r requirements.txt

# CUDA 対応の場合
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## ComfyUI の起動と使い方

### サーバーの起動

```bash
# ComfyUI ディレクトリで実行
python main.py

# GPU を指定して実行（複数 GPU の場合）
python main.py --cuda-device 0

# CPU モードで実行（GPU がない場合）
python main.py --cpu
```

**出力例:**

```
starting web server on 127.0.0.1:8188
To see the GUI go to http://127.0.0.1:8188
```

### ブラウザで アクセス

`http://localhost:8188` にアクセスして ComfyUI の UI を開く

## ワークフロー（基本的な使い方）

### 1. テキスト→画像生成（基本フロー）

#### ワークフローの構成

```
1. Load Checkpoint
   ↓
2. CLIP Text Encode（Positive）→ テキスト入力
   ↓
3. CLIP Text Encode（Negative）→ ネガティブプロンプト
   ↓
4. KSampler → ステップ数、CFGスケール などを設定
   ↓
5. VAE Decode → 潜在表現を画像に変換
   ↓
6. Save Image → 画像を保存
```

#### ノード詳細

**Load Checkpoint:**
```
- ckpt_name: モデルファイルを選択
- 出力: MODEL, CLIP, VAE
```

**CLIP Text Encode:**
```
- text: プロンプト入力
- clip: Load Checkpoint から接続
- 出力: CONDITIONING
```

**KSampler:**
```
- seed: ランダムシード（-1 で自動）
- steps: 生成ステップ数（20-50）
- cfg: CFGスケール（7.0-15.0）
- sampler_name: サンプラー（DPM++, Euler など）
- scheduler: スケジューラー（karras, normal など）
```

**VAE Decode:**
```
- samples: KSampler から接続
- vae: Load Checkpoint から接続
- 出力: 画像
```

**Save Image:**
```
- filename_prefix: ファイル名プレフィックス
- images: VAE Decode から接続
```

### 2. 画像→画像生成（Img2Img）

```
1. Load Image → 元画像を読み込む
   ↓
2. VAE Encode → 画像を潜在空間に変換
   ↓
3. KSampler
   - denoise: 0.5-1.0（低いほど元画像に近い）
   ↓
4. VAE Decode
   ↓
5. Save Image
```

### 3. ControlNet での構図指定

```
1. Load Image → 参照画像
   ↓
2. ControlNet Processor
   - 処理タイプ: canny, openpose, depth など
   ↓
3. ControlNet Loader → ControlNet モデルを読み込む
   ↓
4. KSampler で ControlNet を適用
   - control_net: ControlNet Loader から接続
   - conditioning: ControlNet から接続
```

## よく使うノード集

### 画像・ビデオ操作

| ノード | 機能 |
|--------|------|
| **Load Image** | 画像ファイルを読み込む |
| **Save Image** | 画像を保存 |
| **Scale Image** | 画像をリサイズ |
| **Crop Image** | 画像をトリミング |
| **Image Composite** | 複数画像を合成 |

### テキスト処理

| ノード | 機能 |
|--------|------|
| **CLIP Text Encode** | テキストを CLIP にエンコード |
| **Conditioning Combine** | 複数のコンディショニングを結合 |
| **Conditioning Set Mask** | マスクを適用 |

### 生成・サンプリング

| ノード | 機能 |
|--------|------|
| **KSampler** | 潜在空間でサンプリング |
| **KSamplerAdvanced** | 詳細設定を含むサンプリング |
| **Latent Composite** | 潜在表現を合成 |

### エンコード・デコード

| ノード | 機能 |
|--------|------|
| **VAE Encode** | 画像を潜在表現に変換 |
| **VAE Decode** | 潜在表現を画像に変換 |
| **CheckPoint Loader** | モデルを読み込む |

### 高度な機能

| ノード | 機能 |
|--------|------|
| **LoRA Loader** | LoRA アダプタを読み込む |
| **ControlNet** | 構図制御を適用 |
| **Upscale Image** | 画像を拡大 |
| **Face Restore** | 顔を修復 |

## ワークフロー保存・読み込み

### ワークフローを保存

```
1. UI 右上の「Save」ボタンをクリック
2. JSON ファイルとして保存される
3. ファイル名は自動生成（例：workflow_12345.json）
```

### ワークフローを読み込み

```
1. UI 右上の「Load」ボタンをクリック
2. 保存されたワークフロー JSON を選択
3. 自動的にノードが配置される
```

### ワークフロー共有

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "a beautiful landscape",
      "clip": [1, 1]
    }
  }
  // ... 以降のノード定義
}
```

## カスタムノード・拡張機能

### カスタムノードのインストール

```bash
# Manager ノードをインストール（推奨）
# ComfyUI Manager: https://github.com/ltdrdata/ComfyUI-Manager

# ディレクトリを作成
mkdir custom_nodes
cd custom_nodes

# ノードをクローン
git clone https://github.com/[author]/[node-name]

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 人気のカスタムノード

| ノード名 | 機能 |
|---------|------|
| **ComfyUI Manager** | ノード・モデル管理 |
| **Roop** | 顔交換 |
| **OpenPose** | 人物ポーズ検出 |
| **GFPGAN** | 顔修復 |
| **Frame Interpolation** | フレーム補間 |

## API からの制御

### Python からワークフロー実行

```python
import requests
import json
from PIL import Image
import io

# ComfyUI サーバーのURL
SERVER_URL = "http://127.0.0.1:8188"

# ワークフロー JSON を定義
workflow = {
    "1": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}
    },
    "2": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "text": "a beautiful landscape",
            "clip": ["1", 1]
        }
    },
    "3": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "text": "ugly, deformed",
            "clip": ["1", 1]
        }
    },
    "4": {
        "class_type": "KSampler",
        "inputs": {
            "seed": 12345,
            "steps": 20,
            "cfg": 7.0,
            "sampler_name": "dpmpp_2m",
            "scheduler": "karras",
            "denoise": 1.0,
            "model": ["1", 0],
            "positive": ["2", 0],
            "negative": ["3", 0],
            "latent_image": ["5", 0]
        }
    },
    "5": {
        "class_type": "EmptyLatentImage",
        "inputs": {
            "width": 512,
            "height": 512,
            "batch_size": 1
        }
    },
    "6": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": ["4", 0],
            "vae": ["1", 2]
        }
    },
    "7": {
        "class_type": "SaveImage",
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": ["6", 0]
        }
    }
}

# ワークフロー実行
def execute_workflow(workflow):
    data = json.dumps(workflow).encode('utf-8')
    
    req = requests.post(
        f"{SERVER_URL}/prompt",
        data=data
    )
    
    return req.json()

# 実行
result = execute_workflow(workflow)
print(f"Job queued: {result['prompt_id']}")
```

### cURL コマンドでの実行

```bash
curl -X POST http://localhost:8188/prompt \
  -H "Content-Type: application/json" \
  -d @workflow.json
```

## トラブルシューティング

### よくあるエラーと解決方法

#### 1. "CUDA out of memory"

```
原因：GPU メモリ不足

解決：
1. モデルのサイズを小さくする
   → Stable Diffusion 1.5 を使用
2. 画像サイズを減らす
   → 512×512 から開始
3. ステップ数を減らす
   → 20 ステップから開始
4. VAE Tiling を使用
   → Enable VAE Tiling オプションを有効化
```

#### 2. "Model not found"

```
原因：モデルファイルがダウンロードされていない

解決：
1. models/checkpoints/ ディレクトリを確認
2. Hugging Face からモデルをダウンロード
   → https://huggingface.co/runwayml/stable-diffusion-v1-5
3. .safetensors ファイルを配置
```

#### 3. "No GPU detected"

```
原因：GPU ドライバが認識されていない

解決：
1. GPU ドライバを更新
2. CUDA ツールキットをインストール
3. PyTorch で GPU が認識されているか確認
   → python -c "import torch; print(torch.cuda.is_available())"
4. CPU モードで実行
   → python main.py --cpu
```

#### 4. ポート 8188 がすでに使用されている

```
原因：別のアプリが同じポートを使用

解決：
python main.py --port 8189
# 別のポートで起動
```

## パフォーマンス最適化

### 高速化のコツ

#### 1. モデル最適化

```
✅ LCM モデルを使用（高速）
✅ SDXL Turbo を使用（3-4ステップで生成）
✅ LoRA を組み合わせ（軽量）
```

#### 2. メモリ最適化

```
✅ VAE Tiling を有効化
✅ 不要なモデルをアンロード
✅ Batch Size を調整（1 推奨）
```

#### 3. ステップ数の調整

```
生成品質 vs 速度のバランス

品質重視：30-50 ステップ
バランス型：20-30 ステップ
高速重視：10-15 ステップ
```

## ベストプラクティス

### プロンプト作成

```
✅ 具体的な説明を追加
   例：「a beautiful landscape」→ 「a beautiful mountain landscape with snow, sunset, detailed, 4k, professional photography」

✅ スタイルを指定
   例：「oil painting」「digital art」「3D render」

✅ ネガティブプロンプトを活用
   例：「ugly, deformed, blurry, low quality」
```

### ワークフロー設計

```
✅ モジュール化：再利用可能なノード構成
✅ 段階的テスト：一部ノードから実行
✅ ワークフロー保存：成功したワークフローは保存
✅ コメント追加：複雑なワークフローにはコメント
```

### リソース管理

```
✅ 大きなモデルは必要な時だけ読み込む
✅ VRAM 監視：nvidia-smi で確認
✅ 定期的に キャッシュをクリア
```

## まとめ

ComfyUI は、Stable Diffusion の強力な機能を直感的に活用できるツールです。ノードベースのインターフェースにより、複雑な画像生成パイプラインも視覚的に構築でき、初心者からプロフェッショナルまで幅広いユーザーに対応します。

**重要なポイント：**
- 完全無料・オープンソース
- GPU による高速処理
- 拡張性が高い（カスタムノード対応）
- コミュニティが活発
- API での自動化も可能

ComfyUI を使いこなすことで、AI 画像生成の可能性を最大限に引き出すことができます。

## リソース

- [ComfyUI 公式 GitHub](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)
- [ComfyUI コミュニティ](https://github.com/comfyanonymous/ComfyUI/discussions)
- [Hugging Face Models](https://huggingface.co/models)
