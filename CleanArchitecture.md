# クリーンアーキテクチャ

## 概要

### クリーンアーキテクチャとは

クリーンアーキテクチャ（Clean Architecture）は、Robert C. Martin（Uncle Bob）によって2012年に提唱されたアーキテクチャパターンです。ビジネスロジックをどの層に配置すべきか、依存関係をどう管理するかについて、明確な指針を提供します。

**依存性逆転原則**に基づき、外側から内側への依存性のみを許可し、内側の層は外側に依存しません。

### 特徴

- **同心円状の層構造**：4つの層（Entities、Use Cases、Interface Adapters、Frameworks）
- **依存方向が内側へ向かう**：外側は内側に依存するが、内側は外側に依存しない
- **ビジネスロジック中心**：フレームワークに依存しないコア
- **テスト容易性**：各層を独立してテスト可能
- **フレームワーク非依存**：フレームワークの変更に強い

## 層の構成

### クリーンアーキテクチャの 4 層

```
                    ┌─────────────────────────┐
                    │   Frameworks & Drivers  │
                    │  (Web, UI, DB, etc)     │
                    └──────────────┬──────────┘
                                   │
                    ┌──────────────▼──────────┐
                    │ Interface Adapters      │
                    │ (Controllers, Presenters)
                    └──────────────┬──────────┘
                                   │
                    ┌──────────────▼──────────┐
                    │  Application Business   │
                    │  Rules (Use Cases)      │
                    └──────────────┬──────────┘
                                   │
                    ┌──────────────▼──────────┐
                    │ Enterprise Business     │
                    │ Rules (Entities)        │
                    └─────────────────────────┘

依存方向：外側 → 内側のみ
         内側は外側に依存しない
```

### 各層の詳細

#### 1. Entities（企業全体のビジネスルール）

```
責務：
- 最も変わらないビジネスルール
- 複数のアプリケーションで共有可能
- Enterprise-wide ビジネスルール

実装例：
- ドメインモデル（User、Order、Product等）
- 値オブジェクト（Money、Email、Address等）
- ドメインサービス
```

#### 2. Use Cases（アプリケーション固有のビジネスルール）

```
責備：
- 特定のアプリケーションのビジネスルール
- ユースケース（ユーザー作成、注文処理等）
- Entities を使用して実装
- アプリケーション層

実装例：
- UseCase インターフェース
- Request/Response
- Interactor（UseCase実装）
- Repository インターフェース
```

#### 3. Interface Adapters（インターフェース・アダプター）

```
責務：
- Use Cases と外部システムの変換
- フレームワークからのデータを Use Cases 用に変換
- Use Cases の結果を外部用に変換
- DB、Web、UI等との連携

実装例：
- Controllers
- Presenters
- Gateways
- DTO (Data Transfer Object)
```

#### 4. Frameworks & Drivers（フレームワーク・ドライバー）

```
責務：
- 実際のフレームワーク・ライブラリの使用
- Web フレームワーク（Spring、Rails）
- データベース（PostgreSQL、MongoDB）
- UI ライブラリ

実装例：
- Spring Boot、Flask
- JPA、SQLAlchemy
- React、Vue
```

## 実装例

### Java での クリーンアーキテクチャ

#### プロジェクト構造

```
src/
├── entities/
│   └── User.java
├── usecases/
│   ├── CreateUserUseCase.java
│   ├── CreateUserRequest.java
│   ├── CreateUserResponse.java
│   └── UserRepository.java (interface)
├── adapters/
│   ├── web/
│   │   ├── UserController.java
│   │   └── UserPresenter.java
│   ├── db/
│   │   ├── UserRepositoryImpl.java
│   │   └── UserJpaRepository.java
│   └── dto/
│       └── UserDTO.java
└── frameworks/
    ├── config/
    │   └── AppConfig.java
    └── Application.java
```

#### Entity（Entities層）

```java
// entities/User.java
public class User {
    private String id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    
    public User(String id, String name, String email) {
        if (id == null || id.isEmpty()) {
            throw new DomainException("ID cannot be empty");
        }
        if (!isValidEmail(email)) {
            throw new DomainException("Invalid email");
        }
        
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }
    
    private static boolean isValidEmail(String email) {
        return email != null && email.matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }
    
    // ビジネスロジック：ドメイン固有の処理
    public void changeName(String newName) {
        if (newName == null || newName.isEmpty()) {
            throw new DomainException("Name cannot be empty");
        }
        this.name = newName;
    }
    
    public void changeEmail(String newEmail) {
        if (!isValidEmail(newEmail)) {
            throw new DomainException("Invalid email");
        }
        this.email = newEmail;
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
```

