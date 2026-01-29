# MVP（Model-View-Presenter）

## 概要

### MVP とは

MVP（Model-View-Presenter）は、MVC の変形パターンで、View と Model を完全に分離することを目指します。Presenter が View と Model の仲介役となり、View から全てのビジネスロジックを排除します。

**テスト容易性を重視**するアーキテクチャパターンで、特にモバイルアプリケーション開発で採用されています。

### 特徴

- **完全な View-Model 分離**：View は Presenter に依存のみ
- **テスト容易性が高い**：Presenter をモック化して View をテスト
- **Presenter 中心**：ビジネスロジックを Presenter に集約
- **View は受動的**：View は表示のみ、入力は Presenter へ委譲
- **複雑なUI向け**：複雑な画面遷移やUI更新に対応

## アーキテクチャの構造

### MVP パターン

```
┌──────────────┐
│    User      │
│(ユーザー入力)│
└───────┬──────┘
        │
        │ イベント
        │
        ▼
┌─────────────────────────┐
│   Presenter             │
│ ・入力処理              │
│ ・ビジネスロジック      │
│ ・View更新指令          │
└────────┬────────────────┘
         │
         │ 更新指示
         │
         ▼
      ┌──────────┐
      │ View     │
      │ (UI表示) │
      └────┬─────┘
           │
        画面表示
           │
        ユーザーが見る

Model
  ↑
  │ データ取得・保存
  │
┌─────────────────────────┐
│   Presenter             │
│(Modelにアクセス)        │
└─────────────────────────┘
```

### MVC との違い

```
MVC：
Controller ◄─► Model
    ▼
   View

MVP：
Presenter ◄─► Model
  │
  ▼
 View (受動的)
```

## 各コンポーネント

### 1. Model（モデル）

```
責務：
- ビジネスロジック
- データ管理
- ビジネスルール
- バリデーション

特徴：
- View や Presenter に依存しない
- 純粋なビジネスロジック
- テストが非常に容易
- 再利用可能
```

#### Model の例

```java
public class User {
    private String id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    
    public User(String id, String name, String email) {
        validateEmail(email);
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }
    
    // ビジネスロジック
    public boolean isValidAge(int age) {
        return age >= 18;
    }
    
    public boolean isEmailValid() {
        return email.contains("@");
    }
    
    private void validateEmail(String email) {
        if (!email.contains("@")) {
            throw new IllegalArgumentException("Invalid email");
        }
    }
    
    // Getter
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
```

### 2. View（ビュー）

```
責務：
- UI表示
- ユーザー入力の取得
- Presenter への入力委譲
- Presenter からの指示に従う

特徴：
- 受動的（Passive View）
- ビジネスロジックはない
- 表示ロジックもない
- Presenter に完全に依存
- テストが容易
```

#### View インターフェース

```java
// View インターフェース
public interface UserCreationView {
    // 表示関連メソッド
    void showNameError(String message);
    void showEmailError(String message);
    void clearForm();
    void showSuccessMessage(String userId);
    void navigateToUserDetail(String userId);
    
    // ユーザー入力取得
    String getName();
    String getEmail();
}
```

#### View 実装（Android）

```java
public class UserCreationActivity 
    extends AppCompatActivity 
    implements UserCreationView {
    
    private EditText nameInput;
    private EditText emailInput;
    private Button submitButton;
    private UserCreationPresenter presenter;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_creation);
        
        nameInput = findViewById(R.id.name_input);
        emailInput = findViewById(R.id.email_input);
        submitButton = findViewById(R.id.submit_button);
        
        // Presenter を初期化
        presenter = new UserCreationPresenter(this);
        
        // ボタンクリックを Presenter に委譲
        submitButton.setOnClickListener(v -> 
            presenter.onCreateButtonClicked(
                getName(),
                getEmail()
            )
        );
    }
    
    @Override
    public String getName() {
        return nameInput.getText().toString();
    }
    
    @Override
    public String getEmail() {
        return emailInput.getText().toString();
    }
    
    @Override
    public void showNameError(String message) {
        nameInput.setError(message);
    }
    
    @Override
    public void showEmailError(String message) {
        emailInput.setError(message);
    }
    
    @Override
    public void clearForm() {
        nameInput.setText("");
        emailInput.setText("");
    }
    
    @Override
    public void showSuccessMessage(String userId) {
        Toast.makeText(this, 
            "User created: " + userId,
            Toast.LENGTH_SHORT).show();
    }
    
    @Override
    public void navigateToUserDetail(String userId) {
        Intent intent = new Intent(
            this,
            UserDetailActivity.class
        );
        intent.putExtra("user_id", userId);
        startActivity(intent);
    }
}
```

### 3. Presenter（プレゼンター）

