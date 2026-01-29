# レイヤードアーキテクチャ

## 概要

### レイヤードアーキテクチャとは

レイヤードアーキテクチャ（Layered Architecture）は、アプリケーションを複数の水平層（レイヤー）に分割するアーキテクチャパターンです。各層は特定の役割を持ち、上位層が下位層に依存する単方向の依存関係を持ちます。

**最も採用されているアーキテクチャ**として知られており、シンプルで理解しやすく、初心者向けです。

### 特徴

- **水平的な層構造**：UI層、ビジネスロジック層、データアクセス層など
- **単方向依存**：上位層が下位層に依存、逆は通常ない
- **シンプルさ**：理解しやすく導入が容易
- **スケーラビリティ**：中程度のアプリケーションに適している
- **標準的なパターン**：業界で広く採用されている

## レイヤー構成

### 標準的な 4 層構造

```
┌─────────────────────────────┐
│   プレゼンテーション層      │  UI・Web・API
│  (Presentation Layer)        │
└──────────────┬──────────────┘
               ↓ 依存
┌─────────────────────────────┐
│   ビジネスロジック層        │  ビジネスルール・検証
│  (Business Logic Layer)      │
└──────────────┬──────────────┘
               ↓ 依存
┌─────────────────────────────┐
│   永続化層                  │  DB・キャッシュ
│  (Persistence Layer)         │
└──────────────┬──────────────┘
               ↓ 依存
┌─────────────────────────────┐
│   データベース              │  実際のデータストア
│  (Database)                  │
└─────────────────────────────┘
```

### 各層の役割

#### 1. プレゼンテーション層（UI層）

```
責務：
- ユーザーインターフェース表示
- ユーザー入力受け取り
- バリデーション表示
- プレゼンテーションロジック

実装例：
- Web: HTML, CSS, JavaScript, React, Vue
- モバイル: iOS SwiftUI, Android Jetpack Compose
- デスクトップ: Qt, WPF, Electron
- API: REST エンドポイント定義
```

#### 2. ビジネスロジック層（アプリケーション層）

```
責務：
- ビジネスルール実装
- バリデーション
- トランザクション管理
- ワークフロー制御
- 複雑な計算処理

実装例：
- サービスクラス
- ドメインモデル
- ユースケース実装
```

#### 3. 永続化層（データアクセス層）

```
責備：
- データベースアクセス
- SQL クエリ実行
- ORM 利用
- キャッシュ管理
- リポジトリパターン実装

実装例：
- Repository クラス
- DAO (Data Access Object)
- ORM (Hibernate, SQLAlchemy)
- Query Builder
```

#### 4. データベース層

```
責務：
- 実際のデータ保存
- 永続化
- インデックス管理
- バックアップ

実装例：
- PostgreSQL
- MySQL
- MongoDB
- Redis
```

### 拡張：5層構造

```
┌─────────────────────────────┐
│   プレゼンテーション層      │  UI・Web・API
└────────────────┬────────────┘
                 ↓
┌─────────────────────────────┐
│   コントローラー層          │  リクエスト処理
└────────────────┬────────────┘
                 ↓
┌─────────────────────────────┐
│   ビジネスロジック層        │  ビジネスルール
└────────────────┬────────────┘
                 ↓
┌─────────────────────────────┐
│   永続化層                  │  DB アクセス
└────────────────┬────────────┘
                 ↓
┌─────────────────────────────┐
│   データベース              │  実際のデータ
└─────────────────────────────┘
```

## 実装例

### Java での レイヤードアーキテクチャ

#### プロジェクト構造

```
src/
├── presentation/
│   ├── controller/
│   │   └── UserController.java
│   └── dto/
│       └── UserRequest.java
├── business/
│   ├── service/
│   │   └── UserService.java
│   └── model/
│       └── User.java
├── persistence/
│   ├── repository/
│   │   └── UserRepository.java
│   └── entity/
│       └── UserEntity.java
└── config/
    └── AppConfig.java
```

#### ユーザー作成フロー実装

