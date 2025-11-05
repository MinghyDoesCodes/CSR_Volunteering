"""
Database Initialization Script
Run this to create the database and seed initial data
"""

from database.db_config import init_database, get_session
from entities.user_profile import UserProfile
from entities.user_account import UserAccount
from entities.category import Category
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
        
        # Add profiles to database (skip if they already exist)
        profiles_created = 0
        for profile in profiles:
            existing = session.query(UserProfile).filter_by(profile_name=profile.profile_name).first()
            if not existing:
                session.add(profile)
                profiles_created += 1
        
        if profiles_created > 0:
            session.commit()
            print(f"✓ {profiles_created} new user profile(s) created successfully")
        else:
            print("✓ All user profiles already exist")
        
        # Get profile IDs (they should exist now)
        admin_profile = session.query(UserProfile).filter_by(profile_name="User Admin").first()
        csr_profile = session.query(UserProfile).filter_by(profile_name="CSR Rep").first()
        pin_profile = session.query(UserProfile).filter_by(profile_name="PIN").first()
        platform_manager_profile = session.query(UserProfile).filter_by(profile_name="Platform Manager").first()
        
        # Create default admin account
        existing_admin = session.query(UserAccount).filter_by(username="admin").first()
        if not existing_admin:
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
            admin_account = UserAccount(
                username="admin",
                email="admin@csrvolunteering.com",
                password_hash=hashed_password.decode('utf-8'),
                first_name="System",
                last_name="Administrator",
                user_profile_id=admin_profile.id if admin_profile else 1,
                is_active=True
            )
            session.add(admin_account)
            session.commit()
            print("✓ Default admin account created")
            print("  Username: admin")
            print("  Password: admin123")
        else:
            print("✓ Default admin account already exists")
        
        # Create default PIN account
        existing_pin = session.query(UserAccount).filter_by(username="pin").first()
        if not existing_pin and pin_profile:
            hashed_password = bcrypt.hashpw("pin123".encode('utf-8'), bcrypt.gensalt())
            pin_account = UserAccount(
                username="pin",
                email="pin@csrvolunteering.com",
                password_hash=hashed_password.decode('utf-8'),
                first_name="PIN",
                last_name="Test",
                user_profile_id=pin_profile.id,
                is_active=True
            )
            session.add(pin_account)
            session.commit()
            print("✓ Default PIN account created")
            print("  Username: pin")
            print("  Password: pin123")
        else:
            print("✓ Default PIN account already exists")
        
        # Create default CSR Rep account
        existing_csr = session.query(UserAccount).filter_by(username="csr").first()
        if not existing_csr and csr_profile:
            hashed_password = bcrypt.hashpw("csr123".encode('utf-8'), bcrypt.gensalt())
            csr_account = UserAccount(
                username="csr",
                email="csr@csrvolunteering.com",
                password_hash=hashed_password.decode('utf-8'),
                first_name="CSR",
                last_name="Rep",
                user_profile_id=csr_profile.id,
                is_active=True
            )
            session.add(csr_account)
            session.commit()
            print("✓ Default CSR Rep account created")
            print("  Username: csr")
            print("  Password: csr123")
        else:
            print("✓ Default CSR Rep account already exists")
        
        # Create default Platform Manager account
        existing_pm = session.query(UserAccount).filter_by(username="pm").first()
        if not existing_pm and platform_manager_profile:
            hashed_password = bcrypt.hashpw("pm123".encode('utf-8'), bcrypt.gensalt())
            pm_account = UserAccount(
                username="pm",
                email="pm@csrvolunteering.com",
                password_hash=hashed_password.decode('utf-8'),
                first_name="Platform",
                last_name="Manager",
                user_profile_id=platform_manager_profile.id,
                is_active=True
            )
            session.add(pm_account)
            session.commit()
            print("✓ Default Platform Manager account created")
            print("  Username: pm")
            print("  Password: pm123")
        else:
            print("✓ Default Platform Manager account already exists")

        # Create Categories
        categories = [
            Category(created_by=4, title="Medical Assistance", description="Bringing PIN to clinic/hospital, collecting medication, accompanying to appointments"),
            Category(created_by=4, title="Mobility Support", description="Requesting wheelchairs, assistance with mobility aids, transporting PINs to events"),
            Category(created_by=4, title="Household Assistance", description="Cleaning, minor repairs, grocery shopping, cooking"),
            Category(created_by=4, title="Elderly Care", description="Companionship, reading sessions, help with technology for seniors"),
            Category(created_by=4, title="Childcare Support", description="Babysitting, helping children with homework, escorting children to school"),
            Category(created_by=4, title="Food & Essentials Aid", description="Delivering meals, distributing food packs or hygiene kits"),
            Category(created_by=4, title="Community Events", description="Helping to organize charity drives, community clean-ups"),
            Category(created_by=4, title="Environmental Projects", description="Tree planting, recycling drives, community garden maintenance"),
            Category(created_by=4, title="Miscellaneous", description="For requests that do not fit into other categories"),
        ]
        categories_created = 0
        for category in categories:
            existing = session.query(Category).filter_by(title=category.title).first()
            if not existing:
                session.add(category)
                categories_created += 1

        if categories_created > 0:
            session.commit()
            print(f"✓ {categories_created} new category(ies) created successfully")
        else:
            print("✓ Categories already exists")
        
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