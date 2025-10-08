# Architecture Documentation - User Admin Module

## BCE Architecture Pattern

This implementation follows the **Boundary-Control-Entity** (BCE) pattern, which is a variation of MVC specifically designed for use case-driven development.

```
┌─────────────────────────────────────────────────────────────────────┐
│                              USER                                    │
│                         (User Admin)                                 │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ Interacts with
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      BOUNDARY LAYER (B)                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │         UserAdminBoundary (CLI Interface)                   │    │
│  │  - Display menus                                            │    │
│  │  - Capture user input                                       │    │
│  │  - Display results                                          │    │
│  │  - No business logic                                        │    │
│  └────────────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ Calls methods
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      CONTROL LAYER (C)                               │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────┐ │
│  │ Authentication       │  │ UserAccount          │  │ UserProfile│ │
│  │ Controller           │  │ Controller           │  │ Controller │ │
│  │                      │  │                      │  │            │ │
│  │ - login()            │  │ - create_user_       │  │ - create_  │ │
│  │ - logout()           │  │   account()          │  │   user_    │ │
│  │ - validate           │  │ - view_user_         │  │   profile()│ │
│  │   credentials        │  │   account()          │  │ - view_    │ │
│  │ - manage session     │  │ - update_user_       │  │   user_    │ │
│  │                      │  │   account()          │  │   profile()│ │
│  │                      │  │ - suspend_user_      │  │ - update_  │ │
│  │                      │  │   account()          │  │   user_    │ │
│  │                      │  │ - search_user_       │  │   profile()│ │
│  │                      │  │   accounts()         │  │ - suspend_ │ │
│  │                      │  │                      │  │   user_    │ │
│  │                      │  │                      │  │   profile()│ │
│  │                      │  │                      │  │ - search_  │ │
│  │                      │  │                      │  │   user_    │ │
│  │                      │  │                      │  │   profiles()│ │
│  └──────────────────────┘  └──────────────────────┘  └──────────┘ │
│                                                                       │
│  Business Logic:                                                     │
│  - Validation                                                        │
│  - Data processing                                                   │
│  - Error handling                                                    │
│  - Coordination between Boundary and Entity                          │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ CRUD operations
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ENTITY LAYER (E)                                │
│  ┌──────────────────────┐         ┌──────────────────────┐         │
│  │   UserAccount        │         │   UserProfile        │         │
│  │   (Entity)           │─────────│   (Entity)           │         │
│  │                      │ n:1     │                      │         │
│  │ Attributes:          │         │ Attributes:          │         │
│  │ - id                 │         │ - id                 │         │
│  │ - username           │         │ - profile_name       │         │
│  │ - email              │         │ - description        │         │
│  │ - password_hash      │         │ - is_active          │         │
│  │ - first_name         │         │                      │         │
│  │ - last_name          │         │                      │         │
│  │ - phone_number       │         │                      │         │
│  │ - user_profile_id (FK)│        │                      │         │
│  │ - is_active          │         │                      │         │
│  │ - created_at         │         │                      │         │
│  │ - updated_at         │         │                      │         │
│  └──────────────────────┘         └──────────────────────┘         │
│                                                                       │
│  Data Models (ORM):                                                  │
│  - Pure data structure                                               │
│  - No business logic                                                 │
│  - Database mapping                                                  │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            │ SQLAlchemy ORM
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE (SQLite)                                 │
│  ┌────────────────────┐         ┌────────────────────┐             │
│  │  user_accounts     │         │  user_profiles     │             │
│  │  table             │         │  table             │             │
│  └────────────────────┘         └────────────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

## Sequence Diagram Example: Create User Account

```
User Admin          UserAdminBoundary      UserAccountController    UserAccount    Database
    │                       │                       │                   │            │
    │ Choose option 3       │                       │                   │            │
    │──────────────────────>│                       │                   │            │
    │                       │                       │                   │            │
    │                       │ get_active_user_     │                   │            │
    │                       │ profiles()            │                   │            │
    │                       │──────────────────────>│                   │            │
    │                       │                       │                   │            │
    │                       │ <List of profiles>    │                   │            │
    │                       │<──────────────────────│                   │            │
    │                       │                       │                   │            │
    │ <Display profiles>    │                       │                   │            │
    │<──────────────────────│                       │                   │            │
    │                       │                       │                   │            │
    │ Enter user details    │                       │                   │            │
    │──────────────────────>│                       │                   │            │
    │                       │                       │                   │            │
    │                       │ create_user_account() │                   │            │
    │                       │──────────────────────>│                   │            │
    │                       │                       │                   │            │
    │                       │                       │ Validate data     │            │
    │                       │                       │ Hash password     │            │
    │                       │                       │                   │            │
    │                       │                       │ new UserAccount() │            │
    │                       │                       │──────────────────>│            │
    │                       │                       │                   │            │
    │                       │                       │ session.add()     │            │
    │                       │                       │──────────────────────────────>│
    │                       │                       │                   │            │
    │                       │                       │ session.commit()  │            │
    │                       │                       │──────────────────────────────>│
    │                       │                       │                   │            │
    │                       │ (success, msg, user)  │                   │            │
    │                       │<──────────────────────│                   │            │
    │                       │                       │                   │            │
    │ Display success       │                       │                   │            │
    │<──────────────────────│                       │                   │            │
    │                       │                       │                   │            │
