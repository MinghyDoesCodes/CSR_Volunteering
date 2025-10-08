# Web Application Setup Guide

## 🌐 CSR Volunteering Web Portal

This is a **Flask web application** that runs on localhost. Access it through your web browser!

---

## ⚡ Quick Start

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Initialize Database

```powershell
python -m database.init_db
```

You should see:
```
✓ User profiles created successfully
✓ Default admin account created
  Username: admin
  Password: admin123
```

### Step 3: Run the Web Server

```powershell
python app.py
```

You should see:
```
============================================================
CSR VOLUNTEERING SYSTEM - WEB PORTAL
============================================================

Server starting...
Access the portal at: http://localhost:5000

Default admin credentials:
  Username: admin
  Password: admin123

Press CTRL+C to stop the server
============================================================
```

### Step 4: Open Your Browser

Go to: **http://localhost:5000**

---

## 🎯 Testing the Application

### 1. **Homepage**
- Visit http://localhost:5000
- You'll see the welcome page with login button

### 2. **Login**
- Click "Login to Portal"
- Use credentials:
  - Username: `admin`
  - Password: `admin123`

### 3. **Dashboard**
- After login, you'll see the User Admin dashboard
- Quick access to all features

### 4. **Create User Account**
- Click "➕ Create User Account"
- Fill in the form:
  - Username: `john_doe`
  - Email: `john@example.com`
  - Password: `password123`
  - First Name: `John`
  - Last Name: `Doe`
  - Profile: Select "CSR Rep"
- Click "Create Account"

### 5. **View User Accounts**
- Click "User Accounts" in navigation
- See table of all users
- Click "View" to see details
- Click "Edit" to modify

### 6. **Search Users**
- Click "🔍 Search" button
- Try searching by keyword: `john`
- Filter by profile: `CSR Rep`
- Filter by status: `Active`

### 7. **Manage User Profiles**
- Click "User Profiles" in navigation
- View, Create, Edit, or Search profiles

### 8. **Suspend/Activate**
- View any user account
- Click "🚫 Suspend" button
- User status changes to "Suspended"
- Click "✅ Activate" to reactivate

---

## 📱 Web Pages Available

### Public Pages
- `/` - Homepage
- `/login` - Login page

### Protected Pages (Requires Login)
- `/dashboard` - User dashboard
- `/logout` - Logout

### User Admin Pages (Requires User Admin Role)

**User Accounts:**
- `/user-accounts` - List all accounts
- `/user-accounts/create` - Create new account
- `/user-accounts/<id>` - View account details
- `/user-accounts/<id>/edit` - Edit account
- `/user-accounts/<id>/suspend` - Suspend account
- `/user-accounts/<id>/activate` - Activate account
- `/user-accounts/search` - Search accounts

**User Profiles:**
- `/user-profiles` - List all profiles
- `/user-profiles/create` - Create new profile
- `/user-profiles/<id>` - View profile details
- `/user-profiles/<id>/edit` - Edit profile
- `/user-profiles/<id>/suspend` - Suspend profile
- `/user-profiles/<id>/activate` - Activate profile
- `/user-profiles/search` - Search profiles

---

## 🎨 Features Implemented

### ✅ User Interface
- Modern, clean design
- Responsive (works on mobile, tablet, desktop)
- Navigation menu with current user info
- Flash messages for success/error feedback
- Form validation
- Tables with search and filter
- Action buttons (View, Edit, Suspend, etc.)

### ✅ Security
- Login required for protected pages
- Role-based access control (User Admin only)
- Password hashing (bcrypt)
- Session management
- CSRF protection (Flask built-in)

### ✅ User Experience
- Clear page headers
- Breadcrumb navigation (Back buttons)
- Confirmation dialogs for dangerous actions
- Status badges (Active/Suspended)
- Hover effects on cards and buttons
- Success/Error alerts

### ✅ All 12 User Stories
1. ✅ Login
2. ✅ Logout
3. ✅ Create User Account
4. ✅ View User Account
5. ✅ Update User Account
6. ✅ Suspend User Account
7. ✅ Search User Accounts
8. ✅ Create User Profile
9. ✅ View User Profile
10. ✅ Update User Profile
11. ✅ Suspend User Profile
12. ✅ Search User Profiles

---

## 🛠️ Troubleshooting

### Issue: Port 5000 already in use

