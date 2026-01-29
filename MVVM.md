# MVVM（Model-View-ViewModel）

## 概要

### MVVM とは

MVVM（Model-View-ViewModel）は、John Gossman によって 2005 年に Microsoft で提唱されたアーキテクチャパターンです。**データバインディング**を活用して、View と ViewModel を自動同期させます。

特に WPF（Windows Presentation Foundation）、Xamarin、そして近年では Flutter、React、Vue などのモダン UI フレームワークで採用されています。

### 特徴

- **データバインディング**：View と ViewModel の自動同期
- **View は受動的**：UI 更新ロジックなし
- **ViewModel がロジックを管理**：プレゼンテーション状態を管理
- **高度なテスト容易性**：ViewModel を独立してテスト
- **フレームワーク指向**：バインディング機能のあるフレームワーク前提

## アーキテクチャの構造

### MVVM パターン

```
┌──────────────┐
│    User      │
│ (ユーザー)   │
└───────┬──────┘
        │
        │ ユーザー入力
        │
        ▼
┌──────────────────────────┐
│ View                     │
│ ・UI要素                 │
│ ・バインディング定義      │
└──────────────┬───────────┘
               │
    ◄─────データバインディング─────►
               │
        ┌──────▼────────────┐
        │ ViewModel          │
        │ ・プレゼンテーション│
        │   ロジック         │
        │ ・状態管理         │
        │ ・コマンド         │
        │ ・プロパティ       │
        └──────┬────────────┘
               │
              △ 依存
               │
        ┌──────┴────────────┐
        │ Model              │
        │ ・ビジネスロジック │
        │ ・データ管理       │
        └────────────────────┘
```

### 特徴的なデータフロー

```
1. ユーザーが View で操作
   ↓
2. バインディングが ViewModel にデータを送信
   ↓
3. ViewModel がビジネスロジック実行（Model使用）
   ↓
4. ViewModel のプロパティが変更
   ↓
5. バインディングが自動的に View を更新
   ↓
6. ユーザーが画面更新を見る
```

## 各コンポーネント

### 1. Model（モデル）

```
責務：
- ビジネスロジック
- データ管理
- バリデーション

特徴：
- View や ViewModel に依存しない
- 純粋なビジネスロジック
```

#### Model の例

```csharp
// C# での Model
public class User
{
    public string Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public DateTime CreatedAt { get; set; }
    
    public User(string id, string name, string email)
    {
        ValidateEmail(email);
        Id = id;
        Name = name;
        Email = email;
        CreatedAt = DateTime.Now;
    }
    
    // ビジネスロジック
    public bool IsValidAge(int age)
    {
        return age >= 18;
    }
    
    private void ValidateEmail(string email)
    {
        if (!email.Contains("@"))
            throw new ArgumentException("Invalid email");
    }
}
```

### 2. View（ビュー）

```
責備：
- UI 表示
- バインディング定義
- ユーザー入力受け取り

特徴：
- ビジネスロジックなし
- Code-behind は最小限
- バインディングで ViewModel に接続
- 受動的
```

#### View の例（WPF/XAML）

```xaml
<!-- UserCreationView.xaml -->
<Window x:Class="UserApp.Views.UserCreationView"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    Title="Create User" Height="300" Width="400">
    
    <StackPanel Margin="20">
        <!-- NameプロパティにバインディングText を Text プロパティにバインディング
        <TextBlock Text="Name:" />
        <TextBox Text="{Binding Name, UpdateSourceTrigger=PropertyChanged}" 
                 Height="30" Margin="0,5"/>
        
        <!-- Email -->
        <TextBlock Text="Email:" Margin="0,10,0,0"/>
        <TextBox Text="{Binding Email, UpdateSourceTrigger=PropertyChanged}" 
                 Height="30" Margin="0,5"/>
        
        <!-- エラーメッセージ表示 -->
        <TextBlock Text="{Binding ErrorMessage}" 
                   Foreground="Red" Margin="0,10,0,0"/>
        
        <!-- ボタン：CreateUserCommand にバインディング -->
        <Button Command="{Binding CreateUserCommand}" 
                Content="Create" 
                Height="40" Margin="0,20,0,0"
                Background="Blue" Foreground="White"/>
        
        <!-- 成功メッセージ -->
        <TextBlock Text="{Binding SuccessMessage}" 
                   Foreground="Green" Margin="0,10,0,0"/>
    </StackPanel>
</Window>
```

#### View の Code-behind

```csharp
// UserCreationView.xaml.cs
public partial class UserCreationView : Window
{
    public UserCreationView()
    {
        InitializeComponent();
        
        // ViewModel をデータコンテキストに設定
        // これだけ！ビジネスロジックなし
        this.DataContext = new UserCreationViewModel();
    }
}
```

