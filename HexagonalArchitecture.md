# ヘキサゴナルアーキテクチャ

## 概要

### ヘキサゴナルアーキテクチャとは

ヘキサゴナルアーキテクチャ（Hexagonal Architecture、別称：Ports & Adapters パターン）は、Alistair Cockburn によって提唱されたアーキテクチャパターンです。アプリケーションの**ビジネスロジックを外部依存から完全に隔離**することを目指します。

**ビジネスロジックが中心**であり、その周囲に複数のポート（インターフェース）とアダプター（実装）を配置する設計です。

### 特徴

- **ビジネスロジックの独立性**：フレームワークやライブラリに依存しない
- **多方向のI/O**：複数の入力・出力ポイント（Web、CLI、イベント等）に対応
- **テスト容易性**：モック・スタブを使ったテストが容易
- **フレームワーク非依存**：フレームワークの変更に強い
- **ポート&アダプター**：インターフェースと実装の分離

## アーキテクチャの構造

### 基本的な6角形構造

```
                    WEB UI
                      │
        ┌─────────────┼─────────────┐
        │             │             │
      Port1          Port2          Port3
        │             │             │
        ▼             ▼             ▼
    ┌───────────────────────────────────┐
    │                                   │
    │    ビジネスロジック層             │  (6角形の中心)
    │   (Domain / Application Core)      │
    │                                   │
    └───────────────────────────────────┘
        ▲             ▲             ▲
        │             │             │
      Adapter1      Adapter2      Adapter3
        │             │             │
        └─────────────┼─────────────┘
                      │
              ┌───────┴────────┐
              │                │
          Database          Message Queue
```

### コンポーネント

#### 1. Core（ビジネスロジック層）

```
責務：
- ビジネスルール実装
- ドメインモデル
- ユースケース実装
- 外部依存なし
```

#### 2. Port（ポート）

```
定義：
- インターフェース定義
- 外部システムとの通信規約
- 実装に依存しない契約

種類：
- Input Port: UI、API からの入力受付
- Output Port: DB、外部API への出力
```

#### 3. Adapter（アダプター）

```
実装：
- Port の具体的な実装
- フレームワーク・ライブラリ依存性はここのみ
- 交換可能な実装

例：
- REST API アダプター
- データベースアダプター
- メッセージキューアダプター
```

## 実装パターン

### Java での ヘキサゴナルアーキテクチャ

#### プロジェクト構造

```
src/
├── domain/
│   ├── model/
│   │   ├── User.java
│   │   └── Order.java
│   └── repository/
│       └── UserPort.java
├── application/
│   ├── usecase/
│   │   └── CreateUserUseCase.java
│   ├── service/
│   │   └── UserApplicationService.java
│   └── port/
│       ├── UserRepositoryPort.java
│       └── EmailSenderPort.java
├── adapter/
│   ├── in/
│   │   ├── web/
│   │   │   └── UserController.java
│   │   └── cli/
│   │       └── UserCLI.java
│   └── out/
│       ├── persistence/
│       │   └── UserJpaAdapter.java
│       └── notification/
│           └── EmailAdapter.java
└── config/
    └── AdapterConfig.java
```

#### Core：ドメインモデル

```java
// domain/model/User.java
public class User {
    private String id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    
    public User(String id, String name, String email) {
        if (id == null || id.isEmpty()) {
            throw new IllegalArgumentException("ID cannot be empty");
        }
        if (name == null || name.isEmpty()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        if (!isValidEmail(email)) {
            throw new IllegalArgumentException("Invalid email");
        }
        
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdAt = LocalDateTime.now();
    }
    
    private static boolean isValidEmail(String email) {
        return email != null && email.contains("@");
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
```

#### Core：Output Port（出力ポート）

```java
// application/port/UserRepositoryPort.java
public interface UserRepositoryPort {
    void save(User user);
    User findById(String id);
    boolean existsByEmail(String email);
}

// application/port/EmailSenderPort.java
public interface EmailSenderPort {
    void sendWelcomeEmail(String email, String name);
}
```

#### Core：Input Port（入力ポート）

```java
// application/port/CreateUserInputPort.java
public interface CreateUserInputPort {
    UserResponse createUser(CreateUserRequest request);
}

// Request/Response は Layer で定義
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

public class UserResponse {
    private String id;
    private String name;
    private String email;
    
    public UserResponse(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}
```

#### Core：Usecase / Application Service