**Solution:** Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to 5001
```

### Issue: Database not found

**Solution:** Run the init script:
```powershell
python -m database.init_db
```

### Issue: Can't access from other devices

**Solution:** The server runs on `0.0.0.0` so it's accessible on your network.
Find your IP address:
```powershell
ipconfig
```
Then access from another device: `http://YOUR_IP:5000`

### Issue: CSS not loading

**Solution:** Hard refresh your browser:
- Windows: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

---

## 📂 Project Structure

```
CSR_Volunteering/
├── app.py                    ← Main Flask application (RUN THIS!)
├── requirements.txt          ← Dependencies
├── database/                 ← Database layer
├── entities/                 ← Entity models (E)
├── controllers/              ← Business logic (C)
├── boundaries/               ← OLD CLI (not used)
├── templates/                ← HTML templates (B)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── user_accounts/
│   │   ├── list.html
│   │   ├── create.html
│   │   ├── view.html
│   │   ├── edit.html
│   │   └── search.html
│   └── user_profiles/
│       ├── list.html
│       ├── create.html
│       ├── view.html
│       ├── edit.html
│       └── search.html
└── static/                   ← Static files
    └── css/
        └── style.css         ← Styles
```

---

## 🎓 For Academic Submission

### Design Artifacts (Now Based on Web App!)

**1. Use Case Diagrams**
- Actor: User Admin
- System: CSR Volunteering Web Portal
- Use Cases: All 12 user stories

**2. Wireframes**
- Extract from HTML templates
- Each page is a wireframe:
  - Login page → `templates/login.html`
  - Dashboard → `templates/dashboard.html`
  - User list → `templates/user_accounts/list.html`
  - Create form → `templates/user_accounts/create.html`
  - Etc.

**3. Sequence Diagrams**
- Follow HTTP request flow:
  1. User → Browser → Flask Route → Controller → Entity → Database
  2. Database → Entity → Controller → Flask → Template → Browser → User

**4. BCE Architecture**
- **Boundary**: Flask routes + HTML templates (`app.py` + `templates/`)
- **Control**: Controller classes (`controllers/`)
- **Entity**: ORM models (`entities/`)

**5. Screenshots**
- Take screenshots of every page
- Show in your report as evidence
- Demonstrate all functionality

---

## 📸 Expected Screenshots

### For Your Report

1. **Homepage** (index page)
2. **Login page** (with credentials entered)
3. **Dashboard** (after login)
4. **User Accounts List** (table view)
5. **Create User Account** (form filled)
6. **View User Account** (detail page)
7. **Edit User Account** (form with existing data)
8. **Search User Accounts** (with results)
9. **User Profiles List** (table view)
10. **Create User Profile** (form)
11. **View User Profile** (detail page)
12. **Suspend Account** (showing status change)

---

## 🚀 Next Steps

### 1. Test Everything
- Go through each page
- Test all buttons
- Try to break it (error handling)
- Take screenshots

### 2. Create Design Documents
- Use pages as wireframes
- Extract sequence diagrams from routes
- Document the BCE separation

### 3. Implement Other Modules
- Platform Manager pages
- CSR Rep pages
- PIN pages

### 4. Add Unit Tests
- Test controllers
- Test routes
- Test entities

### 5. Setup CI/CD
- GitHub Actions
- Automated testing
- Deployment

---

## 💡 Tips

### Development Mode
- Flask runs in **debug mode** (auto-reload on code changes)
- Error pages show detailed traceback
- Change `debug=False` for production

### Adding New Pages
1. Create route in `app.py`
2. Create HTML template in `templates/`
3. Use existing templates as reference

### Styling
- Modify `static/css/style.css` for custom styles
- Use existing CSS classes
- Mobile-responsive by default

---

## ✅ Verification Checklist

Before submission:

- [ ] All 12 user stories work on web interface
- [ ] Can login/logout
- [ ] Can create/view/update user accounts
- [ ] Can suspend/activate accounts
- [ ] Can search and filter users
- [ ] Can manage user profiles
- [ ] All pages have proper styling
- [ ] Navigation works correctly
- [ ] Flash messages appear
- [ ] Forms validate input
- [ ] Screenshots taken for report
- [ ] BCE architecture documented

---

## 🎉 Success!

You now have a fully functional web application!

Access at: **http://localhost:5000**

Login: `admin` / `admin123`

Enjoy! 🚀

