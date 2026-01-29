# Bluetooth - 近距離無線通信技術

スマートフォン、IoTデバイス、ウェアラブル間の無線通信実装ガイド

## Bluetooth とは

Bluetoothは、近距離のデバイス間で無線通信を行うための技術です。1990年代に開発され、現在ではスマートフォン、タブレット、イヤホン、パソコン、ウェアラブルデバイスなど多くのデバイスで利用されています。通信範囲は一般的に10メートル程度で、低消費電力で安定した接続が特徴です。

### Bluetooth の活用場面

```
✅ Bluetooth が活躍する領域

├─ ワイヤレスイヤホン・ヘッドセット
├─ スマートウォッチ・フィットネストラッカー
├─ スマートホーム・家電制御
├─ ゲームコントローラー
├─ ワイヤレスマウス・キーボード
├─ 医療機器（心拍計など）
├─ IoT センサーデバイス
└─ 自動車ハンズフリー通話
```

## Bluetooth の基本構造

Bluetoothは、主に**マスターデバイス**と**スレーブデバイス**に分かれて通信を行います。マスターが通信を制御し、スレーブがその指示に従ってデータを送受信します。これにより、接続デバイスの役割を明確にすることができます。

```
通信構造：

マスターデバイス
（スマートフォンなど）
    ↕
スレーブデバイス
（ウェアラブルなど）

役割分担：
├─ マスター：通信を開始・制御
└─ スレーブ：マスターの指示に従う
```

### Bluetooth の主要なプロトコル

#### 1. L2CAP（Logical Link Control and Adaptation Protocol）

データの転送を管理し、パケットの再送やエラー処理を行う役割があります。

```
機能：
├─ パケット管理
├─ エラー処理
├─ フロー制御
└─ マルチプレックス
```

#### 2. RFCOMM（Radio Frequency Communication）

シリアル通信の代わりとして使用され、Bluetoothでの仮想シリアルポートを提供します。

```
用途：
├─ シリアル通信の仮想化
├─ 従来のシリアルアプリケーション対応
└─ Point-to-Point 通信
```

#### 3. SDP（Service Discovery Protocol）

デバイスがどのサービスを提供しているかを発見するプロトコルです。

```
機能：
├─ サービス検索
├─ デバイス情報取得
├─ 利用可能なプロファイル確認
└─ ポート情報の取得
```

## Bluetooth のバージョン

Bluetoothはバージョンごとに異なる機能や性能が追加されています。

### バージョン比較

| バージョン | 年 | 主な機能 | データ速度 | 消費電力 |
|-----------|-----|---------|-----------|---------|
| **2.0 + EDR** | 2004 | EDR対応 | 3 Mbps | 中程度 |
| **3.0 + HS** | 2009 | 高速化 | 24 Mbps | 中程度 |
| **4.0 (BLE)** | 2010 | BLE追加 | 1 Mbps | 低（BLE） |
| **4.1** | 2013 | 改善 | 1 Mbps | 低 |
| **4.2** | 2014 | セキュリティ強化 | 1 Mbps | 低 |
| **5.0** | 2016 | 大幅改善 | 2 Mbps | 低 |
| **5.1** | 2019 | 方向検出 | 2 Mbps | 低 |
| **5.2** | 2020 | 同期化向上 | 2 Mbps | 低 |
| **5.3** | 2021 | 干渉対策 | 2 Mbps | 低 |

### Bluetooth 2.0 + EDR

```
特徴：
├─ EDR（Enhanced Data Rate）によるデータ転送速度向上
├─ 最大転送速度：3 Mbps
├─ 消費電力：中程度
└─ 用途：音声・ストリーミング
```

### Bluetooth 4.0 - BLE 導入

```
革新：
├─ BLE（Bluetooth Low Energy）の追加
├─ 従来比 100 倍の省電力化
├─ IoT デバイスに最適
└─ 長時間動作が可能
```

### Bluetooth 5.0

```
改善点：
├─ 通信範囲：最大 4 倍
├─ データ転送速度：2 倍
├─ Mesh ネットワーク対応
└─ 接続デバイス数の拡大
```

## BLE（Bluetooth Low Energy）