#### Use Cases（Use Cases層）

```java
// usecases/CreateUserRequest.java
public class CreateUserRequest {
    private String name;
    private String email;
    
    public CreateUserRequest(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    public String getName() { return name; }
    public String getEmail() { return email; }
}

// usecases/CreateUserResponse.java
public class CreateUserResponse {
    private String id;
    private String name;
    private String email;
    
    public CreateUserResponse(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

// usecases/UserRepository.java (Repository Interface)
public interface UserRepository {
    void save(User user);
    User findById(String id);
    boolean existsByEmail(String email);
}

// usecases/CreateUserUseCase.java (Interactor)
public class CreateUserUseCase {
    
    private final UserRepository userRepository;
    private final UserPresenter presenter;
    
    public CreateUserUseCase(
        UserRepository userRepository,
        UserPresenter presenter) {
        this.userRepository = userRepository;
        this.presenter = presenter;
    }
    
    public CreateUserResponse execute(CreateUserRequest request) {
        // バリデーション
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new UseCaseException("Email already registered");
        }
        
        // ユーザー作成（Entity使用）
        String userId = generateUserId();
        User user = new User(
            userId,
            request.getName(),
            request.getEmail()
        );
        
        // リポジトリに保存
        userRepository.save(user);
        
        // レスポンス生成
        return new CreateUserResponse(
            user.getId(),
            user.getName(),
            user.getEmail()
        );
    }
    
    private String generateUserId() {
        return UUID.randomUUID().toString();
    }
}
```

#### Adapter（Interface Adapters層）

```java
// adapters/web/UserController.java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final CreateUserUseCase createUserUseCase;
    private final UserPresenter presenter;
    
    @Autowired
    public UserController(
        CreateUserUseCase createUserUseCase,
        UserPresenter presenter) {
        this.createUserUseCase = createUserUseCase;
        this.presenter = presenter;
    }
    
    @PostMapping
    public ResponseEntity<UserDTO> createUser(
        @RequestBody UserDTO request) {
        
        // DTOを Use Case 用にマップ
        CreateUserRequest useCaseRequest = 
            new CreateUserRequest(
                request.getName(),
                request.getEmail()
            );
        
        // Use Case 実行
        CreateUserResponse response = 
            createUserUseCase.execute(useCaseRequest);
        
        // Presenter でレスポンス生成
        UserDTO dto = presenter.present(response);
        
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(dto);
    }
}

// adapters/web/UserPresenter.java
@Component
public class UserPresenter {
    
    public UserDTO present(CreateUserResponse response) {
        return new UserDTO(
            response.getId(),
            response.getName(),
            response.getEmail()
        );
    }
}

// adapters/dto/UserDTO.java
public class UserDTO {
    private String id;
    private String name;
    private String email;
    
    public UserDTO(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Getter/Setter
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    
    public void setId(String id) { this.id = id; }
    public void setName(String name) { this.name = name; }
    public void setEmail(String email) { this.email = email; }
}
```

#### Framework（Frameworks & Drivers層）

```java
// frameworks/db/UserRepositoryImpl.java
@Repository
public class UserRepositoryImpl implements UserRepository {
    
    private final UserJpaRepository jpaRepository;
    
    @Autowired
    public UserRepositoryImpl(UserJpaRepository jpaRepository) {
        this.jpaRepository = jpaRepository;
    }
    
    @Override
    public void save(User user) {
        UserEntity entity = new UserEntity(
            user.getId(),
            user.getName(),
            user.getEmail(),
            user.getCreatedAt()
        );
        jpaRepository.save(entity);
    }
    
    @Override
    public User findById(String id) {
        UserEntity entity = jpaRepository.findById(id)
            .orElse(null);
        
        if (entity == null) return null;
        
        return new User(
            entity.getId(),
            entity.getName(),
            entity.getEmail()
        );
    }
    
    @Override
    public boolean existsByEmail(String email) {
        return jpaRepository.existsByEmail(email);
    }
}

// frameworks/db/UserJpaRepository.java
@Repository
public interface UserJpaRepository
    extends JpaRepository<UserEntity, String> {
    boolean existsByEmail(String email);
}

// frameworks/config/AppConfig.java
@Configuration
public class AppConfig {
    
    @Bean
    public CreateUserUseCase createUserUseCase(
        UserRepository userRepository,
        UserPresenter presenter) {
        return new CreateUserUseCase(userRepository, presenter);
    }
}
```