### 3. ViewModel（ビューモデル）

```
責務：
- プレゼンテーション状態管理
- ユーザー入力処理
- Model との連携
- View への通知
- コマンド定義

特徴：
- View に依存しない（XAML も参照しない）
- プロパティ定義（INotifyPropertyChanged）
- コマンド定義（ICommand）
- ビジネスロジックは Model に委譲
```

#### ViewModel の実装（WPF）

```csharp
// UserCreationViewModel.cs
using System;
using System.Windows.Input;

public class UserCreationViewModel : ViewModelBase
{
    private readonly UserService _userService;
    
    // プロパティ
    private string _name;
    public string Name
    {
        get { return _name; }
        set
        {
            if (_name != value)
            {
                _name = value;
                OnPropertyChanged(nameof(Name));
            }
        }
    }
    
    private string _email;
    public string Email
    {
        get { return _email; }
        set
        {
            if (_email != value)
            {
                _email = value;
                OnPropertyChanged(nameof(Email));
            }
        }
    }
    
    private string _errorMessage;
    public string ErrorMessage
    {
        get { return _errorMessage; }
        set
        {
            if (_errorMessage != value)
            {
                _errorMessage = value;
                OnPropertyChanged(nameof(ErrorMessage));
            }
        }
    }
    
    private string _successMessage;
    public string SuccessMessage
    {
        get { return _successMessage; }
        set
        {
            if (_successMessage != value)
            {
                _successMessage = value;
                OnPropertyChanged(nameof(SuccessMessage));
            }
        }
    }
    
    // コマンド
    public ICommand CreateUserCommand { get; }
    
    public UserCreationViewModel()
    {
        _userService = new UserService();
        CreateUserCommand = new RelayCommand(
            CreateUser,
            CanCreateUser
        );
    }
    
    // コマンド実行メソッド
    private void CreateUser()
    {
        // バリデーション
        if (string.IsNullOrEmpty(Name))
        {
            ErrorMessage = "Name is required";
            return;
        }
        
        if (string.IsNullOrEmpty(Email))
        {
            ErrorMessage = "Email is required";
            return;
        }
        
        // Model 経由でビジネスロジック実行
        try
        {
            User newUser = _userService.CreateUser(Name, Email);
            
            // 成功通知
            SuccessMessage = $"User created: {newUser.Id}";
            ErrorMessage = null;
            
            // フォーム初期化
            Name = "";
            Email = "";
        }
        catch (EmailAlreadyExistsException ex)
        {
            ErrorMessage = ex.Message;
        }
        catch (InvalidEmailException ex)
        {
            ErrorMessage = ex.Message;
        }
    }
    
    // コマンド実行可否判定
    private bool CanCreateUser()
    {
        return !string.IsNullOrEmpty(Name) && 
               !string.IsNullOrEmpty(Email);
    }
}

// ViewModelBase：INotifyPropertyChanged 実装
public abstract class ViewModelBase : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler PropertyChanged;
    
    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(
            this,
            new PropertyChangedEventArgs(propertyName)
        );
    }
}

// RelayCommand：ICommand 実装
public class RelayCommand : ICommand
{
    private readonly Action _execute;
    private readonly Func<bool> _canExecute;
    
    public RelayCommand(
        Action execute,
        Func<bool> canExecute = null)
    {
        _execute = execute ?? throw new ArgumentNullException(nameof(execute));
        _canExecute = canExecute;
    }
    
    public event EventHandler CanExecuteChanged
    {
        add { CommandManager.RequerySuggested += value; }
        remove { CommandManager.RequerySuggested -= value; }
    }
    
    public bool CanExecute(object parameter)
    {
        return _canExecute?.Invoke() ?? true;
    }
    
    public void Execute(object parameter)
    {
        _execute();
    }
}
```

## モダンフレームワークでの実装

### Vue.js での MVVM