BLEはBluetooth 4.0で導入された低消費電力モードで、主にIoTデバイスやウェアラブルデバイスで使用されます。短時間で少量のデータを送受信する用途に最適で、長時間の稼働が求められるデバイスでよく利用されます。

### BLE の特徴

```
✅ BLE の利点

├─ 消費電力が非常に低い
│  └─ 単4電池で数ヶ月～数年稼働可能
│
├─ セットアップが簡単
│  └─ ペアリング不要な場合もある
│
├─ 素早い接続
│  └─ 数ミリ秒で接続確立
│
├─ 小さなデータ送信に最適
│  └─ センサーデータ
│
├─ 範囲内で複数接続
│  └─ 1個のセントラルに複数ペリフェラル

❌ BLE の制限

└─ データ転送速度が低い
   └─ 最大 1-2 Mbps
```

### BLE の通信スタック

```
BLE 通信構造：

────────────────────────────────────
│ GATT / ATT 層
│ (Generic Attribute Profile)
├─ Service（サービス）
├─ Characteristic（キャラクタリスティック）
└─ Descriptor（ディスクリプタ）
────────────────────────────────────
│ GAP 層
│ (Generic Access Profile)
├─ アドバタイズ
├─ スキャン
└─ 接続
────────────────────────────────────
│ L2CAP
│ (Logical Link Control and Adaptation)
────────────────────────────────────
│ HCI（Host Controller Interface）
────────────────────────────────────
│ Bluetooth コントローラ
────────────────────────────────────
```

## Bluetooth 機能の実装手順

Bluetooth機能を実装するための一般的な流れです。

### 1. Bluetooth アダプタの準備

Bluetoothを使用するには、まずデバイスにBluetoothアダプタが必要です。多くのスマートフォンやコンピュータには内蔵されていますが、外部アダプタも存在します。

```
デバイス別の確認：

スマートフォン：
└─ 内蔵 Bluetooth 搭載（現代のほぼ全機種）

パソコン：
├─ 内蔵（最近のノート PC）
└─ USB 外部アダプタ（デスクトップなど）

ラズベリーパイ：
├─ Pi 3 以降は内蔵
└─ Pi Zero/Pi 1/2 は USB アダプタ必要
```

### 2. デバイスのペアリング

通信を行う前に、2つのデバイスをペアリングする必要があります。ペアリングとは、一度認識したデバイス同士がその後も接続を許可するためのプロセスです。

```
ペアリングの流れ：

1. デバイス A：スキャン開始
   ↓
2. デバイス B：アドバタイズ開始
   ↓
3. デバイス A：デバイス B を発見
   ↓
4. デバイス A：ペアリング要求
   ↓
5. デバイス B：ペアリング受け入れ
   ↓
6. PINコード/パスキー交換
   ↓
7. 認証・暗号化鍵生成
   ↓
8. ペアリング完了（再接続時は簡略化）
```

### 3. サービスの発見

Bluetoothデバイスは特定のサービスを提供しており、通信前にそれを発見する必要があります。SDPを使って、どのサービスが利用可能かを確認します。

```
BLE でのサービス構造：

────────────────────────────────────
│ Service（サービス）
│ UUID: 180A（Device Information）
├─ Characteristic
│  UUID: 2A29（Manufacturer Name）
│  Value: "Raspberry Pi"
│
├─ Characteristic
│  UUID: 2A24（Model Number）
│  Value: "RPi 3B+"
│
└─ Characteristic
   UUID: 2A27（Hardware Version）
   Value: "1.0"
────────────────────────────────────
```

### 4. データ通信

ペアリングが完了し、必要なサービスが見つかったら、データの送受信が可能になります。多くのデバイスでは、シリアル通信プロトコル（RFCOMM）を利用してデータを送信します。

## ラズベリーパイと Unity 間の BLE データ通信

### 概要

この手順では、ラズベリーパイとUnityアプリケーション間でBluetooth Low Energy（BLE）を使用してデータを送受信する方法を解説します。

### 必要な環境

```
ハードウェア：
├─ Raspberry Pi 3 以降（BLE 対応）
├─ Bluetooth LE プラグイン対応スマートフォン
└─ USB Bluetooth アダプタ（古い機種の場合）

ソフトウェア：
├─ Raspberry Pi OS
├─ Python 3.x
├─ Unity 2020 以降
├─ Bluetooth LE プラグイン（Unity）
└─ bluepy/bleak（Python）
```