```
責備：
- View とのやり取り
- ビジネスロジック実行
- Model へのアクセス
- View の更新指示
- ユースケース実装

特徴：
- Model と View の仲介役
- ビジネスロジック（新規追加はない）
- View 更新ロジック
- テストがしやすい（View をモック化）
```

#### Presenter の実装

```java
// Presenter インターフェース
public interface UserCreationPresenter {
    void onCreateButtonClicked(String name, String email);
    void onDestroy();
}

// Presenter 実装
public class UserCreationPresenterImpl 
    implements UserCreationPresenter {
    
    private UserCreationView view;
    private UserModel userModel;
    
    public UserCreationPresenterImpl(
        UserCreationView view,
        UserModel userModel) {
        this.view = view;
        this.userModel = userModel;
    }
    
    @Override
    public void onCreateButtonClicked(String name, String email) {
        // 1. Input validation
        if (name.isEmpty()) {
            view.showNameError("Name is required");
            return;
        }
        
        if (email.isEmpty()) {
            view.showEmailError("Email is required");
            return;
        }
        
        // 2. ビジネスロジック実行
        // （Model へ委譲）
        try {
            User newUser = userModel.createUser(name, email);
            
            // 3. View を更新
            view.showSuccessMessage(newUser.getId());
            view.clearForm();
            view.navigateToUserDetail(newUser.getId());
            
        } catch (EmailAlreadyExistsException e) {
            view.showEmailError("Email already registered");
        } catch (InvalidEmailException e) {
            view.showEmailError("Invalid email format");
        }
    }
    
    @Override
    public void onDestroy() {
        // リソースクリーンアップ
        view = null;
    }
}
```

## MVC vs MVP 比較

### MVC フロー

```
User Input
    ↓
Controller
    ↓ (バリデーション + ロジック)
Model
    ↓ (データ変更通知)
View (自動更新)
    ↓
Display
```

### MVP フロー

```
User Input
    ↓
View (受動的)
    ↓ (入力のみ)
Presenter
    ↓ (全てのロジック)
Model
    ↓ (データ操作)
Presenter
    ↓ (View 更新指示)
View (指示に従う)
    ↓
Display
```

## 実装パターン

### Passive View パターン

View が完全に受動的で、Presenter が全てを制御：

```java
// Passive View：何もしない
public class UserListActivity extends AppCompatActivity 
    implements UserListView {
    
    private ListView listView;
    private UserListPresenter presenter;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_list);
        
        listView = findViewById(R.id.user_list);
        presenter = new UserListPresenter(this);
        
        // ロード要求を Presenter に委譲
        presenter.loadUsers();
    }
    
    @Override
    public void displayUsers(List<UserDTO> users) {
        // Presenter の指示に従う
        ArrayAdapter<UserDTO> adapter = 
            new ArrayAdapter<>(
                this,
                android.R.layout.simple_list_item_1,
                users
            );
        listView.setAdapter(adapter);
    }
    
    @Override
    public void showError(String message) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }
}

// Presenter：全てを制御
public class UserListPresenter {
    
    private UserListView view;
    private UserRepository userRepository;
    
    public UserListPresenter(
        UserListView view,
        UserRepository userRepository) {
        this.view = view;
        this.userRepository = userRepository;
    }
    
    public void loadUsers() {
        try {
            List<User> users = userRepository.getAllUsers();
            
            // DTO に変換
            List<UserDTO> dtos = convertToDTO(users);
            
            // View に表示指示
            view.displayUsers(dtos);
            
        } catch (Exception e) {
            view.showError("Failed to load users");
        }
    }
    
    private List<UserDTO> convertToDTO(List<User> users) {
        return users.stream()
            .map(user -> new UserDTO(
                user.getId(),
                user.getName(),
                user.getEmail()
            ))
            .collect(Collectors.toList());
    }
}
```

### Supervising Controller パターン

View がデータバインディングを持つパターン：

```java
// Supervising View：データバインディング有り
public class UserListActivity extends AppCompatActivity 
    implements UserListView {
    
    private ListView listView;
    private UserListPresenter presenter;
    private UserListAdapter adapter;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user_list);
        
        listView = findViewById(R.id.user_list);
        adapter = new UserListAdapter();
        listView.setAdapter(adapter);
        
        presenter = new UserListPresenter(this);
        presenter.loadUsers();
    }
    
    @Override
    public void bindUsers(List<UserDTO> users) {
        // データバインディング：View が更新を管理
        adapter.setData(users);
    }
}
```

## テスト戦略

### Presenter のテスト