### Python での 実装例

```python
# entities/user.py
from datetime import datetime
import re

class User:
    def __init__(self, user_id: str, name: str, email: str):
        if not user_id:
            raise ValueError("ID is required")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email")
        
        self._id = user_id
        self._name = name
        self._email = email
        self._created_at = datetime.now()
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[A-Za-z0-9+_.-]+@(.+)$'
        return re.match(pattern, email) is not None
    
    def change_email(self, new_email: str) -> None:
        if not self._is_valid_email(new_email):
            raise ValueError("Invalid email")
        self._email = new_email
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def email(self):
        return self._email
    
    @property
    def created_at(self):
        return self._created_at

# usecases/create_user.py
from abc import ABC, abstractmethod
from entities.user import User
from typing import Optional

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

class CreateUserRequest:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class CreateUserResponse:
    def __init__(self, user_id: str, name: str, email: str):
        self.id = user_id
        self.name = name
        self.email = email

class CreateUserUseCase:
    def __init__(self, 
                 user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # バリデーション
        if self.user_repository.exists_by_email(request.email):
            raise Exception("Email already registered")
        
        # Entity 作成
        import uuid
        user_id = str(uuid.uuid4())
        user = User(user_id, request.name, request.email)
        
        # 保存
        self.user_repository.save(user)
        
        # レスポンス返却
        return CreateUserResponse(user.id, user.name, user.email)

# adapters/web.py
from flask import Blueprint, request, jsonify
from usecases.create_user import CreateUserUseCase

def create_user_routes(usecase: CreateUserUseCase):
    bp = Blueprint('users', __name__, url_prefix='/api/users')
    
    @bp.route('', methods=['POST'])
    def create_user():
        data = request.get_json()
        
        from usecases.create_user import CreateUserRequest
        req = CreateUserRequest(data['name'], data['email'])
        response = usecase.execute(req)
        
        return jsonify({
            'id': response.id,
            'name': response.name,
            'email': response.email
        }), 201
    
    return bp

# adapters/db.py
from usecases.create_user import UserRepository
from entities.user import User
from typing import Optional

class UserRepositoryImpl(UserRepository):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def save(self, user: User) -> None:
        query = """
            INSERT INTO users (id, name, email, created_at)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute(
            query,
            (user.id, user.name, user.email, user.created_at)
        )
        self.db.commit()
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = ?"
        result = self.db.execute(query, (user_id,)).fetchone()
        
        if not result:
            return None
        
        return User(result[0], result[1], result[2])
    
    def exists_by_email(self, email: str) -> bool:
        query = "SELECT COUNT(*) FROM users WHERE email = ?"
        result = self.db.execute(query, (email,)).fetchone()
        return result[0] > 0
```

## テスト戦略

### Entity テスト（フレームワーク不要）

```java
public class UserTest {
    
    @Test
    public void testValidUserCreation() {
        User user = new User("1", "John", "john@example.com");
        
        assertEquals("1", user.getId());
        assertEquals("John", user.getName());
    }
    
    @Test
    public void testInvalidEmail() {
        assertThrows(DomainException.class, () -> {
            new User("1", "John", "invalid-email");
        });
    }
    
    @Test
    public void testChangeEmail() {
        User user = new User("1", "John", "john@example.com");
        user.changeEmail("newemail@example.com");
        
        assertEquals("newemail@example.com", user.getEmail());
    }
}
```

### Use Case テスト

