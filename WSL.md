# WSL - Windows Subsystem for Linux

Windows 上で Linux 環境を実行するための互換性レイヤー

## WSL とは

WSL（Windows Subsystem for Linux）は、Windows 10 および Windows 11 上で Linux ベースの環境を実行するための互換性レイヤーです。このシステムを使うことで、Windows ユーザーは Linux のコマンドラインツール、ユーティリティ、アプリケーションを直接実行することができます。これにより、開発者は Windows 環境内で直接 Linux プログラムを使って作業ができるため、クロスプラットフォームのアプリケーション開発が容易になります。

### WSL の主な特徴

#### 1. フル Linux カーネルの統合

WSL 2 では、完全な Linux カーネルが Windows 内に統合されており、パフォーマンスが大幅に向上しています。これにより、ファイルシステムのパフォーマンスが向上し、より多くの Linux アプリケーションが互換性を持って実行されます。

**パフォーマンス比較：**

```
WSL 1：
└─ Windows のシステムコールを変換（低速）

WSL 2：
└─ 完全な Linux カーネル搭載（高速）
└─ ファイルアクセス：~20倍高速化
└─ コンパイル時間：~2-3倍高速化
```

#### 2. Windows と Linux 間のシームレスな操作

WSL を使用すると、Windows アプリケーションと Linux コマンドラインツールを同時に使用できます。例えば、Windows のファイル エクスプローラーから Linux ファイルシステムにアクセスしたり、Visual Studio Code のようなエディタで Linux 上で動作するアプリケーションを編集できます。

```
統合の例：

Windows ファイルエクスプーラー
         ↕
  Linux ファイルシステム
         ↕
Visual Studio Code（Windows）で編集
         ↕
WSL 内の Linux コンパイラで実行
```

#### 3. 開発環境の向上

WSL は、特に Web 開発、システム管理、科学研究など、さまざまな開発タスクにおいて、強力なツールを提供します。Linux 環境が必要な開発ワークフローにとって、Windows 上で直接それらを利用できるのは大きな利点です。

**対応する開発領域：**

```
Web 開発：
├─ Node.js、Python、Ruby
├─ Apache、Nginx
└─ Docker コンテナ

データサイエンス：
├─ Python（NumPy、Pandas、Scikit-learn）
├─ R 言語
└─ Jupyter Notebook

システム管理：
├─ Bash スクリプト
├─ grep、sed、awk などのテキスト処理
└─ cron による定期実行
```

#### 4. 簡単なセットアップ

Microsoft Store から Linux ディストリビューションをダウンロードし、数ステップでセットアップすることができます。これにより、ユーザーは複雑なデュアルブート環境を設定することなく、すぐに Linux を使用開始できます。

## WSL のインストール

### 前提条件

**Windows 10/11 の要件：**

```
Windows 10：
└─ バージョン 2004 以降（Build 19041 以上）

Windows 11：
└─ すべてのバージョン対応

メモリ：
└─ 最低 4GB（推奨 8GB 以上）

ディスク容量：
└─ ディストリビューションあたり 5～20GB 程度
```

**仮想化の有効化：**

```
BIOS で仮想化機能を有効化
├─ Intel VT-x（Intel CPU）
└─ AMD-V（AMD CPU）
```

### Step 1: WSL 2 を有効化

**Windows PowerShell を管理者権限で開く：**

```powershell
# WSL を有効化
wsl --install

# または、個別に有効化
wsl --install --no-distribution

# WSL 2 をデフォルトに設定
wsl --set-default-version 2
```

**実行結果：**

```
インストールが完了します
必要に応じて再起動が促される
```

### Step 2: Linux ディストリビューションをインストール

**Microsoft Store から直接インストール：**

```
Windows キー → 「Microsoft Store」を開く
  ↓
「WSL」または「Linux」で検索
  ↓
以下から選択：
├─ Ubuntu（最も一般的）
├─ Debian
├─ Fedora
├─ openSUSE
├─ Kali Linux
└─ その他
  ↓
「インストール」をクリック
  ↓
「起動」をクリック
```

**コマンドラインからインストール：**

```powershell
# インストール可能なディストリビューション一覧を表示
wsl --list --online

# Ubuntu をインストール
wsl --install -d Ubuntu

# Debian をインストール
wsl --install -d Debian

# Fedora をインストール
wsl --install -d Fedora
```

### Step 3: ユーザアカウントの設定

WSL が初回起動時に以下を促します：

```
Enter new UNIX username: your_username
Enter new UNIX password: ***
Retype new UNIX password: ***
```

**入力内容：**

```
ユーザー名：
├─ 小文字英数字（スペース、特殊文字不可）
├─ 例：developer、user123

パスワード：
├─ 任意の複雑度で設定可能
├─ 入力時は表示されない
└─ sudo コマンド実行時に必要
```

### Step 4: パッケージマネージャーを更新