```vue
<template>
  <div class="user-creation">
    <h1>Create User</h1>
    
    <!-- View：データバインディング -->
    <div>
      <label>Name:</label>
      <input v-model="name" placeholder="Enter name" />
    </div>
    
    <div>
      <label>Email:</label>
      <input v-model="email" placeholder="Enter email" />
    </div>
    
    <!-- エラーメッセージ表示 -->
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
    
    <!-- 成功メッセージ表示 -->
    <div v-if="successMessage" class="success">
      {{ successMessage }}
    </div>
    
    <!-- ボタン：メソッド呼び出し -->
    <button @click="createUser" :disabled="!canCreateUser">
      Create
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // ViewModel：状態管理
      name: '',
      email: '',
      errorMessage: '',
      successMessage: ''
    }
  },
  
  computed: {
    // 計算プロパティ
    canCreateUser() {
      return this.name.length > 0 && 
             this.email.length > 0;
    }
  },
  
  methods: {
    // ビジネスロジック実行
    createUser() {
      // バリデーション
      if (!this.name) {
        this.errorMessage = 'Name is required';
        return;
      }
      
      if (!this.email) {
        this.errorMessage = 'Email is required';
        return;
      }
      
      // API呼び出し（Model）
      this.$api.users.create({
        name: this.name,
        email: this.email
      })
      .then(response => {
        // 成功時：状態更新
        this.successMessage = `User created: ${response.id}`;
        this.errorMessage = '';
        this.name = '';
        this.email = '';
      })
      .catch(error => {
        // エラー時：状態更新
        this.errorMessage = error.message;
      });
    }
  }
}
</script>

<style scoped>
.user-creation {
  padding: 20px;
  max-width: 400px;
}

input {
  width: 100%;
  padding: 8px;
  margin: 5px 0 15px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: blue;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.error {
  color: red;
  margin: 10px 0;
}

.success {
  color: green;
  margin: 10px 0;
}
</style>
```

### Flutter での MVVM パターン

```dart
// Model
class User {
  final String id;
  final String name;
  final String email;
  
  User({
    required this.id,
    required this.name,
    required this.email,
  });
  
  // ビジネスロジック
  bool isValidAge(int age) => age >= 18;
  
  static void validateEmail(String email) {
    if (!email.contains('@')) {
      throw ArgumentError('Invalid email');
    }
  }
}

// Service（Model の一部）
class UserService {
  Future<User> createUser(String name, String email) async {
    User.validateEmail(email);
    
    // API呼び出し
    final response = await http.post(
      Uri.parse('http://api.example.com/users'),
      body: {
        'name': name,
        'email': email,
      },
    );
    
    if (response.statusCode == 200) {
      return User.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to create user');
    }
  }
}

// ViewModel
class UserCreationViewModel extends ChangeNotifier {
  final UserService _userService = UserService();
  
  // プロパティ（状態）
  String _name = '';
  String _email = '';
  String _errorMessage = '';
  String _successMessage = '';
  bool _isLoading = false;
  
  // Getter
  String get name => _name;
  String get email => _email;
  String get errorMessage => _errorMessage;
  String get successMessage => _successMessage;
  bool get isLoading => _isLoading;
  
  bool get canCreateUser =>
      _name.isNotEmpty && _email.isNotEmpty && !_isLoading;
  
  // Setter（バインディング用）
  void setName(String value) {
    _name = value;
    notifyListeners(); // View に通知
  }
  
  void setEmail(String value) {
    _email = value;
    notifyListeners();
  }
  
  // ビジネスロジック実行
  Future<void> createUser() async {
    // バリデーション
    if (_name.isEmpty) {
      _errorMessage = 'Name is required';
      notifyListeners();
      return;
    }
    
    if (_email.isEmpty) {
      _errorMessage = 'Email is required';
      notifyListeners();
      return;
    }
    
    try {
      _isLoading = true;
      notifyListeners();
      
      // Model にビジネスロジック実行
      final user = await _userService.createUser(_name, _email);
      
      // 成功
      _successMessage = 'User created: ${user.id}';
      _errorMessage = '';
      _name = '';
      _email = '';
      
    } catch (e) {
      // エラー
      _errorMessage = e.toString();
      _successMessage = '';
    } finally {
      _isLoading = false;
      notifyListeners(); // View に通知
    }
  }
}

// View
class UserCreationPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Create User')),
      body: ChangeNotifierProvider(
        create: (_) => UserCreationViewModel(),
        child: Consumer<UserCreationViewModel>(
          builder: (context, viewModel, _) {
            return Padding(
              padding: EdgeInsets.all(20),
              child: Column(
                children: [
                  // Name TextField
                  TextField(
                    onChanged: (value) => viewModel.setName(value),
                    decoration: InputDecoration(
                      labelText: 'Name',
                      errorText: viewModel.errorMessage.isNotEmpty
                          ? viewModel.errorMessage
                          : null,
                    ),
                  ),
                  
                  SizedBox(height: 16),
                  
                  // Email TextField
                  TextField(
                    onChanged: (value) => viewModel.setEmail(value),
                    decoration: InputDecoration(
                      labelText: 'Email',
                    ),
                  ),
                  
                  SizedBox(height: 16),
                  
                  // Error Message
                  if (viewModel.errorMessage.isNotEmpty)
                    Text(
                      viewModel.errorMessage,
                      style: TextStyle(color: Colors.red),
                    ),
                  
                  // Success Message
                  if (viewModel.successMessage.isNotEmpty)
                    Text(
                      viewModel.successMessage,
                      style: TextStyle(color: Colors.green),
                    ),
                  
                  SizedBox(height: 16),
                  
                  // Create Button
                  ElevatedButton(
                    onPressed: viewModel.canCreateUser
                        ? () => viewModel.createUser()
                        : null,
                    child: viewModel.isLoading
                        ? CircularProgressIndicator()
                        : Text('Create'),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
```