## ラズベリーパイのセットアップ

### Step 1：OS のインストールと BLE の準備

```bash
# システムの更新
sudo apt update
sudo apt upgrade -y

# Bluetooth サービスの有効化
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# Bluetooth デーモンの確認
sudo systemctl status bluetooth
```

### Step 2：Bluetooth デバイスのスキャンとペアリング

```bash
# bluetoothctl ツールの起動
bluetoothctl

# 以下のコマンドを順に実行
[bluetooth]# power on
[bluetooth]# scan on

# デバイスを見つけた後（例：00:1A:7D:DA:71:13）
[bluetooth]# pair 00:1A:7D:DA:71:13
[bluetooth]# trust 00:1A:7D:DA:71:13
[bluetooth]# connect 00:1A:7D:DA:71:13

# 接続確認
[bluetooth]# info 00:1A:7D:DA:71:13
[bluetooth]# exit
```

### Step 3：BLE Python ライブラリのインストール

```bash
# パッケージマネージャーのインストール
sudo apt-get install python3-pip

# bleak（推奨）のインストール
pip3 install bleak

# または bluepy（古い方法）
pip3 install bluepy
```

### Step 4：BLE データ送信プログラム

**温度センサーデータを BLE で送信する例：**

```python
#!/usr/bin/env python3

import asyncio
from bleak import BleakServer
import uuid
from datetime import datetime

# サービス・キャラクタリスティック UUID の定義
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "87654321-4321-8765-4321-0fedcba98765"

# グローバル値
current_value = bytearray([0])

async def handle_read_request(char_uuid):
    """読み取りリクエストを処理"""
    return current_value

async def main():
    """BLE サーバーの実行"""
    
    # サービスとキャラクタリスティックの定義
    characteristics = {
        CHAR_UUID: {
            "read": handle_read_request,
            "write": lambda data: update_value(data)
        }
    }
    
    # BLE サーバーを起動
    async with BleakServer([SERVICE_UUID], characteristics):
        print("BLE サーバーが起動しました...")
        print(f"Service UUID: {SERVICE_UUID}")
        print(f"Characteristic UUID: {CHAR_UUID}")
        
        # 温度データをシミュレート
        while True:
            import random
            temperature = round(20 + random.uniform(-5, 5), 1)
            current_value = str(temperature).encode()
            
            print(f"[{datetime.now()}] 温度: {temperature}°C")
            await asyncio.sleep(5)

def update_value(data):
    """書き込みデータを処理"""
    print(f"データ受信: {data}")

if __name__ == "__main__":
    asyncio.run(main())
```

**実行方法：**

```bash
chmod +x ble_server.py
python3 ble_server.py
```

## Unity アプリケーションのセットアップ

### Step 1：BLE プラグインの導入

```
Unity Asset Store から以下をインストール：

1. 「Bluetooth LE for iOS and Android」
   または
2. 「BLE Mobile」
   または
3. その他の BLE プラグイン

インストール後：
├─ Assets/Plugins/ に配置される
└─ スクリプトから BleutoothLEHardwareInterface でアクセス
```

### Step 2：BLE 接続スクリプト（C#）

