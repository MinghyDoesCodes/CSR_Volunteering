# CSR Volunteering System

A Corporate Social Responsibility (CSR) volunteering matching system that connects corporate volunteers with persons-in-need (PIN).

## 🌐 Web Portal Application

This is a **Flask web application** - access it through your browser at http://localhost:5000

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Initialize the database:**
```bash
python -m database.init_db
```

3. **Run the web server:**
```bash
python app.py
```

4. **Open your browser:**
Go to http://localhost:5000

5. **Login:**
- Username: `admin`
- Password: `admin123`

## Project Structure

This project follows the **BCE (Boundary-Control-Entity)** architectural pattern:

- **Entities**: Database models (ORM classes)
- **Controllers**: Business logic layer
- **Boundaries**: Web interface (Flask routes + HTML templates)

## User Roles

- **User Admin**: Manages user accounts and profiles
- **Platform Manager**: Manages categories and reports
- **CSR Rep**: Searches and manages volunteer opportunities
- **PIN (Person-in-Need)**: Creates and manages assistance requests

## Current Implementation Status

✅ User Admin module (12 user stories implemented)
- Authentication (login/logout)
- User Account CRUD operations
- User Profile CRUD operations
- Search functionality
- ✨ **Web interface with modern UI**

## Technology Stack

- **Language**: Python 3.x
- **Web Framework**: Flask
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Password Hashing**: bcrypt
- **Frontend**: HTML5, CSS3

## Documentation

- `WEB_SETUP_GUIDE.md` - Detailed setup and testing instructions
- `ARCHITECTURE.md` - Technical architecture
- `EXTRACTING_DESIGN_ARTIFACTS.md` - How to create UML diagrams

