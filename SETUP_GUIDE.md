# Setup Guide for User Admin Module

## Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

This installs:
- **SQLAlchemy** (ORM for database)
- **bcrypt** (Password hashing for security)

## Step 2: Initialize Database

Create the database and seed initial data:

```powershell
python -m database.init_db
```

This creates:
- `csr_volunteering.db` file
- 4 default user profiles (User Admin, Platform Manager, CSR Rep, PIN)
- 1 default admin account:
  - Username: `admin`
  - Password: `admin123`

## Step 3: Run the Application

```powershell
python main.py
```

## Testing the System

### Quick Test Flow:

1. **Login as admin**
   - Username: admin
   - Password: admin123

2. **Create a new user profile** (Option 9)
   - Example: "Volunteer Coordinator"

3. **Create a new user account** (Option 3)
   - Assign the new profile

4. **Search for users** (Option 7)
   - Test keyword search

5. **View user details** (Option 4)

6. **Update user info** (Option 5)

7. **Suspend a user** (Option 6)

8. **Logout** (Option 2)

## Extracting Design Artifacts

Now that the code is implemented, you can create your design documents:

### 1. Use Case Descriptions
- Read the docstrings in controller methods
- Each method has comments linking to user stories

### 2. Use Case Diagram
- Actor: User Admin
- System: CSR Volunteering System
- Use cases: All 12 operations (login, logout, create account, etc.)

### 3. BCE Diagram
- **Entities**: `UserAccount`, `UserProfile` (in `entities/`)
- **Controls**: `AuthenticationController`, `UserAccountController`, `UserProfileController` (in `controllers/`)
- **Boundaries**: `UserAdminBoundary` (in `boundaries/`)

### 4. Sequence Diagrams
- Follow the method calls from Boundary → Controller → Entity
- Example for "Create User Account":
  1. User → UserAdminBoundary.handle_create_user_account()
  2. UserAdminBoundary → UserProfileController.get_active_user_profiles()
  3. UserAdminBoundary → UserAccountController.create_user_account()
  4. UserAccountController → UserAccount (create entity)
  5. UserAccountController → session.add() & commit()
  6. Return success to Boundary
  7. Boundary displays result to User

### 5. Wireframes
- Base on the CLI prompts in `user_admin_boundary.py`
- Convert CLI screens to web/mobile UI mockups
- Menu structure is already defined in the code

## Project Structure Explanation

### BCE Framework

**Entities (E)** - `entities/`
- Database models (ORM classes)
- Represent data structure
- No business logic

**Controllers (C)** - `controllers/`
- Business logic
- Validate data
- Coordinate between Boundary and Entity

**Boundaries (B)** - `boundaries/`
- User interface
- Handle user input/output
- No business logic or database access

### Database Layer
- `database/db_config.py` - SQLAlchemy configuration
- `database/init_db.py` - Initialize DB and seed data

## Common Issues & Solutions

### Issue: ModuleNotFoundError
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: Database doesn't exist
**Solution:** Run: `python -m database.init_db`

### Issue: Can't login
**Solution:** Use default credentials (admin/admin123) or check if account is suspended

## Next Steps

After User Admin is complete:
1. Implement Platform Manager module (10 user stories)
2. Implement CSR Rep module (9 user stories)
3. Implement PIN module (11 user stories)
4. Add unit tests (TDD)
5. Set up CI/CD pipeline
6. Create web frontend (optional)

