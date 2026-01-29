# MVC（Model-View-Controller）

## 概要

### MVC とは

MVC（Model-View-Controller）は、最も古く、最も広く採用されているアーキテクチャパターンです。アプリケーションを 3 つの相互接続したコンポーネントに分割します。

1980年代から存在し、デスクトップアプリケーションから Web アプリケーション、モバイルアプリまで幅広く採用されています。

### 特徴

- **3つのコンポーネント**：Model、View、Controller
- **シンプル**：理解しやすく、導入が容易
- **広く採用**：業界標準のパターン
- **実績が豊富**：多くのフレームワークで採用
- **段階的な学習**：初心者向けのアーキテクチャ

## アーキテクチャの構造

### MVC パターン

```
                    ┌──────────┐
                    │  User    │
                    └────┬─────┘
                         │
                    入力（イベント）
                         │
                    ┌────▼─────┐
                    │ Controller│
                    │           │
                    │ (入力処理)│
                    └────┬─────┘
                         │
                    更新
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌───────┐        ┌──────┐        ┌──────┐
    │ Model │◄───────┤ View │        │ User │
    │       │  読取  │      │◄───────┤ 表示 │
    │(ビジ │        │(表現)│        │      │
    │ネス) │        │      │        └──────┘
    └───────┘        └──────┘
        ▲
        │
    変更通知
        │
```

## 各コンポーネント

### 1. Model（モデル）

```
責務：
- ビジネスロジック
- データ管理
- 状態管理
- バリデーション
- ビジネスルール実装

特徴：
- ビジネスに関するすべてを含む
- View や Controller に依存しない
- 再利用可能
- テストが容易
```

#### Model の例

```java
// User モデル
public class User {
    private Long id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    
    public User(String name, String email) {
        validateName(name);
        validateEmail(email);
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }
    
    // ビジネスロジック
    public boolean isValidAge(int age) {
        return age >= 18;
    }
    
    public void sendVerificationEmail() {
        // メール送信ロジック
    }
    
    // Getter/Setter
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}
```

### 2. View（ビュー）

```
責務：
- UI 表示
- Model データの表現
- ユーザーに情報を表示
- ユーザー入力を受け取る

特徴：
- Model のデータを表示するのみ
- ビジネスロジックは含まない
- 複数の View が同じ Model を表示可能
- Controller と通信
```

#### View の例（Web）

```html
<!-- users/show.html -->
<div class="user-profile">
    <h1><%= user.getName() %></h1>
    <p>Email: <%= user.getEmail() %></p>
    <p>Created: <%= user.getCreatedAt() %></p>
    
    <form action="/users/<%= user.getId() %>/edit" method="POST">
        <input type="hidden" name="_method" value="PUT">
        <input type="text" name="name" value="<%= user.getName() %>">
        <input type="email" name="email" value="<%= user.getEmail() %>">
        <button type="submit">Update</button>
    </form>
</div>
```

#### View の例（モバイル UI）

```swift
// iOS SwiftUI
struct UserView: View {
    @ObservedObject var user: UserModel
    
    var body: some View {
        VStack {
            Text(user.name)
                .font(.title)
            
            Text("Email: \(user.email)")
            
            Button("Edit") {
                // Controller に通知
            }
        }
    }
}
```

### 3. Controller（コントローラー）

```
責備：
- ユーザー入力を受け取る
- 入力をパースして Model に送信
- Model と View の調整
- イベント処理
- ナビゲーション制御
```

#### Controller の例

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    // GET: ユーザー一覧表示
    @GetMapping
    public String listUsers(Model model) {
        List<User> users = userService.getAllUsers();
        model.addAttribute("users", users);
        return "users/list"; // View を返す
    }
    
    // GET: ユーザー詳細表示
    @GetMapping("/{id}")
    public String showUser(
        @PathVariable Long id,
        Model model) {
        
        User user = userService.getUserById(id);
        if (user == null) {
            return "error/notfound";
        }
        
        model.addAttribute("user", user);
        return "users/show"; // View を返す
    }
    
    // POST: ユーザー作成
    @PostMapping
    public String createUser(
        @RequestParam String name,
        @RequestParam String email) {
        
        // 入力バリデーション
        if (name == null || name.isEmpty()) {
            return "error/invalid";
        }
        
        // Model に処理を委譲
        User user = userService.createUser(name, email);
        
        // リダイレクト
        return "redirect:/users/" + user.getId();
    }
    
    // PUT: ユーザー更新
    @PutMapping("/{id}")
    public String updateUser(
        @PathVariable Long id,
        @RequestParam String name,
        @RequestParam String email) {
        
        User user = userService.updateUser(id, name, email);
        return "redirect:/users/" + user.getId();
    }
    
    // DELETE: ユーザー削除
    @DeleteMapping("/{id}")
    public String deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return "redirect:/users";
    }
}
```

## MVC フロー（詳細）

### ユーザーが「ユーザー作成」をクリック

```
1. ユーザーが View のフォームにデータを入力
   ↓
