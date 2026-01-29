# In-App Purchase: モバイルアプリ内課金システム

## 概要

### In-App Purchaseとは

In-App Purchase（以下、IAP）は、スマートフォンやタブレットなどのモバイルアプリ内で、追加のコンテンツや機能を購入できる仕組みです。IAPを利用することで、アプリ自体は無料または低価格で提供され、ユーザーは必要に応じて追加機能やコンテンツを購入する形となります。このモデルは、特にモバイルゲームやサブスクリプション型アプリで広く利用されています。

### IAPの特徴

- **プラットフォーム統合**：Apple App Store、Google Play Storeと直接統合
- **支払い方法多様性**：各プラットフォームで登録された支払い方法をサポート
- **自動更新**：定期購入の自動更新機能
- **プラットフォーム手数料**：App Store/Google Play が 15～30% の手数料を徴収
- **セキュリティ**：プラットフォームが支払い情報を管理し、開発者が直接扱わない

## IAPの種類

### 1. 消耗型アイテム（Consumable）

一度購入して使用すると消費されるアイテムです。使い切った場合、再度購入する必要があります。

**例:**
- ゲーム内通貨（コイン、ジェム）
- パワーアップアイテム
- 回復アイテム
- ブースター

**特徴:**
- 複数回購入が可能
- 購入履歴の追跡が必要
- ゲーム内ストレージに保存

**実装例（Swift）:**

```swift
import StoreKit

func purchaseConsumable(productId: String) {
    if #available(iOS 15, *) {
        Task {
            do {
                let result = try await AppStore.sync()
                // 同期後、ユーザーの購入履歴を確認
            } catch {
                print("Failed to sync: \(error)")
            }
        }
    }
}
```

### 2. 非消耗型アイテム（Non-Consumable）

一度購入すると永続的に使用できるアイテムや機能です。ユーザーが再度購入する必要はありません。

**例:**
- 広告の非表示化
- 追加レベル・ステージの解除
- プレミアム機能へのアクセス
- コンテンツパック

**特徴:**
- 1回限りの購入
- 購入後、復元可能
- ユーザーのアカウントに紐づく

**実装例（Dart/Flutter）:**

```dart
import 'package:in_app_purchase/in_app_purchase.dart';

class NonConsumableManager {
  final InAppPurchase _iap = InAppPurchase.instance;
  
  Future<void> purchaseNonConsumable(String productId) async {
    final ProductDetailsResponse response =
        await _iap.queryProductDetails(<String>{productId});
    
    if (response.productDetails.isNotEmpty) {
      final ProductDetails productDetails = response.productDetails.first;
      await _iap.buyConsumable(
        purchaseParam: PurchaseParam(productDetails: productDetails),
        autoConsume: false,  // 非消耗型は autoConsume=false
      );
    }
  }
}
```

### 3. 定期購入（Subscription）

定期的に料金が発生する購読型のサービスです。月額や年額で提供されるプレミアム機能やコンテンツアクセス権などが該当します。

**例:**
- 月額プレミアムサービス
- 年額メンバーシップ
- クラウドストレージ容量の拡張
- プレミアム機能へのアクセス

**特徴:**
- 自動更新（ユーザーがキャンセルしない限り）
- 試用期間設定可能
- 複数の価格帯を設定可能
- 更新失敗時の対応が必要

**価格階層例:**

| 階層 | 価格 | 試用期間 |
|------|------|---------|
| Basic | ¥400/月 | 7日間 |
| Standard | ¥1,000/月 | 無し |
| Premium | ¥2,500/月 | 30日間 |

## IAPの手数料体系

### Apple App Store

- **標準手数料**：30%
- **小規模事業者プログラム**：15%（年間売上100万円未満）
- **有効期限**：1年間

### Google Play

- **標準手数料**：30%
- **新規事業者優遇**：15%（最初の1年間）
- **有効期限**：1年間

## IAPのメリット

### 1. 柔軟な収益化

```
フロー：無料ユーザー → 有料ユーザーへの段階的転換
```

- アプリを無料で提供し、ユーザーを獲得
- ユーザーが必要に応じて追加機能やコンテンツを購入
- 多くのユーザーを引きつけることができる
- ダウンロード数の増加 → ランキング向上 → さらなるダウンロード増加

### 2. カスタマイズされたユーザー体験

- ユーザーは自分のニーズに合わせて機能を選択
- 自分好みの体験を作り上げることができる
- ユーザー満足度が向上
- アプリの評価やリテンション率も高くなる