**Presentation層（Controller）:**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final UserService userService;
    
    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    // ユーザー作成
    @PostMapping
    public ResponseEntity<UserResponse> createUser(
        @RequestBody UserRequest request) {
        
        // 入力バリデーション
        if (request.getEmail() == null || request.getEmail().isEmpty()) {
            return ResponseEntity
                .badRequest()
                .build();
        }
        
        User user = userService.createUser(
            request.getName(),
            request.getEmail()
        );
        
        UserResponse response = new UserResponse(
            user.getId(),
            user.getName(),
            user.getEmail()
        );
        
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(response);
    }
    
    // ユーザー取得
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(
        @PathVariable Long id) {
        
        User user = userService.getUserById(id);
        
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        
        UserResponse response = new UserResponse(
            user.getId(),
            user.getName(),
            user.getEmail()
        );
        
        return ResponseEntity.ok(response);
    }
}
```

**Business層（Service）:**

```java
@Service
public class UserService {
    
    private final UserRepository userRepository;
    private final EmailValidator emailValidator;
    
    @Autowired
    public UserService(
        UserRepository userRepository,
        EmailValidator emailValidator) {
        this.userRepository = userRepository;
        this.emailValidator = emailValidator;
    }
    
    // ユーザー作成
    @Transactional
    public User createUser(String name, String email) {
        
        // ビジネスロジック：バリデーション
        if (!emailValidator.isValid(email)) {
            throw new InvalidEmailException("Invalid email format");
        }
        
        // ビジネスロジック：重複チェック
        if (userRepository.existsByEmail(email)) {
            throw new EmailAlreadyExistsException(
                "Email already registered");
        }
        
        // ユーザーオブジェクト作成
        User user = new User(name, email);
        user.setCreatedAt(LocalDateTime.now());
        
        // 永続化層に委譲
        return userRepository.save(user);
    }
    
    // ユーザー取得
    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElse(null);
    }
    
    // ユーザー更新
    @Transactional
    public User updateUser(Long id, String name, String email) {
        User user = getUserById(id);
        
        if (user == null) {
            throw new UserNotFoundException(
                "User not found: " + id);
        }
        
        // バリデーション
        if (!emailValidator.isValid(email)) {
            throw new InvalidEmailException(
                "Invalid email format");
        }
        
        user.setName(name);
        user.setEmail(email);
        user.setUpdatedAt(LocalDateTime.now());
        
        return userRepository.save(user);
    }
}
```

**Persistence層（Repository）:**

```java
@Repository
public interface UserRepository 
    extends JpaRepository<UserEntity, Long> {
    
    UserEntity findByEmail(String email);
    
    boolean existsByEmail(String email);
    
    List<UserEntity> findByNameContaining(String name);
}
```

**ドメインモデル：**

```java
public class User {
    private Long id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }
    
    // Getter/Setter
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    
    public void setName(String name) { this.name = name; }
    public void setEmail(String email) { this.email = email; }
    public void setCreatedAt(LocalDateTime createdAt) { 
        this.createdAt = createdAt; 
    }
    public void setUpdatedAt(LocalDateTime updatedAt) { 
        this.updatedAt = updatedAt; 
    }
}
```

### Python での レイヤードアーキテクチャ

```python
# app/presentation/routes.py
from flask import Blueprint, request, jsonify
from app.business.services import UserService

user_bp = Blueprint('users', __name__, url_prefix='/api/users')
user_service = UserService()

