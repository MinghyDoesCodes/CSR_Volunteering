"""
Database Initialization Script
Run this to create the database and seed initial data
"""

from database.db_config import init_database, get_session
from entities.user_profile import UserProfile
from entities.user_account import UserAccount
import bcrypt


def seed_initial_data():
    """
    Seed the database with initial data
    - Default user profiles (roles)
    - Default admin account
    """
    session = get_session()
    
    try:
        # Create default user profiles (roles)
        profiles = [
            UserProfile(
                profile_name="User Admin",
                description="Administrator who manages user accounts and profiles",
                is_active=True
            ),
            UserProfile(
                profile_name="Platform Manager",
                description="Manages categories and generates reports",
                is_active=True
            ),
            UserProfile(
                profile_name="CSR Rep",
                description="Corporate Social Responsibility Representative",
                is_active=True
            ),
            UserProfile(
                profile_name="PIN",
                description="Person-In-Need who requests assistance",
                is_active=True
            )
        ]
        
        # Add profiles to database
        for profile in profiles:
            session.add(profile)
        
        session.commit()
        print("✓ User profiles created successfully")
        
        # Create default admin account
        # Hash the password for security
        hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        
        admin_account = UserAccount(
            username="admin",
            email="admin@csrvolunteering.com",
            password_hash=hashed_password.decode('utf-8'),
            first_name="System",
            last_name="Administrator",
            user_profile_id=1,  # User Admin profile
            is_active=True
        )
        
        session.add(admin_account)
        session.commit()
        print("✓ Default admin account created")
        print("  Username: admin")
        print("  Password: admin123")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error seeding data: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    print("\nSeeding initial data...")
    seed_initial_data()
    print("\nDatabase setup complete!")