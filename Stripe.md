# Stripe: 支払い処理と請求管理システム

## 概要

### Stripe Billingとは

Stripe Billingは、企業がサブスクリプションと請求書を簡単に管理できる強力なツールです。SaaS、メンバーシップサービス、定期購入など、様々なビジネスモデルに対応します。

### Stripeの主な機能

- **サブスクリプション管理**：定期的な課金を自動化
- **請求書管理**：自動発行、カスタマイズ、追跡
- **複数の決済方法**：クレジットカード、デビットカード、ウォレットなど
- **メーター課金**：使用量に基づいた課金
- **割引・クーポン**：柔軟な割引戦略
- **Webhook対応**：リアルタイムイベント処理
- **グローバル対応**：多通貨、多地域サポート

### Stripeの利点

- **高いセキュリティ**：PCI DSS Level 1準拠
- **充実したAPI**：豊富なドキュメントと実装例
- **優れた開発体験**：Stripeテストカードでサンドボックステスト可能
- **スケーラビリティ**：スタートアップから大規模企業まで対応
- **手厚いサポート**：充実したドキュメントとコミュニティ

## 公式リソース

### ダッシュボード

[Stripe ダッシュボード](https://dashboard.stripe.com/apps)

Stripeアカウントの管理、トランザクション確認、設定変更などの主要な操作を行います。

### ドキュメント

[Stripe 公式ドキュメント](https://docs.stripe.com/)

最新のAPI仕様、コードサンプル、ベストプラクティスが掲載されています。

### テストカード

[Stripe Terminal テストガイド](https://docs.stripe.com/terminal/references/testing?locale=ja-JP)

本番環境に進む前に、テストカードでサンドボックステストを実施します。

## Stripe Billingの基本セットアップ

### 1. アカウント作成

1. [Stripeの公式サイト](https://stripe.com/jp)にアクセス
2. 「アカウントを作成」をクリック
3. メールアドレスとパスワードを入力
4. 事業情報を入力
5. メール確認後、ダッシュボードにアクセス可能

### 2. プロダクトとプランの設定

Stripeでは、各種サービスや商品を「プロダクト」として登録し、それに紐づく「プラン」を設定します。

#### プロダクトの作成

```ruby
require 'stripe'
Stripe.api_key = 'your_secret_api_key'

# プロダクトの作成
product = Stripe::Product.create({
  name: 'Premium Plan',
  type: 'service',
  description: 'Premium subscription plan'
})

puts "Product created: #{product.id}"
```

#### プランの作成

```ruby
# プランの作成
plan = Stripe::Plan.create({
  product: product.id,
  nickname: 'Monthly Subscription',
  interval: 'month',
  interval_count: 1,
  currency: 'jpy',
  amount: 10000,  # ¥100.00
  usage_type: 'licensed'  # または 'metered'
})

puts "Plan created: #{plan.id}"
```

**プランのパラメータ説明:**

| パラメータ | 説明 | 例 |
|-----------|------|-----|
| `product` | プロダクトID | `prod_1234567890` |
| `interval` | 課金周期 | `day`, `week`, `month`, `year` |
| `interval_count` | 課金周期の倍数 | `2` で2ヶ月ごと |
| `currency` | 通貨コード | `jpy`, `usd`, `eur` |
| `amount` | 金額（最小単位） | `10000` (¥100.00) |
| `usage_type` | 課金タイプ | `licensed` または `metered` |

### 3. 顧客の作成

```ruby
# 顧客の作成
customer = Stripe::Customer.create({
  email: 'customer@example.com',
  name: 'John Doe',
  description: 'Test customer'
})

puts "Customer created: #{customer.id}"
```

### 4. サブスクリプションの作成

```ruby
# サブスクリプションの作成
subscription = Stripe::Subscription.create({
  customer: customer.id,
  items: [{
    plan: plan.id,
  }],
  payment_method: payment_method_id,  # または source: token
  confirm: true
})

puts "Subscription created: #{subscription.id}"
```

## 高度な機能

### メーター課金（従量課金）

使用量に基づいた課金をサポートします。

#### 使用記録の追加

```ruby
# 使用量を記録
usage_record = Stripe::SubscriptionItem.create_usage_record(
  'subscription_item_id',
  {
    quantity: 100,           # 使用量
    timestamp: Time.now.to_i,
    action: 'increment'      # increment または set
  }
)

puts "Usage recorded: #{usage_record.id}"
```

**action パラメータ:**
- `increment`：現在の使用量に加算
- `set`：使用量を指定値に設定

### 割引とクーポン

#### クーポンの作成

```ruby
# パーセンテージ割引
coupon = Stripe::Coupon.create({
  percent_off: 20,
  duration: 'once',        # 1回限り
  # duration: 'repeating',
  # duration_in_months: 3   # 3ヶ月間毎回適用
})

puts "Coupon created: #{coupon.id}"
```

**割引タイプ:**
- `percent_off`：パーセンテージ割引
- `amount_off`：固定金額割引（centで指定）

**duration:**
- `once`：初回課金のみ
- `repeating`：指定月数間毎回適用
- `forever`：永久に適用

#### 顧客にクーポンを適用

```ruby
# 顧客にクーポンを適用
updated_customer = Stripe::Customer.update(
  customer.id,
  {
    coupon: coupon.id
  }
)

puts "Coupon applied: #{updated_customer.coupon}"
```

### 促進クレジット

```ruby
# 促進クレジットの追加
invoice_item = Stripe::InvoiceItem.create({
  customer: customer.id,
  amount: -5000,  # 負の値で割引
  currency: 'jpy',
  description: 'Promotional credit'
})

puts "Credit added: #{invoice_item.id}"
```

## 継続的な請求管理

### 請求書の管理

#### 自動請求書の作成

```ruby
# サブスクリプション用の自動請求書はStripeが自動生成します
# 手動で請求書を作成する場合：

invoice = Stripe::Invoice.create({
  customer: customer.id,
  auto_advance: true  # 自動で最終化して送信
})

# 請求書の確定
finalized_invoice = invoice.finalize_invoice

puts "Invoice created: #{finalized_invoice.id}"
```

#### 請求書の一覧取得

```ruby
# 顧客の請求書を取得
invoices = Stripe::Invoice.list({
  customer: customer.id,
  limit: 10
})

invoices.data.each do |invoice|
  puts "Invoice: #{invoice.id}, Amount: #{invoice.total}, Status: #{invoice.status}"
end
```

#### 請求書のカスタマイズ

```ruby
# 請求書の更新
updated_invoice = Stripe::Invoice.update(
  invoice.id,
  {
    custom_fields: [{
      name: 'PO Number',
      value: 'PO-001'
    }],
    footer: 'Thank you for your business!'
  }
)

puts "Invoice updated"
```

### 支払い方法の管理

#### 支払い方法の作成

```ruby
# 支払い方法を作成
payment_method = Stripe::PaymentMethod.create({
  type: 'card',
  card: {
    number: '4242424242424242',
    exp_month: 12,
    exp_year: 2025,
    cvc: '314'
  }
})

puts "Payment method created: #{payment_method.id}"
```

#### サブスクリプションの支払い方法を更新

```ruby
# サブスクリプションの支払い方法を更新
updated_subscription = Stripe::Subscription.update(
  subscription.id,
  {
    default_payment_method: payment_method.id
  }
)

puts "Subscription payment method updated"
```

## React/Railsアプリへのサブスクリプション導入

### Stripe Checkout統合

Stripeが提供するホストされたCheckoutページを使用します。

#### React フロントエンド実装

```jsx
import React, { useState, useEffect } from "react";

const ProductDisplay = () => (
  <section>
    <div className="product">
      <img
        src="https://i.imgur.com/EHyR2nP.png"
        alt="Product image"
      />
      <div className="description">
        <h3>Premium Plan</h3>
        <h5>¥10,000/month</h5>
      </div>
    </div>
    <form action="/create-checkout-session" method="POST">
      <button type="submit">
        Subscribe Now
      </button>
    </form>
  </section>
);

const Message = ({ message }) => (
  <section>
    <p>{message}</p>
  </section>
);

export default function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const query = new URLSearchParams(window.location.search);

    if (query.get("success")) {
      setMessage("Subscription successful! Check your email for confirmation.");
    }

    if (query.get("canceled")) {
      setMessage("Subscription canceled. Please try again.");
    }
  }, []);

  return message ? (
    <Message message={message} />
  ) : (
    <ProductDisplay />
  );
}
```

#### Rails バックエンド実装

```ruby
require 'stripe'

class CheckoutSessionsController < ApplicationController
  skip_before_action :verify_authenticity_token, only: [:create]

  Stripe.api_key = ENV['STRIPE_SECRET_KEY']
  YOUR_DOMAIN = 'https://www.example.com'

  def create
    begin
      session = Stripe::Checkout::Session.create({
        line_items: [{
          price: params[:price_id],
          quantity: 1,
        }],
        mode: 'subscription',
        success_url: "#{YOUR_DOMAIN}?success=true",
        cancel_url: "#{YOUR_DOMAIN}?canceled=true",
      })

      render json: { url: session.url }, status: :ok
    rescue => e
      render json: { error: e.message }, status: :unprocessable_entity
    end
  end
end
```

#### ルーティング設定

```ruby
# config/routes.rb
post 'create-checkout-session', to: 'checkout_sessions#create'
```

### Stripe CLIでのテスト

Stripe CLIを使用してローカルで開発：

```bash
# Stripe CLIをインストール
brew install stripe/stripe-cli/stripe

# ログイン
stripe login

# イベントをローカルにフォワード
stripe listen --forward-to localhost:3000/webhook/stripe

# テストイベントを送信
stripe trigger checkout.session.completed
```

## RailsでStripeサブスクリプションAPIの実装

### セットアップ

#### Gemfileに追加

```ruby
gem 'stripe'
gem 'dotenv-rails'
```

#### .envファイル設定

```
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxx
STRIPE_ENDPOINT_SECRET=whsec_xxxxxxxxxxxxxx
```

### CheckoutSessionsController

```ruby
# app/controllers/checkout_sessions_controller.rb
class CheckoutSessionsController < ApplicationController
  skip_before_action :verify_authenticity_token, only: [:create]

  require 'stripe'

  Stripe.api_key = ENV['STRIPE_SECRET_KEY']
  YOUR_DOMAIN = 'https://www.pagespeedmonitor.jp'

  def create
    Rails.logger.info "Checkout request received with params: #{params.inspect}"
    
    begin
      price_id = params[:price_id]
      uid = params[:uid]
      plan = params[:plan]

      session = Stripe::Checkout::Session.create({
        line_items: [{
          price: price_id,
          quantity: 1,
        }],
        mode: 'subscription',
        success_url: "#{YOUR_DOMAIN}?success=true",
        cancel_url: "#{YOUR_DOMAIN}?canceled=true",
        metadata: {
          uid: uid,
          plan: plan
        }
      })

      render json: { url: session.url }, status: :ok
    rescue => e
      Rails.logger.error "Error creating checkout session: #{e.message}"
      render json: { error: e.message }, status: :unprocessable_entity
    end
  end
end
```

### APIの動作確認

```bash
# curlコマンドでテスト
curl -X POST http://localhost:3001/create-checkout-session \
  -H "Content-Type: application/json" \
  -d '{
    "price_id": "price_1234567890",
    "uid": "user123",
    "plan": "premium"
  }'
```

## Stripe Webhookの設定

### 概要

Webhook は、Stripeで発生したイベント（支払い成功、キャンセルなど）をリアルタイムでアプリケーションに通知します。

### ダッシュボードでの設定

1. [Stripeダッシュボード](https://dashboard.stripe.com/)にログイン
2. 「Developers」→「Webhooks」へ移動
3. 「Add endpoint」でエンドポイントを追加
4. エンドポイントURL を入力：
   ```
   https://www.pagespeedmonitor.jp/railsapp/webhook/handle_checkout_session_completed
   ```
5. イベントを選択：`checkout.session.completed`
6. Webhook シークレットを取得し、`.env`に保存

### 環境変数設定

```
STRIPE_ENDPOINT_SECRET=whsec_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### WebhooksController の実装

```ruby
# app/controllers/webhooks_controller.rb
class WebhooksController < ApplicationController
  skip_before_action :verify_authenticity_token

  def handle_checkout_session_completed
    payload = request.body.read
    sig_header = request.env['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = ENV['STRIPE_ENDPOINT_SECRET']

    begin
      event = Stripe::Webhook.construct_event(payload, sig_header, endpoint_secret)
    rescue JSON::ParserError => e
      render json: { message: 'Invalid payload' }, status: 400
      return
    rescue Stripe::SignatureVerificationError => e
      render json: { message: 'Invalid signature' }, status: 400
      return
    end

    # checkout.session.completed イベントの処理
    if event['type'] == 'checkout.session.completed'
      handle_checkout_session(event['data']['object'])
    end

    render json: { message: 'success' }, status: 200
  end

  private

  def handle_checkout_session(session)
    uid = session['metadata']['uid']
    plan = session['metadata']['plan']

    Rails.logger.info "Processing checkout for uid: #{uid}, plan: #{plan}"

    # ユーザーのプラン情報を更新
    uri = URI('https://www.pagespeedmonitor.jp/railsapp/users/update_plan')
    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    
    request = Net::HTTP::Put.new(uri.path, { 'Content-Type' => 'application/json' })
    request.body = {
      user: {
        uid: uid,
        plan: plan
      }
    }.to_json

    response = http.request(request)
    Rails.logger.info "Update plan response: #{response.body}"
  end
end
```

### ルーティング設定

```ruby
# config/routes.rb
post 'webhook/handle_checkout_session_completed', 
     to: 'webhooks#handle_checkout_session_completed'
```

### ローカルテスト

```bash
# Stripe CLIでローカルに通知をフォワード
stripe listen --forward-to localhost:3000/webhook/handle_checkout_session_completed

# テストイベントを送信
stripe trigger checkout.session.completed
```

## Stripeの解約機能

### サブスクリプションのキャンセル

#### 即座にキャンセル

```ruby
# サブスクリプションを即座にキャンセル
canceled_subscription = Stripe::Subscription.delete(
  subscription.id
)

puts "Subscription canceled: #{canceled_subscription.id}"
```

#### 期間終了時にキャンセル

```ruby
# 現在の課金期間終了時にキャンセル予約
subscription = Stripe::Subscription.update(
  subscription.id,
  {
    cancel_at_period_end: true
  }
)

puts "Subscription will cancel at: #{subscription.cancel_at}"
```

### キャンセル理由の記録

```ruby
# キャンセル理由を記録
subscription = Stripe::Subscription.update(
  subscription.id,
  {
    metadata: {
      cancellation_reason: 'Too expensive',
      canceled_by: 'customer',
      canceled_at: Time.now.to_s
    }
  }
)
```

### Webhook イベント：subscription.deleted

```ruby
# Webhookでキャンセルを処理
def handle_subscription_deleted(subscription)
  uid = subscription['metadata']['uid']
  
  # ユーザーのプラン情報をリセット
  user = User.find_by(uid: uid)
  user.update(plan: 'free', subscription_id: nil)
  
  Rails.logger.info "Subscription canceled for user: #{uid}"
end
```

## よくある設定パターン

### パターン1: 単一プラン（無料→有料）

```ruby
# プロダクト作成（1回）
product = Stripe::Product.create({
  name: 'Premium Service',
  type: 'service'
})

# 有料プラン
premium_plan = Stripe::Plan.create({
  product: product.id,
  amount: 10000,
  currency: 'jpy',
  interval: 'month'
})
```

### パターン2: 複数プラン（ティアード価格設定）

```ruby
# Basic プラン
basic_plan = Stripe::Plan.create({
  product: product.id,
  nickname: 'Basic',
  amount: 5000,
  currency: 'jpy',
  interval: 'month'
})

# Premium プラン
premium_plan = Stripe::Plan.create({
  product: product.id,
  nickname: 'Premium',
  amount: 15000,
  currency: 'jpy',
  interval: 'month'
})

# Enterprise プラン
enterprise_plan = Stripe::Plan.create({
  product: product.id,
  nickname: 'Enterprise',
  amount: 50000,
  currency: 'jpy',
  interval: 'month'
})
```

### パターン3: 試用期間付き

```ruby
# 試用期間（14日）付きサブスクリプション
subscription = Stripe::Subscription.create({
  customer: customer.id,
  items: [{
    plan: plan.id
  }],
  trial_period_days: 14
})

puts "Trial ends at: #{subscription.trial_end}"
```

### パターン4: 請求サイクルの開始日を指定

```ruby
# 月の1日に請求
subscription = Stripe::Subscription.create({
  customer: customer.id,
  items: [{
    plan: plan.id
  }],
  billing_cycle_anchor: Time.parse("2024-02-01").to_i
})
```

## トラブルシューティング

### よくあるエラーと解決方法

#### 1. `stripe_api_error: Invalid API Key`

```
原因：APIキーが正しく設定されていない
解決：Stripe.api_key = ENV['STRIPE_SECRET_KEY'] を確認
```

#### 2. `stripe_authentication_error: Unauthorized`

```
原因：本番環境のシークレットキーがテスト環境で使用されている
解決：テスト環境では sk_test_ で始まるキーを使用
```

#### 3. `stripe_rate_limit_error: Too Many Requests`

```
原因：API呼び出し回数が上限を超えた
解決：バッチ処理やリトライロジックを実装
```

#### 4. Webhook が受信されない

```
原因：エンドポイントURLが正しくない、署名検証が失敗している
解決：
1. ログで HTTP 200 が返されているか確認
2. 署名検証コードを確認
3. Stripe CLIで テストイベントを送信
```

#### 5. サブスクリプションの重複作成

```
原因：同じcustomerに複数のサブスクリプションが作成されている
解決：既存のサブスクリプションを確認してからアップグレード/ダウングレード
```

### デバッグのコツ

```ruby
# ログに詳細情報を出力
Stripe.enable_telemetry = false  # テレメトリを無効化

begin
  session = Stripe::Checkout::Session.create(params)
rescue Stripe::StripeError => e
  Rails.logger.error "Stripe error: #{e.message}"
  Rails.logger.error "Error code: #{e.code}"
  Rails.logger.error "Status: #{e.http_status}"
  raise e
end
```

## セキュリティ考慮事項

### APIキーの管理

```ruby
# ✅ 正しい方法：環境変数を使用
Stripe.api_key = ENV['STRIPE_SECRET_KEY']

# ❌ 間違い：コードに直接記述
Stripe.api_key = 'sk_test_xxxxxxxxxxxxxx'
```

### Webhook署名検証

```ruby
# ✅ 常に署名検証を行う
begin
  event = Stripe::Webhook.construct_event(
    payload, 
    sig_header, 
    endpoint_secret
  )
rescue Stripe::SignatureVerificationError => e
  render json: { error: 'Invalid signature' }, status: 400
  return
end
```

### 本番環境へのデプロイ

```ruby
# config/initializers/stripe.rb
Stripe.api_key = if Rails.env.production?
                    ENV['STRIPE_SECRET_KEY']
                  else
                    ENV['STRIPE_TEST_SECRET_KEY']
                  end
```

## ベストプラクティス

### 1. テストを充実させる

```ruby
# spec/controllers/checkout_sessions_controller_spec.rb
describe CheckoutSessionsController do
  describe 'POST #create' do
    it 'creates a checkout session' do
      VCR.use_cassette('stripe/checkout_session_create') do
        post :create, params: { price_id: 'price_123' }
        
        expect(response).to have_http_status(:ok)
        expect(JSON.parse(response.body)['url']).to match(/checkout.stripe.com/)
      end
    end
  end
end
```

### 2. 定期的な監査ログ

```ruby
# サブスクリプション変更を記録
after_update :log_subscription_change

def log_subscription_change
  if subscription_id_changed?
    SubscriptionLog.create({
      user: self,
      old_plan: subscription_id_was,
      new_plan: subscription_id,
      changed_at: Time.current
    })
  end
end
```

### 3. エラーハンドリング

```ruby
# リトライロジックの実装
def create_subscription_with_retry(customer_id, plan_id)
  max_retries = 3
  retry_count = 0

  begin
    Stripe::Subscription.create({
      customer: customer_id,
      items: [{ plan: plan_id }]
    })
  rescue Stripe::RateLimitError => e
    retry_count += 1
    sleep(2 ** retry_count)  # exponential backoff
    retry if retry_count < max_retries
    raise e
  end
end
```

## まとめ

Stripeは、複雑な支払い処理を簡潔に実装できる強力なプラットフォームです。以下のポイントを押さえることで、安全かつ効率的にサブスクリプションビジネスを構築できます：

- **APIキーを環境変数で管理**してセキュリティを確保
- **Webhook署名検証**を常に実装
- **テストモードで十分にテスト**してから本番運用
- **エラーハンドリングとログ記録**を充実させる
- **定期的に公式ドキュメント**を確認して最新の機能を活用