```bash
# Ubuntu/Debian の場合
sudo apt update
sudo apt upgrade -y

# Fedora の場合
sudo dnf update -y
sudo dnf upgrade -y
```

**完了！** WSL が使用可能になります

## WSL の使い方

### WSL ターミナルを開く

**Windows 11 ターミナルから：**

```powershell
# 新しい WSL タブを開く
wsl
```

**PowerShell から：**

```powershell
# WSL を起動
wsl

# 特定のディストリビューションを起動
wsl -d Ubuntu
```

**Bash から直接コマンド実行：**

```powershell
wsl echo "Hello from Linux"
wsl uname -a
```

### ファイルシステムにアクセス

**WSL から Windows ファイルにアクセス：**

```bash
# Windows ドライブは /mnt/c 以下にマウントされる
cd /mnt/c/Users/YourName/Documents

# ファイルを一覧表示
ls -la

# ファイルを編集
nano sample.txt
```

**Windows から WSL ファイルにアクセス：**

```powershell
# WSL のファイルシステムを開く
explorer.exe \\wsl$\Ubuntu\home\username\

# または、ファイルエクスプローラーの「ネットワーク」から直接アクセス
# \\wsl$\Ubuntu\home\username
```

### WSL 上でアプリケーションを実行

**Node.js のインストール：**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
node --version
npm --version
```

**Python のインストール：**

```bash
sudo apt install -y python3 python3-pip
python3 --version
pip3 --version
```

**Git のインストール：**

```bash
sudo apt install -y git
git --version
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

**Docker のインストール：**

```bash
# WSL 2 での Docker Desktop 連携は別途設定が必要
# Docker Desktop を Windows にインストールし、
# WSL 2 統合を有効化する
```

## Visual Studio Code との統合

### WSL Extension をインストール

```
VS Code を開く
  ↓
拡張機能マーケットプレイス（Ctrl+Shift+X）
  ↓
「WSL」または「Remote - WSL」を検索
  ↓
Microsoft Official の「Remote - WSL」をインストール
```

### VS Code から WSL を開く

**方法1：コマンドから：**

```bash
# WSL ターミナル内で実行
cd ~/my-project
code .
```

**方法2：VS Code から：**

```
左下のアイコン（><）をクリック
  ↓
「WSL に再度開く」を選択
  ↓
VS Code が WSL 統合モードで再起動
  ↓
左下に「WSL: Ubuntu」と表示される
```

**メリット：**

```
✅ VS Code エディタ：Windows 上で動作
✅ コンパイラ・インタプリタ：WSL 上で動作
✅ ターミナル：統合ターミナルで Linux コマンド実行
✅ 拡張機能：WSL 環境を認識
```

## WSL の便利な設定

### .wslconfig ファイル（WSL 2 全体の設定）

**ファイル場所：** `C:\Users\YourName\.wslconfig`

```ini
[wsl2]
# メモリ上限を設定（GB単位）
memory=4GB

# CPU コア数を設定
processors=4

# スワップメモリ（GB単位）
swap=2GB

# ネットワークバッファサイズ
pageReporting=true

# ローカルホストの ipv6 アドレス解決
ipv6=true
```

### wsl.conf ファイル（個別ディストリビューション設定）

**ファイル場所：** `/etc/wsl.conf`（WSL 内）

```ini
[interop]
# Windows exe をパスから実行するか
enabled=true

# Windows exe の拡張子チェック
appendWindowsPath=true

[user]
# デフォルトユーザー
default=username

[boot]
# WSL 起動時のコマンド
command=/usr/bin/bash -c ""
```

## WSL コマンドリファレンス

| コマンド | 説明 |
|---------|------|
| `wsl` | WSL を起動 |
| `wsl -d Ubuntu` | 特定のディストリビューションを起動 |
| `wsl --list` | インストール済みディストリビューション一覧 |
| `wsl --list --online` | インストール可能なディストリビューション一覧 |
| `wsl --install -d Debian` | Debian をインストール |
| `wsl --unregister Ubuntu` | Ubuntu をアンインストール |
| `wsl --shutdown` | すべての WSL インスタンスを終了 |
| `wsl --set-default Ubuntu` | デフォルトディストリビューションを設定 |
| `wsl --set-version Ubuntu 2` | WSL 1 → WSL 2 に変更 |

## 実践的な使用例

### 例1：Web 開発環境の構築

```bash
# WSL ターミナル内で実行
sudo apt update
sudo apt install -y nodejs npm

# Express プロジェクトを作成
npx express-generator my-app
cd my-app
npm install

# サーバー起動
npm start

# Windows のブラウザから http://localhost:3000 にアクセス
```

### 例2：Python データ分析環境

```bash
# Python と必要なパッケージをインストール
sudo apt install -y python3 python3-pip
pip3 install numpy pandas scikit-learn matplotlib

# Jupyter Notebook をインストール
pip3 install jupyter

# Jupyter を起動
jupyter notebook
# http://localhost:8888 で Web インタフェースが起動
```