```java
public class CreateUserUseCaseTest {
    
    private CreateUserUseCase useCase;
    private UserRepository mockRepository;
    private UserPresenter mockPresenter;
    
    @Before
    public void setup() {
        mockRepository = mock(UserRepository.class);
        mockPresenter = mock(UserPresenter.class);
        useCase = new CreateUserUseCase(mockRepository, mockPresenter);
    }
    
    @Test
    public void testCreateUserSuccess() {
        // Arrange
        when(mockRepository.existsByEmail("john@example.com"))
            .thenReturn(false);
        
        CreateUserRequest request = 
            new CreateUserRequest("John", "john@example.com");
        
        // Act
        CreateUserResponse response = useCase.execute(request);
        
        // Assert
        assertNotNull(response.getId());
        assertEquals("John", response.getName());
        verify(mockRepository).save(any(User.class));
    }
    
    @Test
    public void testEmailAlreadyExists() {
        // Arrange
        when(mockRepository.existsByEmail("john@example.com"))
            .thenReturn(true);
        
        CreateUserRequest request = 
            new CreateUserRequest("John", "john@example.com");
        
        // Act & Assert
        assertThrows(UseCaseException.class, () -> {
            useCase.execute(request);
        });
    }
}
```

## 依存性逆転の原則

### 正しい依存関係

```
Frameworks層
    ↑ 依存
Adapters層
    ↑ 依存
Use Cases層
    ↑ 依存
Entities層

重要：
✅ 各層は下位層のみに依存
✅ 上位層への依存はない
✅ インターフェースを通じた依存
❌ 直接的な参照は避ける
```

### 悪い例 vs 良い例

```java
// ❌ Bad：直接依存（フレームワーク依存）
public class UserService {
    private UserJpaRepository repository; // Frameworks層に依存
    
    public void createUser(String name, String email) {
        UserEntity entity = new UserEntity(name, email);
        repository.save(entity);
    }
}

// ✅ Good：インターフェース依存（依存性逆転）
public class CreateUserUseCase {
    private UserRepository repository; // Use Cases層のインターフェース
    
    public CreateUserResponse execute(CreateUserRequest request) {
        User user = new User(...);
        repository.save(user); // Use Cases層で定義
    }
}
```

## メリットとデメリット

### メリット

| メリット | 説明 |
|---------|------|
| **テスト容易性** | ビジネスロジックはフレームワーク無しでテスト可能 |
| **フレームワーク非依存** | DB、Web フレームワークを自由に変更可能 |
| **ビジネスロジック中心** | ビジネス要件に集中できる |
| **明確な責務分離** | 各層の役割が明確 |
| **長期メンテナンス** | コード理解が容易で、修正が低リスク |
| **拡張性** | 新機能追加が容易 |

### デメリット

| デメリット | 説明 |
|----------|------|
| **複雑性が高い** | 初心者には理解困難 |
| **初期開発コストが高い** | インターフェース・実装が多い |
| **過度な設計の可能性** | 小規模プロジェクトでは過剰 |
| **チーム全体の理解が必要** | チームメンバーの習熟度が重要 |
| **パフォーマンスオーバーヘッド** | 層が多いため若干のオーバーヘッド |

## 適用ガイドライン

### クリーンアーキテクチャを選ぶべき場合

```
✅ 複雑なビジネスロジック
✅ 長期的なメンテナンスが必要
✅ チーム開発が必要
✅ テスト自動化が重要
✅ フレームワーク非依存が必要
✅ スケーラブルなアーキテクチャが必要
```

### 避けるべき場合

```
❌ 小規模なプロトタイプ
❌ CRUD アプリケーションのみ
❌ 初心者チーム
❌ 短期プロジェクト
❌ リソース限定的
```

## [[ヘキサゴナルアーキテクチャ]]との違い

| 観点 | ヘキサゴナル | クリーン |
|-----|-----------|--------|
| **焦点** | ポート&アダプター | 層と依存方向 |
| **構造** | 6角形モデル | 同心円状 |
| **複雑性** | 中程度 | やや高い |
| **テスト** | 高度 | 非常に高い |
| **フレームワーク非依存** | ○ | ○ |

## [[MVC]]、[[MVP]]、[[MVVM]]との比較

クリーンアーキテクチャは、上位階の MVC/MVP/MVVM と並行して使用できます：

```
クリーンアーキテクチャの層
    ↓
Interface Adapters層
    ↓
MVC/MVP/MVVM パターン
    ↓
Presentation 実装
```

## まとめ

クリーンアーキテクチャは、**エンタープライズレベルの複雑なアプリケーション向けのアーキテクチャパターン**です。ビジネスロジックをフレームワークから完全に分離し、テスト容易性とメンテナンス性を最大化します。

学習曲線は陡しいですが、習得すれば非常に強力なツールになります。