@user_bp.route('', methods=['POST'])
def create_user():
    """ユーザー作成"""
    data = request.get_json()
    
    # バリデーション
    if not data.get('email'):
        return {'error': 'Email is required'}, 400
    
    user = user_service.create_user(
        name=data['name'],
        email=data['email']
    )
    
    return {
        'id': user['id'],
        'name': user['name'],
        'email': user['email']
    }, 201

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ユーザー取得"""
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return user

# app/business/services.py
from app.persistence.repository import UserRepository
from app.business.validators import EmailValidator

class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.email_validator = EmailValidator()
    
    def create_user(self, name, email):
        """ユーザー作成"""
        
        # バリデーション
        if not self.email_validator.is_valid(email):
            raise ValueError("Invalid email format")
        
        if self.repository.exists_by_email(email):
            raise ValueError("Email already registered")
        
        user = {
            'name': name,
            'email': email
        }
        
        return self.repository.save(user)
    
    def get_user_by_id(self, user_id):
        """ユーザー取得"""
        return self.repository.find_by_id(user_id)

# app/persistence/repository.py
from app.persistence.database import db

class UserRepository:
    def save(self, user):
        """ユーザー保存"""
        result = db.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user['name'], user['email'])
        )
        db.commit()
        
        return {
            'id': result.lastrowid,
            'name': user['name'],
            'email': user['email']
        }
    
    def find_by_id(self, user_id):
        """ID でユーザー取得"""
        return db.query(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    
    def exists_by_email(self, email):
        """メールアドレスが存在するか確認"""
        result = db.query(
            "SELECT COUNT(*) FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        
        return result[0] > 0
```

## メリットとデメリット

### メリット

| メリット | 説明 |
|---------|------|
| **理解しやすい** | 層の責務が明確で、開発者が理解しやすい |
| **実装が容易** | 標準的なパターンで、実装リソースが豊富 |
| **テストが簡単** | 各層を独立してテスト可能 |
| **チーム開発に適している** | 役割分担が明確（UI開発、バックエンド開発） |
| **段階的開発が可能** | 各層を段階的に実装できる |
| **中規模アプリに最適** | 中程度の複雑さのプロジェクトに向いている |

### デメリット

| デメリット | 説明 |
|----------|------|
| **スケーラビリティの限界** | 大規模複雑なアプリケーションでは層が厚くなる |
| **層の分離が曖昧** | ビジネスロジックとプレゼンテーション層の分離が難しい場合がある |
| **横断的関心事が処理困難** | ロギング、セキュリティなどが層を横断する |
| **テーブル駆動設計になりやすい** | データベース設計が中心になる傾向 |
| **デプロイ統合の難しさ** | 各層の修正がデプロイに影響しやすい |
| **マイクロサービス非対応** | 単一のモノリシックアーキテクチャ |

## ベストプラクティス

### 層の責務を明確にする

```
✅ 各層は単一責任原則に従う
✅ 層間の依存関係は明確に定義
✅ 層を超えたアクセスは避ける
```

### 層間通信のアプローチ

```
✅ Controller → Service → Repository → DB
✅ 逆方向の依存関係は避ける
✅ 下位層が上位層を知らない設計
```

### Dependency Injection を使用

```java
// ✅ Good：依存性注入
@Service
public class UserService {
    private final UserRepository repository;
    
    @Autowired
    public UserService(UserRepository repository) {
        this.repository = repository;
    }
}

// ❌ Bad：硬く結合
@Service
public class UserService {
    private UserRepository repository = new UserRepository();
}
```

### DTO（Data Transfer Object）を活用

```java
// Presentation層用の DTO
public class UserRequest {
    private String name;
    private String email;
}

// Business層用のドメインモデル
public class User {
    private Long id;
    private String name;
    private String email;
}

// Persistence層用の Entity
@Entity
public class UserEntity {
    @Id
    private Long id;
    private String name;
    private String email;
}
```

### エラー処理の層的な設計

```java
// 層別エラーハンドリング
public class UserController {
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(
        UserNotFoundException ex) {
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage()));
    }
}

public class UserService {
    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> 
                new UserNotFoundException("User not found"));
    }
}
```

## 適用ガイドライン

### レイヤードアーキテクチャを選ぶべき場合

```
✅ CRUD アプリケーション
✅ 中規模 Web アプリケーション
✅ チーム開発で役割分担が必要
✅ 明確なビジネスロジックが存在
✅ 従来的な 3 層構造で十分
```

### 避けるべき場合

```
❌ マイクロサービスアーキテクチャが必要
❌ 複雑なドメインロジック
❌ リアルタイムイベント駆動システム
❌ 非常に大規模なアプリケーション
❌ 複数チームによる独立した開発
```

## まとめ

レイヤードアーキテクチャは、**シンプルで実用的なアーキテクチャパターン**です。明確な層構造により、チーム開発が容易で、初心者向けプロジェクトに最適です。

ただし、アプリケーションが複雑化する場合は、[[ヘキサゴナルアーキテクチャ]]や[[クリーンアーキテクチャ]]への移行を検討すべき場合があります。

**重要なポイント：**
- 層の責務を明確に保つ
- 依存性注入を活用する
- 下位層が上位層を知らない
- テストしやすい設計を心がける