## テスト戦略

### ViewModel のテスト

```csharp
[TestFixture]
public class UserCreationViewModelTest
{
    private UserCreationViewModel _viewModel;
    private Mock<UserService> _mockUserService;
    
    [SetUp]
    public void Setup()
    {
        _mockUserService = new Mock<UserService>();
        _viewModel = new UserCreationViewModel(_mockUserService.Object);
    }
    
    [Test]
    public void CreateUser_Success()
    {
        // Arrange
        var expectedUser = new User("1", "John", "john@example.com");
        _mockUserService
            .Setup(s => s.CreateUser("John", "john@example.com"))
            .Returns(expectedUser);
        
        _viewModel.Name = "John";
        _viewModel.Email = "john@example.com";
        
        // Act
        _viewModel.CreateUserCommand.Execute(null);
        
        // Assert
        Assert.AreEqual("User created: 1", _viewModel.SuccessMessage);
        Assert.IsNull(_viewModel.ErrorMessage);
        _mockUserService.Verify(s => s.CreateUser("John", "john@example.com"));
    }
    
    [Test]
    public void CreateUser_ValidationError_EmptyName()
    {
        // Arrange
        _viewModel.Name = "";
        _viewModel.Email = "john@example.com";
        
        // Act
        _viewModel.CreateUserCommand.Execute(null);
        
        // Assert
        Assert.AreEqual("Name is required", _viewModel.ErrorMessage);
        _mockUserService.Verify(
            s => s.CreateUser(It.IsAny<string>(), It.IsAny<string>()),
            Times.Never);
    }
    
    [Test]
    public void CanCreateUser_ReturnsFalse_WhenNameOrEmailEmpty()
    {
        // Arrange
        _viewModel.Name = "";
        _viewModel.Email = "";
        
        // Act
        var result = _viewModel.CreateUserCommand.CanExecute(null);
        
        // Assert
        Assert.IsFalse(result);
    }
    
    [Test]
    public void CanCreateUser_ReturnsTrue_WhenBothFieldsFilled()
    {
        // Arrange
        _viewModel.Name = "John";
        _viewModel.Email = "john@example.com";
        
        // Act
        var result = _viewModel.CreateUserCommand.CanExecute(null);
        
        // Assert
        Assert.IsTrue(result);
    }
}
```

## メリットとデメリット

### メリット

| メリット | 説明 |
|---------|------|
| **自動同期** | データバインディングで自動更新 |
| **高度なテスト** | ViewModel を独立してテスト |
| **View は最小限** | UI ロジックがない |
| **再利用性** | ViewModel を複数 View で使用可能 |
| **デスクトップ向け** | WPF/Xamarin で標準 |
| **状態管理が明確** | ViewModel が状態を一元管理 |

### デメリット

| デメリット | 説明 |
|----------|------|
| **バインディングの複雑さ** | 複雑なバインディング式 |
| **フレームワーク依存** | バインディング機能が必須 |
| **デバッグの困難さ** | 自動同期が原因でバグ追跡が難しい |
| **パフォーマンス** | バインディングオーバーヘッド |
| **学習曲線** | 習得に時間がかかる |

## 適用ガイドライン

### MVVM を選ぶべき場合

```
✅ WPF / Xamarin アプリケーション
✅ Vue.js / React を使用する Web アプリ
✅ Flutter モバイルアプリケーション
✅ データバインディングが活発
✅ 複雑な UI 状態管理
✅ テスト自動化が重要
```

### 避けるべき場合

```
❌ バインディング機能のないフレームワーク
❌ シンプルな Web アプリケーション
❌ チーム規模が小さい
```

## [[MVP]]との比較

| 特性 | MVP | MVVM |
|-----|-----|------|
| **データ同期** | メソッド呼び出し | データバインディング |
| **View-Presenter関係** | 1:1 参照 | 疎結合 |
| **テスト** | 高い | 非常に高い |
| **フレームワーク依存** | 低い | 高い |
| **用途** | モバイル | デスクトップ・Web |

## まとめ

MVVM は、**データバインディングを活用した現代的なアーキテクチャ**です。View と ViewModel が自動同期され、テスト容易性が高くなります。

**重要なポイント：**
- View は受動的（バインディングのみ）
- ViewModel がプレゼンテーション状態を管理
- データバインディングで自動同期
- Model は ViewModel に依存しない

デスクトップアプリケーション、モダン Web フレームワーク（Vue、React）、Flutter などで非常に効果的です。