```java
public class UserCreationPresenterTest {
    
    private UserCreationView mockView;
    private UserModel mockModel;
    private UserCreationPresenter presenter;
    
    @Before
    public void setUp() {
        // モック作成
        mockView = mock(UserCreationView.class);
        mockModel = mock(UserModel.class);
        
        presenter = new UserCreationPresenterImpl(
            mockView,
            mockModel
        );
    }
    
    @Test
    public void testCreateUserSuccess() {
        // Arrange
        String name = "John";
        String email = "john@example.com";
        User expectedUser = new User("1", name, email);
        
        when(mockModel.createUser(name, email))
            .thenReturn(expectedUser);
        
        // Act
        presenter.onCreateButtonClicked(name, email);
        
        // Assert
        verify(mockView).showSuccessMessage("1");
        verify(mockView).clearForm();
        verify(mockView).navigateToUserDetail("1");
    }
    
    @Test
    public void testValidationError_EmptyName() {
        // Arrange
        String name = "";
        String email = "john@example.com";
        
        // Act
        presenter.onCreateButtonClicked(name, email);
        
        // Assert
        verify(mockView).showNameError("Name is required");
        verify(mockModel, never()).createUser(anyString(), anyString());
    }
    
    @Test
    public void testEmailAlreadyExists() {
        // Arrange
        String name = "John";
        String email = "john@example.com";
        
        when(mockModel.createUser(name, email))
            .thenThrow(new EmailAlreadyExistsException());
        
        // Act
        presenter.onCreateButtonClicked(name, email);
        
        // Assert
        verify(mockView).showEmailError("Email already registered");
    }
}
```

### View のテスト（自動テスト）

```java
@RunWith(AndroidJUnit4.class)
public class UserCreationActivityTest {
    
    @Rule
    public ActivityTestRule<UserCreationActivity> 
        rule = new ActivityTestRule<>(
            UserCreationActivity.class
        );
    
    @Test
    public void testUIDisplay() {
        // View が表示されるか確認
        onView(withId(R.id.name_input))
            .check(matches(isDisplayed()));
        
        onView(withId(R.id.email_input))
            .check(matches(isDisplayed()));
        
        onView(withId(R.id.submit_button))
            .check(matches(isDisplayed()));
    }
    
    @Test
    public void testFormSubmission() {
        // フォーム入力
        onView(withId(R.id.name_input))
            .perform(typeText("John"));
        
        onView(withId(R.id.email_input))
            .perform(typeText("john@example.com"));
        
        // ボタンクリック
        onView(withId(R.id.submit_button))
            .perform(click());
        
        // 結果確認
        onView(withText("User created"))
            .check(matches(isDisplayed()));
    }
}
```

## メリットとデメリット

### メリット

| メリット | 説明 |
|---------|------|
| **テスト容易性** | View をモック化してPresenterをテスト |
| **View は受動的** | Presenter が全て制御 |
| **ビジネスロジック集約** | Presenter に集約 |
| **複雑なUI対応** | 複雑な画面遷移に対応 |
| **Model独立** | Model は View に依存しない |
| **チーム分業** | UI開発とロジック開発を分離可能 |

### デメリット

| デメリット | 説明 |
|----------|------|
| **複雑性が増す** | Presenter層が必要 |
| **コードが増える** | Presenter + View インターフェース |
| **学習曲線** | 理解に時間がかかる |
| **初期開発コストが高い** | テンプレートコードが多い |
| **Presenter が肥大化** | 複雑なUIでは Presenter が大きくなる |

## 適用ガイドライン

### MVP を選ぶべき場合

```
✅ モバイルアプリケーション（Android、iOS）
✅ テスト自動化が重要
✅ 複雑なUI操作
✅ チーム開発で役割分担が必要
✅ レガシーコード改善
✅ UI と ロジックの完全分離が必要
```

### 避けるべき場合

```
❌ シンプルなアプリケーション
❌ チーム規模が小さい
❌ 短期プロジェクト
❌ Web アプリケーション（MVVM の方が良い）
```

## [[MVC]]との比較

| 特性 | MVC | MVP |
|-----|-----|-----|
| **View-Model 分離** | 直接結合 | 完全分離 |
| **テスト容易性** | 中 | 高 |
| **Presenter/Controller** | 薄い | 厚い |
| **ビジネスロジック** | Model + Controller | Presenter + Model |
| **主な用途** | Web | モバイル |
| **複雑性** | 低 | 中 |

## [[MVVM]]との比較

| 特性 | MVP | MVVM |
|-----|-----|------|
| **データバインディング** | なし | あり |
| **View依存性** | あり | 少ない |
| **テスト** | 高い | 非常に高い |
| **View-ViewModel通信** | メソッド呼び出し | データバインディング |

## まとめ

MVP は、**モバイルアプリケーション向けのテスト容易なアーキテクチャ**です。View を完全に受動的にし、Presenter がビジネスロジックと View 制御を統括します。

**重要なポイント：**
- View は受動的（Passive View）に保つ
- Presenter が全てを制御
- テストは Presenter に集中
- View インターフェースで依存関係を逆転

複雑なUI を持つモバイルアプリケーションで非常に効果的です。