### 3. 継続的な収益

定期購入型のIAPを導入することで：
- 安定した継続収益を見込める
- サブスクリプションモデルは長期的な収益基盤となる
- 予測可能な収益計画が立てられる

### 4. プラットフォームの安全性

- Apple/Googleが支払い情報を管理
- 開発者がクレジットカード情報を扱わない
- PCI DSS準拠が不要
- サポート体制が充実

## IAPのデメリット

### 1. 購入への抵抗感

一部のユーザーは、アプリ内での課金に対して抵抗感を持つ可能性：
- 課金に慎重なユーザーの離脱
- ネガティブレビューのリスク
- ユーザーが納得する形で価値を提供することが重要

### 2. 運営コストの増加

- 課金システムの開発・管理コスト
- 課金に関するサポート対応
- トラブル対応のリソース増加
- 定期的な商品内容の更新・管理

### 3. プラットフォーム依存

- App Store/Google Playのルール変更に対応する必要
- 手数料率の変更リスク
- アプリが削除されると収益も失われる
- プラットフォームのレビュープロセスを通過する必要

### 4. 技術的な複雑性

- トランザクション管理の複雑さ
- 購入履歴の同期・復元
- エラーハンドリング
- テスト環境の限定性

## Stripe vs Native IAP

### 主要な違い

| 項目 | Native IAP | Stripe |
|------|-----------|--------|
| **プラットフォーム**別対応 | 統合（App Store/Google Play） | Web共通 |
| **手数料** | 15-30% | 2.9% + 30円 |
| **サポート対象** | iOS/Android | Web/iOS/Android |
| **規制** | 必須（アプリ内課金を強制） | 選択的 |
| **復元機能** | 自動 | 手動実装 |
| **試用期間** | 標準機能 | 手動実装 |

### なぜStripeをアプリ内課金に使ってはいけないのか

**Apple App Storeの規制:**

App Storeのガイドラインでは、以下のルールがあります：

> 3.1.1 「App内課金」は、アプリ内でコンテンツ、機能、またはサービスをユーザーが購入できる場合に必須です。

**つまり:**
- サブスクリプション、アイテム購入などはApp内課金を使用する必要
- Stripeなどのサードパーティ決済を直接使用すると**アプリがリジェクト**される
- **例外：物理的商品・サービス**（食べ物の配達、ホテル予約など）

**リジェクト例:**

```
"2.1 App Completeness
Your app appears to use Apple's In-App Purchase API; however, 
it still offers subscriptions or services via Stripe.
Please use In-App Purchase for any digital subscriptions or services."
```

### 使い分けのポイント

**Native IAPを使うべき場合:**
- ✅ デジタルコンテンツの販売
- ✅ プレミアム機能のアンロック
- ✅ 定期購読（サブスクリプション）
- ✅ ゲーム内通貨・アイテム

**Stripeを使える場合:**
- ✅ 物理的商品の販売
- ✅ サービス提供（配達、予約など）
- ✅ Web上での支払い処理
- ✅ Androidのみの場合（一部制限あり）

## IAPの導入手順

### 1. ストア設定

#### Apple App Store