```java
// application/service/UserApplicationService.java
@Service
public class UserApplicationService implements CreateUserInputPort {
    
    private final UserRepositoryPort userRepository;
    private final EmailSenderPort emailSender;
    
    @Autowired
    public UserApplicationService(
        UserRepositoryPort userRepository,
        EmailSenderPort emailSender) {
        this.userRepository = userRepository;
        this.emailSender = emailSender;
    }
    
    @Override
    @Transactional
    public UserResponse createUser(CreateUserRequest request) {
        // 1. バリデーション（ビジネスロジック）
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException(
                "Email already registered");
        }
        
        // 2. ユーザー作成
        String userId = generateUserId();
        User user = new User(
            userId,
            request.getName(),
            request.getEmail()
        );
        
        // 3. リポジトリに保存（Port経由）
        userRepository.save(user);
        
        // 4. メール送信（Port経由）
        emailSender.sendWelcomeEmail(
            user.getEmail(),
            user.getName()
        );
        
        // 5. レスポンス返却
        return new UserResponse(
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

#### Adapter In：REST Controller

```java
// adapter/in/web/UserController.java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    private final CreateUserInputPort createUserUseCase;
    
    @Autowired
    public UserController(CreateUserInputPort createUserUseCase) {
        this.createUserUseCase = createUserUseCase;
    }
    
    @PostMapping
    public ResponseEntity<UserResponse> createUser(
        @RequestBody CreateUserRequest request) {
        
        UserResponse response = createUserUseCase.createUser(request);
        
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(response);
    }
}
```

#### Adapter Out：Database Adapter

```java
// adapter/out/persistence/UserJpaAdapter.java
@Component
public class UserJpaAdapter implements UserRepositoryPort {
    
    private final UserJpaRepository jpaRepository;
    
    @Autowired
    public UserJpaAdapter(UserJpaRepository jpaRepository) {
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

// JPA Repository（フレームワーク固有）
@Repository
public interface UserJpaRepository
    extends JpaRepository<UserEntity, String> {
    boolean existsByEmail(String email);
}

// JPA Entity
@Entity
@Table(name = "users")
public class UserEntity {
    @Id
    private String id;
    private String name;
    private String email;
    private LocalDateTime createdAt;
    
    // Getter/Setter
}
```

#### Adapter Out：Email Sender Adapter

```java
// adapter/out/notification/EmailAdapter.java
@Component
public class EmailAdapter implements EmailSenderPort {
    
    private final JavaMailSender mailSender;
    
    @Autowired
    public EmailAdapter(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }
    
    @Override
    public void sendWelcomeEmail(String email, String name) {
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(email);
            message.setSubject("Welcome to Our Service");
            message.setText("Hello " + name + 
                ", welcome to our service!");
            
            mailSender.send(message);
        } catch (Exception e) {
            throw new EmailSendingException(
                "Failed to send email", e);
        }
    }
}
```

### Python での 実装例

```python
# domain/models.py
from datetime import datetime
from typing import Optional

class User:
    def __init__(self, user_id: str, name: str, email: str):
        if not user_id or not name:
            raise ValueError("ID and Name are required")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        
        self.id = user_id
        self.name = name
        self.email = email
        self.created_at = datetime.now()
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        return "@" in email

# application/ports.py
from abc import ABC, abstractmethod
from domain.models import User

class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

class EmailSenderPort(ABC):
    @abstractmethod
    def send_welcome_email(self, email: str, name: str) -> None:
        pass

# application/service.py
from domain.models import User
from application.ports import UserRepositoryPort, EmailSenderPort
import uuid

class UserApplicationService:
    def __init__(self, 
                 repository: UserRepositoryPort,
                 email_sender: EmailSenderPort):
        self.repository = repository
        self.email_sender = email_sender
    
    def create_user(self, name: str, email: str) -> dict:
        # バリデーション
        if self.repository.exists_by_email(email):
            raise Exception("Email already registered")
        
        # ユーザー作成
        user_id = str(uuid.uuid4())
        user = User(user_id, name, email)
        
        # 保存
        self.repository.save(user)
        
        # メール送信
        self.email_sender.send_welcome_email(email, name)
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

# adapter/in/web.py
from flask import Blueprint, request, jsonify
from application.service import UserApplicationService

def create_user_routes(service: UserApplicationService):
    bp = Blueprint('users', __name__, url_prefix='/api/users')
    
    @bp.route('', methods=['POST'])
    def create_user():
        data = request.get_json()
        result = service.create_user(
            name=data['name'],
            email=data['email']
        )
        return jsonify(result), 201
    