2. フォーム送信（POST /users）
   ↓
3. Controller が POST リクエストを受け取る
   ↓
4. Controller が入力データをパース
   ↓
5. Controller が Model（Service）を呼び出す
   → userService.createUser(name, email)
   ↓
6. Model がビジネスロジックを実行
   - バリデーション
   - ユーザーオブジェクト作成
   - データベースに保存
   ↓
7. Model が結果を Controller に返す
   ↓
8. Controller が View を選択（表示）
   ↓
9. View が Model データを画面に表示
   ↓
10. ユーザーが画面を見る
```

## 実装例

### Rails での MVC

```ruby
# config/routes.rb
Rails.application.routes.draw do
  resources :users
end

# app/models/user.rb (Model)
class User < ApplicationRecord
  validates :name, presence: true
  validates :email, presence: true, uniqueness: true
  
  # ビジネスロジック
  def send_welcome_email
    UserMailer.welcome_email(self).deliver_later
  end
  
  def full_info
    "#{name} (#{email})"
  end
end

# app/controllers/users_controller.rb (Controller)
class UsersController < ApplicationController
  
  # GET /users
  def index
    @users = User.all # Model データを取得
  end
  
  # GET /users/new
  def new
    @user = User.new
  end
  
  # POST /users
  def create
    @user = User.new(user_params)
    
    if @user.save
      # Model が正常に保存された
      redirect_to @user, notice: 'User created'
    else
      # バリデーションエラー
      render :new
    end
  end
  
  # GET /users/:id
  def show
    @user = User.find(params[:id])
  end
  
  # GET /users/:id/edit
  def edit
    @user = User.find(params[:id])
  end
  
  # PUT /users/:id
  def update
    @user = User.find(params[:id])
    
    if @user.update(user_params)
      redirect_to @user, notice: 'User updated'
    else
      render :edit
    end
  end
  
  # DELETE /users/:id
  def destroy
    @user = User.find(params[:id])
    @user.destroy
    redirect_to users_url
  end
  
  private
  
  def user_params
    params.require(:user).permit(:name, :email)
  end
end

<!-- app/views/users/index.html.erb (View) -->
<h1>Users</h1>

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <% @users.each do |user| %>
      <tr>
        <td><%= user.name %></td>
        <td><%= user.email %></td>
        <td>
          <%= link_to 'Show', user %>
          <%= link_to 'Edit', edit_user_path(user) %>
          <%= link_to 'Delete', user, method: :delete %>
        </td>
      </tr>
    <% end %>
  </tbody>
</table>

<%= link_to 'New User', new_user_path %>

<!-- app/views/users/show.html.erb (View) -->
<h1><%= @user.name %></h1>
<p>Email: <%= @user.email %></p>

<%= link_to 'Edit', edit_user_path(@user) %>
<%= link_to 'Back', users_path %>
```

### Django での MVC（MTV）

Django は MVC を MTV（Model-Template-View）と呼びます：

```python
# models.py (Model)
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    # ビジネスロジック
    def send_welcome_email(self):
        pass
    
    class Meta:
        db_table = 'users'

# views.py (Controller)
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import User

class UserListView(View):
    def get(self, request):
        users = User.objects.all()  # Model を取得
        return render(request, 'users/list.html', {'users': users})

class UserDetailView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'users/detail.html', {'user': user})

class UserCreateView(View):
    def get(self, request):
        return render(request, 'users/create.html')
    
    def post(self, request):
        # フォーム入力を取得
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        # Model に処理を委譲
        user = User.objects.create(name=name, email=email)
        
        return redirect('user_detail', pk=user.id)

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
]

# templates/users/list.html (View)
<h1>Users</h1>

<ul>
    {% for user in users %}
        <li>
            <a href="{% url 'user_detail' user.id %}">
                {{ user.name }} ({{ user.email }})
            </a>
        </li>
    {% endfor %}
</ul>

<a href="{% url 'user_create' %}">New User</a>
```

## MVC のバリエーション

### Fat Model

```
Model にビジネスロジックを集中させる

利点：
✅ Controller がシンプル
✅ View が単純
✅ ビジネスロジックが一元管理

欠点：
❌ Model が肥大化
❌ テストが複雑になる
❌ 再利用性が低下
```

### Fat Controller

```
Controller にビジネスロジックを詰め込む

利点：
✅ 実装が早い
✅ 初期段階では簡単

欠点：
❌ Controller が肥大化
❌ テストが困難
❌ 再利用不可
❌ 複数のアクションで重複
```

### Thin Controller

```
Controller は入出力処理のみ、ビジネスロジックは Model に委譲

利点：
✅ テストが容易
✅ 再利用性が高い
✅ 責務が明確