```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;

public class BLEManager : MonoBehaviour
{
    [SerializeField] private Text dataDisplayText;
    [SerializeField] private Text statusText;
    
    private string deviceAddress = "";
    private string serviceUUID = "12345678-1234-5678-1234-56789abcdef0";
    private string characteristicUUID = "87654321-4321-8765-4321-0fedcba98765";
    private bool isScanning = false;
    private bool isConnected = false;

    void Start()
    {
        Initialize();
    }

    void Initialize()
    {
        // Bluetooth LE の初期化
        BluetoothLEHardwareInterface.Initialize(true, false, () =>
        {
            Debug.Log("Bluetooth LE initialized");
            statusText.text = "初期化完了";
        }, (error) =>
        {
            Debug.LogError("BLE Initialization failed: " + error);
            statusText.text = "初期化失敗: " + error;
        });
    }

    public void StartScan()
    {
        if (isScanning) return;
        
        isScanning = true;
        statusText.text = "スキャン中...";
        
        // BLE デバイスをスキャン
        BluetoothLEHardwareInterface.ScanForPeripheralsWithServices(
            null, // すべてのサービスをスキャン
            (address, name) =>
            {
                // デバイス発見時の処理
                if (!string.IsNullOrEmpty(name) && name.Contains("Raspberry"))
                {
                    Debug.Log($"Found device: {name} ({address})");
                    deviceAddress = address;
                    BluetoothLEHardwareInterface.StopScan();
                    isScanning = false;
                    statusText.text = "デバイス発見: " + name;
                    
                    // 接続開始
                    ConnectToDevice(address);
                }
            },
            null
        );
        
        // 10秒後にスキャン終了（デバイス未発見の場合）
        Invoke(nameof(StopScan), 10f);
    }

    void StopScan()
    {
        if (isScanning)
        {
            BluetoothLEHardwareInterface.StopScan();
            isScanning = false;
            statusText.text = "スキャン停止（デバイス未発見）";
        }
    }

    void ConnectToDevice(string address)
    {
        statusText.text = "接続中...";
        
        BluetoothLEHardwareInterface.ConnectToPeripheral(
            address,
            (address2) =>
            {
                // 接続成功時
                Debug.Log("Connected to: " + address2);
                isConnected = true;
                statusText.text = "接続成功";
                StartCoroutine(ReceiveData(address2));
            },
            (address2, serviceUUID2) =>
            {
                // サービス発見時
                Debug.Log("Discovered service: " + serviceUUID2);
            },
            (address2, serviceUUID2, characteristicUUID2) =>
            {
                // キャラクタリスティック発見時
                Debug.Log("Discovered characteristic: " + characteristicUUID2);
            },
            (address2) =>
            {
                // 接続失敗時
                Debug.LogError("Failed to connect to: " + address2);
                statusText.text = "接続失敗";
            }
        );
    }

    IEnumerator ReceiveData(string address)
    {
        while (isConnected)
        {
            // キャラクタリスティックを読み取り
            BluetoothLEHardwareInterface.ReadCharacteristic(
                address,
                serviceUUID,
                characteristicUUID,
                (characteristic) =>
                {
                    // データ受信時の処理
                    string receivedData = System.Text.Encoding.UTF8.GetString(characteristic);
                    dataDisplayText.text = "受信データ: " + receivedData;
                    Debug.Log("Received: " + receivedData);
                }
            );
            
            yield return new WaitForSeconds(2);
        }
    }

    public void SendData(string data)
    {
        if (!isConnected || string.IsNullOrEmpty(deviceAddress))
        {
            statusText.text = "デバイスに接続していません";
            return;
        }

        byte[] byteData = System.Text.Encoding.UTF8.GetBytes(data);
        
        BluetoothLEHardwareInterface.WriteCharacteristic(
            deviceAddress,
            serviceUUID,
            characteristicUUID,
            byteData,
            byteData.Length,
            true,
            (success) =>
            {
                if (success)
                {
                    Debug.Log("Data sent successfully");
                    statusText.text = "送信完了: " + data;
                }
                else
                {
                    Debug.LogError("Failed to send data");
                    statusText.text = "送信失敗";
                }
            }
        );
    }

    public void Disconnect()
    {
        if (isConnected)
        {
            BluetoothLEHardwareInterface.DisconnectPeripheral(
                deviceAddress,
                (address) =>
                {
                    isConnected = false;
                    statusText.text = "接続切断";
                    Debug.Log("Disconnected from: " + address);
                }
            );
        }
    }
}
```

### Step 3：UI の構成

**Canvas に以下の要素を配置：**

```
┌─────────────────────────────────┐
│ Bluetooth BLE データ受信         │
├─────────────────────────────────┤
│ 状態: [statusText]              │
│ データ: [dataDisplayText]        │
├─────────────────────────────────┤
│ [スキャン開始] [接続]           │
│ [データ送信]   [切断]           │
└─────────────────────────────────┘
```

## iOS 向けのビルド設定

### Info.plist への権限追加