    return bp

# adapter/out/persistence.py
from application.ports import UserRepositoryPort
from domain.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

class UserDatabaseAdapter(UserRepositoryPort):
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, user: User) -> None:
        # SQL実行
        query = """
            INSERT INTO users (id, name, email, created_at)
            VALUES (?, ?, ?, ?)
        """
        self.session.execute(
            query,
            (user.id, user.name, user.email, user.created_at)
        )
        self.session.commit()
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = ?"
        result = self.session.execute(query, (user_id,)).fetchone()
        return result

# adapter/out/email.py
from application.ports import EmailSenderPort
import smtplib

class EmailAdapter(EmailSenderPort):
    def __init__(self, smtp_host: str, smtp_port: int):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
    
    def send_welcome_email(self, email: str, name: str) -> None:
        message = f"Hello {name}, welcome!"
        # メール送信処理
        pass
```

## メリットとデメリット

### メリット

| メリット | 説明 |
|---------|------|
| **完全なテスト容易性** | Core がフレームワーク非依存で、モックが容易 |
| **フレームワーク非依存** | Rails → Django への切り替えも可能 |
| **複数の入出力に対応** | Web、CLI、イベント等を同時実装 |
| **ビジネスロジックに集中** | Core がビジネスに専念できる |
| **アダプター交換が容易** | DB、メール等を簡単に切り替え |
| **エンタープライズレベル** | 複雑なドメインロジックに対応 |

### デメリット

| デメリット | 説明 |
|----------|------|
| **学習曲線が陡しい** | ポート・アダプター概念が複雑 |
| **初期実装コストが高い** | テンプレートコードが増える |
| **過度な設計の可能性** | 小規模アプリでは過設計になる |
| **チーム全体の理解が必要** | 理解していないメンバーで問題発生 |
| **ファイル数が増加** | インターフェース・実装が多くなる |
| **パフォーマンスオーバーヘッド** | 抽象化レイヤーが増える |

## テスト戦略

### Core のテスト（フレームワーク不要）

```java
// test/domain/UserTest.java
public class UserTest {
    
    @Test
    public void testUserCreation() {
        User user = new User("1", "John", "john@example.com");
        
        assertEquals("1", user.getId());
        assertEquals("John", user.getName());
    }
    
    @Test
    public void testInvalidEmail() {
        assertThrows(IllegalArgumentException.class, () -> {
            new User("1", "John", "invalid-email");
        });
    }
}

// test/application/UserApplicationServiceTest.java
public class UserApplicationServiceTest {
    
    private UserApplicationService service;
    private UserRepositoryPort repository;
    private EmailSenderPort emailSender;
    
    @Before
    public void setup() {
        // モック作成
        repository = mock(UserRepositoryPort.class);
        emailSender = mock(EmailSenderPort.class);
        
        service = new UserApplicationService(repository, emailSender);
    }
    
    @Test
    public void testCreateUser() {
        // Arrange
        when(repository.existsByEmail("john@example.com"))
            .thenReturn(false);
        
        // Act
        UserResponse response = service.createUser(
            new CreateUserRequest("John", "john@example.com"));
        
        // Assert
        assertNotNull(response.getId());
        assertEquals("John", response.getName());
        
        // モックの呼び出し確認
        verify(emailSender, times(1))
            .sendWelcomeEmail(anyString(), anyString());
    }
}
```

## 適用ガイドライン

### ヘキサゴナルアーキテクチャを選ぶべき場合

```
✅ 複雑なビジネスロジック
✅ 長期メンテナンスが必要
✅ テスト自動化が重要
✅ フレームワーク非依存が必要
✅ エンタープライズアプリケーション
✅ マイクロサービス化の可能性がある
```

### 避けるべき場合

```
❌ 小規模なCRUDアプリケーション
❌ 初心者チーム
❌ 短期プロジェクト
❌ シンプルなロジック
❌ リソースが限定的
```

## [[クリーンアーキテクチャ]]との関係

ヘキサゴナルアーキテクチャは、[[クリーンアーキテクチャ]]の基礎概念となっており、両者は非常に類似しています。主な違いは：

- **ヘキサゴナル**：ポート&アダプターパターンに焦点
- **クリーン**：層の分離と依存方向に焦点

## まとめ

ヘキサゴナルアーキテクチャは、**ビジネスロジックをフレームワークから完全に独立させる**アーキテクチャです。複雑なドメインロジックを持つエンタープライズアプリケーションに最適です。

学習コストはありますが、テスト容易性とメンテナンス性が大幅に向上します。
