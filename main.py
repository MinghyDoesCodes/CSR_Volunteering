"""
CSR Volunteering System - Main Application Entry Point
"""

from database.db_config import init_database
from boundaries.user_admin_boundary import UserAdminBoundary
import os


def main():
    """Main entry point for the application"""
    
    # Check if database exists
    db_exists = os.path.exists("csr_volunteering.db")
    
    if not db_exists:
        print("Database not found. Initializing...")
        print("\nPlease run the following command first:")
        print("  python -m database.init_db")
        print("\nThis will create the database and seed initial data.")
        return
    
    # Start the User Admin interface
    print("\n" + "="*60)
    print("WELCOME TO CSR VOLUNTEERING SYSTEM")
    print("="*60)
    print("\nStarting User Admin Module...")
    
    boundary = UserAdminBoundary()
    boundary.run()


if __name__ == "__main__":
    main()