1. [App Store Connect](https://appstoreconnect.apple.com/)にログイン
2. **My Apps** → 対象アプリを選択
3. **App内課金** → **+** をクリック
4. 商品タイプを選択
5. 商品情報を入力：
   - 商品ID（例：`com.example.premium_monthly`）
   - 参照名（App Store Connect内での表示名）
   - 価格帯を選択
   - スクリーンショットを追加
6. **保存** → **送信して審査**

#### Google Play

1. [Google Play Console](https://play.google.com/console/)にログイン
2. **アプリを選択** → **商品化 > インアプリ商品**
3. **商品を作成** をクリック
4. 商品タイプを選択
5. 商品情報を入力：
   - 商品ID
   - デフォルト言語での商品名
   - 説明
   - 価格
6. **保存** → **有効化**

### 2. アプリへの実装

#### Flutter での実装例

**pubspec.yaml に追加:**

```yaml
dependencies:
  in_app_purchase: ^3.1.0
  in_app_purchase_storekit: ^0.3.0
```

**実装コード:**

```dart
import 'package:in_app_purchase/in_app_purchase.dart';

class InAppPurchaseManager {
  static final InAppPurchaseManager _instance = InAppPurchaseManager._internal();
  
  final InAppPurchase _iap = InAppPurchase.instance;
  
  factory InAppPurchaseManager() {
    return _instance;
  }
  
  InAppPurchaseManager._internal();
  
  // 利用可能かチェック
  Future<bool> isAvailable() async {
    final available = await _iap.isAvailable();
    return available;
  }
  
  // 商品情報を取得
  Future<List<ProductDetails>> getProducts(Set<String> productIds) async {
    final ProductDetailsResponse response = await _iap.queryProductDetails(productIds);
    return response.productDetails;
  }
  
  // 購入処理
  Future<void> purchase(ProductDetails productDetails) async {
    final PurchaseParam purchaseParam = PurchaseParam(
      productDetails: productDetails,
    );
    
    await _iap.buyConsumable(
      purchaseParam: purchaseParam,
      autoConsume: true,  // 消耗型の場合はtrue
    );
  }
  
  // 購入履歴を確認
  Future<List<PurchaseDetails>> getPurchaseHistory() async {
    final QueryPurchaseDetailsResponse response =
        await _iap.queryPastPurchases();
    return response.pastPurchases;
  }
  
  // 復元処理（非消耗型・サブスク用）
  Future<void> restorePurchases() async {
    await _iap.restorePurchases();
  }
  
  // ストリームリスナー
  Stream<List<PurchaseDetails>> getPurchaseStream() {
    return _iap.purchaseStream;
  }
}
```

### 3. テスト

#### Apple サンドボックステスト

1. [App Store Connect](https://appstoreconnect.apple.com/)で**ユーザーとアクセス** → **サンドボックス**
2. **テストユーザーアカウント**を作成
3. Xcode でテストユーザーアカウントでサインイン
4. アプリ内でテスト購入を実行

#### Google Play テスト

1. [Google Play Console](https://play.google.com/console/)で**テストの設定** → **ライセンスの設定**
2. **テスター** にメールアドレスを追加
3. アプリのベータ版を **テスター** に配布
4. テスト購入を実行

### 4. リリース

1. テスト完了後、アプリを本番環境にリリース
2. App内課金商品も本番環境で有効化
3. ユーザーがIAPを利用できるようになる
4. 定期的にレビューと改善を実施

## Firebase との連携（推奨パターン）

### 事例：FlutterアプリでFirebase + IAP

**アーキテクチャ:**

```
Flutter App
    ↓
In-App Purchase SDK
    ↓
Apple App Store / Google Play
    ↓
Firebaseサーバー（バックエンド検証）
    ↓
ユーザー情報・購入履歴 保存
```

**実装例:**

```dart
import 'package:firebase_functions/firebase_functions.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class PurchaseVerificationService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  
  // 購入をサーバー側で検証
  Future<void> verifyAndSavePurchase(PurchaseDetails purchase) async {
    try {
      // Firebase Cloud Functions を呼び出し
      final callable = FirebaseFunctions.instance
          .httpsCallable('verifyInAppPurchase');
      
      final result = await callable.call({
        'transactionId': purchase.transactionId,
        'productId': purchase.productID,
        'verificationData': purchase.verificationData.serverVerificationData,
      });
      
      if (result.data['isValid']) {
        // Firestoreに購入情報を保存
        await _firestore
            .collection('users')
            .doc(userId)
            .collection('purchases')
            .add({
              'productId': purchase.productID,
              'transactionId': purchase.transactionId,
              'purchaseDate': DateTime.now(),
              'status': 'verified'
            });
      }
    } catch (e) {
      print('Error verifying purchase: $e');
    }
  }
}
```

**Cloud Functions側（Node.js）:**

```typescript
import * as functions from 'firebase-functions';
import { admin } from 'firebase-admin';

// Apple検証
async function verifyAppleReceipt(receipt: string) {
  const response = await fetch('https://buy.itunes.apple.com/verifyReceipt', {
    method: 'POST',
    body: JSON.stringify({ 'receipt-data': receipt })
  });
  const data = await response.json();
  return data.status === 0;  // 0 = valid
}

// Google検証
async function verifyGooglePurchase(
  packageName: string,
  productId: string,
  token: string
) {
  const androidPublisher = google.androidpublisher('v3');
  const result = await androidPublisher.purchases.products.get({
    packageName,
    productId,
    token,
    auth: authClient
  });
  return result.data;
}

export const verifyInAppPurchase = functions.https.onCall(
  async (data, context) => {
    const { transactionId, productId, verificationData } = data;
    
    try {
      // プラットフォーム別に検証
      const isValid = await verifyAppleReceipt(verificationData);
      return { isValid };
    } catch (error) {
      throw new functions.https.HttpsError(
        'internal',
        'Failed to verify purchase'
      );
    }
  }
);
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. "商品がない、または購入できません" エラー

```
原因：商品IDが一致していない、App Store Connectで有効化されていない

解決：
1. 商品IDをコピー＆ペーストして確認（スペースがないか確認）
2. App Store Connect で商品が「準備完了」状態か確認
3. テストユーザーで再度試行
4. キャッシュをクリア：queryProductDetails() を再実行
```

#### 2. 購入後に復元されない

```
原因：購入情報がローカルに保存されていない

解決：
1. restorePurchases() を呼び出す
2. CloudFirestore に同期
3. ネットワーク接続を確認
```

#### 3. サンドボックステストが機能しない

```
原因：テストユーザーでサインインしていない

解決：
1. Xcode の Scheme 設定確認
2. テストユーザー情報が正しいか確認
3. StoreKit 設定ファイルを確認
4. Xcode をリビルド
```

#### 4. App Store からリジェクト

```
原因：App内課金の使用ルール違反

解決：
1. デジタル商品はApp内課金を使用
2. Stripeなどのサードパーティ決済を使用していないか確認
3. 試用期間情報が正しいか確認
4. Apple ガイドラインを再確認
```

## ベストプラクティス

### 1. サーバー側検証（必須）

```dart
// ❌ 悪い例：クライアント側のみ信頼
if (purchase.status == PurchaseStatus.purchased) {
  grantPremiumAccess();  // 検証なし
}

// ✅ 良い例：サーバー側で検証
final isValid = await verifyPurchaseOnServer(purchase);
if (isValid) {
  grantPremiumAccess();
}
```

### 2. 購入履歴の同期

```dart
// アプリ起動時に購入履歴を確認・同期
Future<void> syncPurchases() async {
  final purchases = await iap.queryPastPurchases();
  
  for (var purchase in purchases) {
    if (purchase.pendingCompletePurchase) {
      await iap.completePurchase(purchase);
    }
    
    // サーバーと同期
    await verifyAndSavePurchase(purchase);
  }
}
```

### 3. エラーハンドリング

```dart
try {
  await purchase(productDetails);
} on PlatformException catch (e) {
  if (e.code == 'BILLING_RESPONSE_CODE_USER_CANCELED') {
    print('User canceled purchase');
  } else if (e.code == 'BILLING_RESPONSE_CODE_ITEM_ALREADY_OWNED') {
    print('User already owns this item');
  } else {
    print('Purchase failed: ${e.message}');
  }
}
```

### 4. 適切な価格設定

- **心理的価格設定**：¥99, ¥499 など
- **階層化**：Basic → Standard → Premium
- **地域別設定**：各国の購買力に合わせて調整
- **定期的な見直し**：売上データから最適化

### 5. ユーザー体験の最適化

```dart
// 購入フローを簡潔に
1. 機能説明画面
2. 「購入」ボタンをタップ
3. App Store/Google Play の支払い画面
4. 完了画面

// リターゲティング
- 購入ユーザーへの感謝メッセージ
- 未購入ユーザーへの定期的なオファー
- 限時セール告知
```

## 実装時のチェックリスト

- [ ] App Store Connect で商品を作成・有効化
- [ ] Google Play Console で商品を作成・有効化
- [ ] in_app_purchase パッケージをインストール
- [ ] IAPManager クラスを実装
- [ ] 購入フローのUI を作成
- [ ] サーバー側の検証ロジックを実装
- [ ] テストユーザーでテスト実行
- [ ] サンドボックステスト完了
- [ ] エラーハンドリングを実装
- [ ] ローカライゼーション対応
- [ ] ログ記録を実装
- [ ] App Store Connect でビルドを送信
- [ ] App Store Review に合格
- [ ] 本番環境で稼働確認

## まとめ

In-App Purchase は、アプリの収益化戦略の一環として非常に効果的な手段です。

**重要なポイント:**
- **ネイティブIAPを使用**：App Store/Google Play の規制を遵守
- **サーバー側検証**：セキュリティを確保
- **ユーザー体験を優先**：無理な課金は避ける
- **定期的なメンテナンス**：商品情報や価格の見直し
- **ガイドラインの遵守**：各プラットフォームのルールに従う

適切に実装することで、安定した継続収益を見込め、ユーザー満足度も向上させることができます。