```xml
<!-- Bluetooth 常時利用権限 -->
<key>NSBluetoothAlwaysUsageDescription</key>
<string>このアプリケーションはBluetoothデバイスと通信するために使用します。</string>

<!-- バックグラウンド Bluetooth 権限 -->
<key>NSBluetoothPeripheralUsageDescription</key>
<string>Bluetoothでデバイスと通信するために必要です。</string>

<!-- バックグラウンドモード -->
<key>UIBackgroundModes</key>
<array>
    <string>bluetooth-central</string>
    <string>bluetooth-peripheral</string>
</array>
```

### Xcode での設定

```
Build Phases → Link Binary With Libraries:
├─ CoreBluetooth.framework を追加
└─ Foundation.framework を確認
```

## Android 向けのビルド設定

### AndroidManifest.xml への権限追加

```xml
<!-- Bluetooth 基本権限 -->
<uses-permission android:name="android.permission.BLUETOOTH"/>
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>

<!-- Android 12+ での新規権限 -->
<uses-permission android:name="android.permission.BLUETOOTH_SCAN"/>
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT"/>

<!-- 位置情報権限（BLE スキャンに必須） -->
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
```

### ランタイム権限の要求（C#）

```csharp
#if UNITY_ANDROID
using UnityEngine.Android;

void RequestPermissions()
{
    if (!Permission.HasUserAuthorizedPermission("android.permission.ACCESS_FINE_LOCATION"))
    {
        Permission.RequestUserPermission("android.permission.ACCESS_FINE_LOCATION");
    }
    
    if (!Permission.HasUserAuthorizedPermission("android.permission.BLUETOOTH_SCAN"))
    {
        Permission.RequestUserPermission("android.permission.BLUETOOTH_SCAN");
    }
    
    if (!Permission.HasUserAuthorizedPermission("android.permission.BLUETOOTH_CONNECT"))
    {
        Permission.RequestUserPermission("android.permission.BLUETOOTH_CONNECT");
    }
}
#endif
```

## トラブルシューティング

### ラズベリーパイ側の問題

```
問題 1：Bluetooth サービスが起動しない
└─ 解決：sudo systemctl start bluetooth

問題 2：デバイスが発見されない
└─ 解決：bluetoothctl で power on、scan on を確認

問題 3：ペアリングに失敗
└─ 解決：PIN コード入力を確認、再度 pair を実行
```

### Unity 側の問題

```
問題 1：プラグインが認識されない
└─ 解決：Asset Store から再インストール

問題 2：接続できない
└─ 解決：UUID が正しいか確認、デバイス発見まで待つ

問題 3：Android でスキャンが開始されない
└─ 解決：位置情報権限を要求・許可
```

## Bluetooth セキュリティ対策

```
✅ セキュリティベストプラクティス

① 認証と暗号化
  └─ ペアリング時にパスキー交換

② セキュアなペアリングモード
  └─ Bluetooth 4.2+ の Strong Authentication を使用

③ MITM（中間者攻撃）対策
  └─ BLE の Bonding 機能を利用

④ 通信データの保護
  └─ AES-128 での暗号化

⑤ デバイスの認可リスト
  └─ ホワイトリスト管理
```

## ベストプラクティス

```
✅ 実装時の推奨事項

① 接続状態の管理
   └─ isConnected フラグで状態追跡

② エラーハンドリング
   └─ 接続失敗時の再試行ロジック

③ バッテリー対策
   └─ 読み取り間隔を適切に設定

④ バージョン互換性
   └─ 複数の Bluetooth バージョンに対応

⑤ ロギング機能
   └─ デバッグ情報の記録
```

## まとめ

```
Bluetooth 通信の全体像：

1. デバイスペアリング
   └─ 一度だけ実施

2. スキャン・検出
   └─ デバイス探索

3. 接続確立
   └─ サービス・キャラクタリスティック発見

4. データ送受信
   └─ Read/Write/Notify 操作

5. 接続終了
   └─ リソース解放
```

BLEを使用することで、ラズベリーパイとUnityアプリケーション間で省電力かつ効率的にデータ通信が行えます。iOSとAndroidに向けたビルドでは、それぞれのプラットフォームに対応したBluetooth設定が必要です。

## 関連トピック

- [[IoT]]：IoT デバイス開発
- [[RaspberryPi]]：ラズベリーパイ活用
- [[Unity]]：Unity ゲームエンジン
- [[MobileApp]]：モバイルアプリ開発
- [[Networking]]：ネットワーク通信