### 例3：Docker で開発環境を統合

```bash
# Docker Desktop をインストール（Windows）
# 設定で WSL 2 統合を有効化

# WSL ターミナルから Docker を使用
docker --version

# Docker コンテナを実行
docker run -it ubuntu:20.04 /bin/bash
```

### 例4：Bash スクリプトの自動化

```bash
# backup.sh という自動バックアップスクリプトを作成
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/mnt/c/Backups"
SOURCE_DIR="/mnt/c/Users/YourName/Documents"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/backup-$(date +%Y%m%d).tar.gz $SOURCE_DIR

echo "バックアップ完了"
EOF

chmod +x backup.sh
./backup.sh
```

## パフォーマンス最適化

### WSL ファイルシステムでのパフォーマンス

```
✅ 高速：WSL 内のファイルシステムで作業
└─ /home/username/projects

❌ 低速：Windows ファイルシステムで作業
└─ /mnt/c/Users/...

推奨：
└─ WSL 内の home ディレクトリでプロジェクト管理
└─ データの永続化が必要な場合のみ /mnt/c を使用
```

### メモリ/CPU 最適化

```bash
# 現在のメモリ使用量を確認
free -h

# CPU 使用率を確認
top

# .wslconfig で制限を設定
# C:\Users\YourName\.wslconfig
# [wsl2]
# memory=4GB
# processors=4
```

## トラブルシューティング

### 問題1：「仮想化が有効になっていない」

**解決方法：**

```
1. BIOS 設定を確認
   ├─ 再起動時に F2、F10、Del キー押下
   ├─ Virtualization、VT-x、AMD-V を有効化

2. Hyper-V が有効か確認
   ├─ Windows の機能を有効化
   ├─ 「Hyper-V」にチェック

3. 再起動
   powershell.exe
   Restart-Computer
```

### 問題2：「WSL インストール後に起動しない」

**解決方法：**

```bash
# WSL のカーネルを更新
wsl --update

# Linux ディストリビューションをリセット
wsl --unregister Ubuntu
wsl --install -d Ubuntu

# WSL サービスを再起動
# PowerShell（管理者）で実行
net stop LxssManager
net start LxssManager
```

### 問題3：「Windows ファイルシステムの書き込みが遅い」

**解決方法：**

```bash
# WSL 内のホームディレクトリで作業
cd ~
mkdir projects
cd projects

# または、.wslconfig で設定変更
# [interop]
# appendWindowsPath=true
```

### 問題4：「ディスク容量が足りない」

**解決方法：**

```bash
# WSL のディスク使用量を確認
du -sh ~/*

# 不要なファイルを削除
rm -rf ~/Downloads/*

# または、仮想ディスクをリサイズ
# PowerShell で実行：
# diskpart
# > select vdisk file="C:\Users\YourName\AppData\Local\Packages\...\ext4.vhdx"
# > expand vdisk maximum=100000  # 100GB に拡張
```

## WSL 1 vs WSL 2 比較

| 項目 | WSL 1 | WSL 2 |
|------|-------|-------|
| **パフォーマンス** | 低～中 | 高速 |
| **ファイル操作** | 低速 | 高速（~20倍） |
| **メモリ効率** | 優秀 | 中程度 |
| **Docker サポート** | なし | あり（ネイティブ） |
| **Linux カーネル** | 互換性レイヤー | 完全なカーネル |
| **推奨用途** | 軽量作業 | Web開発、Docker |

**結論：** ほぼすべてのユースケースで WSL 2 が推奨されます

## ベストプラクティス

```
✅ 推奨される使い方

① WSL 内のホームディレクトリで作業
   └─ /home/username/projects

② VS Code Remote - WSL で開発
   └─ エディタと実行環境が統合される

③ Git を WSL 内で設定
   └─ git config --global user.name "..."

④ .wslconfig でリソースを適切に設定
   └─ メモリ、CPU を制限して安定化

⑤ 定期的にアップデート
   └─ wsl --update で最新カーネル

❌ 避けるべき方法

① Windows ファイルシステムでの全面作業
   └─ パフォーマンスが低下

② ディストリビューション設定なしでの使用
   └─ 予期しない動作が発生

③ 複数ディストリビューションの無分別インストール
   └─ ディスク容量を圧迫

④ セキュリティアップデートの放置
   └─ 脆弱性が放置される
```

## WSL 導入の効果

```
開発効率の向上：
├─ Windows でのデスクトップ作業
├─ Linux ツール・言語の直接利用
└─ クロスプラットフォーム開発が容易

総合的なメリット：
├─ デュアルブート不要
├─ 仮想マシンより軽量
├─ 学習曲線が低い
└─ オープンソースツール活用が容易
```

## 関連トピック

- [[Linux]]：Linux 基本知識
- [[CommandLine]]：コマンドラインツール
- [[Docker]]：コンテナ化技術
- [[DeveloperTools]]：開発者向けツール