欠点：
❌ Service層の設計が必要
```

### Service Layer パターン（MVC + Service）

```
Model
 ├── Entity（ドメインモデル）
 └── Repository（DB アクセス）

Service
 └── Business Logic（ビジネスロジック）

Controller → Service → Model
```

```java
// Service層を追加
@Service
public class UserService {
    
    private final UserRepository userRepository;
    
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User createUser(String name, String email) {
        // ビジネスロジック
        if (userRepository.existsByEmail(email)) {
            throw new EmailAlreadyExistsException();
        }
        
        User user = new User(name, email);
        return userRepository.save(user);
    }
}

// Controller で Service を使用
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    
    @PostMapping
    public ResponseEntity<User> createUser(
        @RequestBody UserRequest request) {
        User user = userService.createUser(
            request.getName(),
            request.getEmail()
        );
        return ResponseEntity.ok(user);
    }
}
```

## メリットとデメリット

### メリット

| メリット | 説明 |
|---------|------|
| **シンプル** | 構造が単純で理解しやすい |
| **導入が容易** | 学習曲線が緩やか |
| **広く採用** | 多くのフレームワークで使用 |
| **実績が豊富** | 多くのプロジェクトで検証済み |
| **小～中規模に最適** | 中程度のプロジェクトに適切 |
| **チーム開発が容易** | 役割分担が明確 |

### デメリット

| デメリット | 説明 |
|----------|------|
| **Model が肥大化しやすい** | ビジネスロジックが集中 |
| **View と Model の結合度** | 直接結合されやすい |
| **テストの困難さ** | Model のテストが複雑 |
| **再利用性の低さ** | View 固有のロジックが混在 |
| **大規模プロジェクトに不適切** | スケーラビリティの限界 |

## ベストプラクティス

### 1. Thin Controller + Fat Model パターン

```java
// ✅ Good：ビジネスロジックを Model に
@RestController
public class UserController {
    private final UserService userService;
    
    @PostMapping("/users")
    public ResponseEntity<User> createUser(
        @RequestBody UserRequest request) {
        User user = userService.createUser(
            request.getName(),
            request.getEmail()
        );
        return ResponseEntity.ok(user);
    }
}

@Service
public class UserService {
    public User createUser(String name, String email) {
        // ビジネスロジック：バリデーション
        validateEmail(email);
        validateName(name);
        
        // Entity作成
        User user = new User(name, email);
        return userRepository.save(user);
    }
}
```

### 2. ビジネスロジックを Model に集約

```java
// ✅ Good：ビジネスロジックが Model にある
public class User {
    private String email;
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    // ビジネスロジック
    public boolean isValid() {
        return isValidEmail(email);
    }
    
    private boolean isValidEmail(String email) {
        return email.contains("@");
    }
}
```

### 3. View には表示ロジックのみ

```erb
<!-- ✅ Good：View は表示のみ -->
<h1><%= @user.name %></h1>
<p>Email: <%= @user.email %></p>

<!-- ❌ Bad：View にビジネスロジック -->
<% if @user.email.contains("@") %>
    <p><%= @user.email %></p>
<% end %>
```

### 4. Service層で複雑ロジックを処理

```java
// ✅ Good：複雑なワークフローはService層
@Service
public class RegistrationService {
    
    public void registerUser(String name, String email) {
        // 1. ユーザーを作成（Model）
        User user = userRepository.createUser(name, email);
        
        // 2. メール送信（Service）
        emailService.sendWelcomeEmail(email);
        
        // 3. ログを記録（Service）
        auditService.log("User registered: " + email);
    }
}
```

## 適用ガイドライン

### MVC を選ぶべき場合

```
✅ Web アプリケーション
✅ CRUD アプリケーション
✅ 中規模プロジェクト
✅ 初心者チーム
✅ 従来的なビジネスアプリケーション
✅ マルチプラットフォーム対応（Rails等）
```

### 避けるべき場合

```
❌ 複雑なビジネスロジック
❌ リアルタイムイベント駆動
❌ マイクロサービス
❌ 非常に大規模なアプリケーション
```

## [[MVP]]、[[MVVM]]との比較

| 特性 | MVC | MVP | MVVM |
|-----|-----|-----|------|
| **複雑性** | 低 | 中 | 中 |
| **テスト** | 中 | 高 | 高 |
| **View データ結合** | 直接 | 間接 | バインディング |
| **主な用途** | Web | モバイル | デスクトップ・モバイル |

## まとめ

MVC は、**最も古く、最も広く採用されているアーキテクチャパターン**です。シンプルで理解しやすく、中規模 Web アプリケーションに最適です。

**重要なポイント：**
- Thin Controller + Fat Model を心がける
- ビジネスロジックは Model に集約
- Service層を活用して複雑さを管理
- View は表示ロジックに専念

適切に実装すれば、小～中規模プロジェクトで非常に効果的です。