```

## Class Relationships

```
┌──────────────────────┐
│   UserProfile        │
│  (Entity Class)      │
│                      │
│ + id: int            │
│ + profile_name: str  │
│ + description: str   │
│ + is_active: bool    │
└──────────────────────┘
          ▲
          │ 1
          │
          │ has
          │
          │ n
┌──────────────────────┐
│   UserAccount        │
│  (Entity Class)      │
│                      │
│ + id: int            │
│ + username: str      │
│ + email: str         │
│ + password_hash: str │
│ + first_name: str    │
│ + last_name: str     │
│ + phone_number: str  │
│ + user_profile_id: FK│
│ + is_active: bool    │
│ + created_at: date   │
│ + updated_at: date   │
└──────────────────────┘
```

## Method Flow Examples

### User Story 1: Login

```
1. User enters username and password
   └─> UserAdminBoundary.handle_login()
       └─> AuthenticationController.login(username, password)
           ├─> Query UserAccount by username
           ├─> Check if account exists
           ├─> Verify account is not suspended
           ├─> Verify password with bcrypt
           ├─> Check if profile is active
           └─> Return (success, message, user)
```

### User Story 3: Create User Account

```
1. User selects "Create User Account"
   └─> UserAdminBoundary.handle_create_user_account()
       ├─> UserProfileController.get_active_user_profiles()
       │   └─> Display available profiles
       ├─> Collect user input (username, email, etc.)
       └─> UserAccountController.create_user_account(...)
           ├─> Validate profile exists and is active
           ├─> Check username uniqueness
           ├─> Check email uniqueness
           ├─> Hash password with bcrypt
           ├─> Create UserAccount entity
           ├─> session.add(user)
           ├─> session.commit()
           └─> Return (success, message, user)
```

### User Story 7: Search Users

```
1. User selects "Search User Accounts"
   └─> UserAdminBoundary.handle_search_user_accounts()
       ├─> Collect search criteria (keyword, profile, status)
       └─> UserAccountController.search_user_accounts(...)
           ├─> Build query with filters
           │   ├─> Keyword: LIKE search on username/email/name
           │   ├─> Profile: Filter by user_profile_id
           │   └─> Status: Filter by is_active
           ├─> Execute query
           └─> Return (success, message, list_of_users)
```

## Key Design Decisions

### 1. Password Security
- Passwords are **hashed** using bcrypt (never stored in plain text)
- Salt is automatically generated by bcrypt
- Password verification uses constant-time comparison

### 2. Status Management
- Soft delete approach (is_active flag)
- Suspended accounts remain in database but cannot login
- Suspended profiles cannot be assigned to new users

### 3. Timestamps
- Automatic created_at on insert
- Automatic updated_at on update (SQLAlchemy handles this)

### 4. Validation
- Controllers handle all business logic and validation
- Entities are pure data models
- Boundaries are pure interface (no validation)

### 5. Error Handling
- Controllers return tuples: (success: bool, message: str, data: object)
- Consistent error messages for user feedback
- Database rollback on errors

### 6. Search Functionality
- Case-insensitive search (LIKE with %)
- Multiple field search (username, email, name)
- Combinable filters (keyword + profile + status)

## Database Schema

```sql
-- User Profiles Table
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1
);

-- User Accounts Table
CREATE TABLE user_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20),
    user_profile_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_profile_id) REFERENCES user_profiles(id)
);
```

## File Organization Rationale

### Why separate packages?
- **Separation of Concerns**: Each layer has a distinct responsibility
- **Maintainability**: Easy to find and modify specific functionality
- **Testability**: Can test each layer independently
- **Scalability**: Easy to add new entities, controllers, or boundaries

### Why this naming convention?
- **Descriptive**: Names clearly indicate purpose
- **Consistent**: All files follow the same pattern
- **Professional**: Standard Python package structure

## For Your Documentation

Use this implementation to create:

1. **Use Case Diagram**: Extract use cases from boundary methods
2. **Class Diagram**: Extract from entity classes
3. **Sequence Diagrams**: Follow method calls in this document
4. **BCE Diagram**: Use the ASCII diagrams above
5. **Database Schema**: Use the SQL schema above
6. **Wireframes**: Base on CLI screens in boundary class

