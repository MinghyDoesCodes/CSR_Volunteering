"""
Script to generate test data: 120 requests from the default PIN user
Run this to create realistic test data for demonstration

Note: These requests are created by the default PIN user (username: "pin").
Each PIN user will only see requests they created (filtered by user_account_id).
CSR Reps can see all requests to browse and shortlist them.
"""

from database.db_config import get_session
from entities.request import Request
from entities.user_account import UserAccount
from entities.user_profile import UserProfile
from datetime import datetime, timedelta
import random


def generate_test_requests():
    """
    Generate 120 test requests from the default PIN user
    """
    session = get_session()
    
    try:
        # Get PIN profile
        pin_profile = session.query(UserProfile).filter_by(profile_name='PIN').first()
        if not pin_profile:
            print("✗ PIN profile not found. Please run database initialization first.")
            return
        
        # Get the default PIN account (username: "pin")
        pin_account = session.query(UserAccount).filter_by(username='pin', user_profile_id=pin_profile.id).first()
        
        if not pin_account:
            print("✗ Default PIN account not found. Please run database initialization first.")
            print("  Expected username: 'pin'")
            return
        
        print(f"✓ Found PIN account: {pin_account.username} (ID: {pin_account.id})")
        
        # Get all active categories and create a mapping by title
        from entities.category import Category
        categories = session.query(Category).filter_by(is_active=True).all()
        
        if not categories:
            print("✗ No active categories found. Please create categories first.")
            print("  Run database initialization to create default categories.")
            return
        
        # Create a mapping from category title to category_id
        category_map = {cat.title: cat.category_id for cat in categories}
        
        # Verify all required categories exist
        required_categories = [
            "Medical Assistance", "Mobility Support", "Household Assistance",
            "Elderly Care", "Childcare Support", "Food & Essentials Aid",
            "Community Events", "Environmental Projects", "Miscellaneous"
        ]
        
        missing_categories = [cat for cat in required_categories if cat not in category_map]
        if missing_categories:
            print(f"⚠️  Warning: Some categories are missing: {', '.join(missing_categories)}")
            print("  Requests will be assigned to available categories only.")
        
        # Request templates for variety (using category titles instead of IDs)
        request_templates = [
            # Medical Assistance
            ("Transportation to medical appointment", "Need a ride to the hospital for my check-up", "Medical Assistance"),
            
            # Mobility Support
            ("Need help moving furniture", "Looking for volunteers to help move heavy furniture to a new apartment", "Mobility Support"),
            ("Help moving boxes", "Need assistance moving boxes to storage", "Mobility Support"),
            ("Moving assistance needed", "Can someone help me move my belongings this weekend?", "Mobility Support"),
            
            # Household Assistance
            ("Home repairs needed", "Need help fixing a leaky faucet and broken door", "Household Assistance"),
            ("Gardening assistance", "Looking for help with yard work and gardening", "Household Assistance"),
            ("Cleaning help needed", "Need assistance with deep cleaning my apartment", "Household Assistance"),
            ("Furniture assembly", "Help needed to assemble IKEA furniture", "Household Assistance"),
            ("Painting assistance", "Looking for volunteers to help paint a room", "Household Assistance"),
            ("Laundry help", "Need assistance with laundry", "Household Assistance"),
            
            # Elderly Care
            ("Companionship needed", "Looking for someone to visit and chat", "Elderly Care"),
            ("Elderly care assistance", "Need help with daily tasks", "Elderly Care"),
            ("Reading assistance", "Need someone to read documents for me", "Elderly Care"),
            ("Phone assistance", "Help needed to learn how to use my smartphone", "Elderly Care"),
            
            # Childcare Support
            ("Childcare assistance", "Looking for temporary childcare help", "Childcare Support"),
            
            # Food & Essentials Aid
            ("Meal preparation help", "Need help preparing meals for the week", "Food & Essentials Aid"),
            ("Food delivery assistance", "Looking for help getting groceries", "Food & Essentials Aid"),
            ("Cooking assistance", "Need someone to teach basic cooking skills", "Food & Essentials Aid"),
            ("Shopping assistance", "Help needed with grocery shopping", "Food & Essentials Aid"),
            
            # Community Events
            ("Event setup help", "Need volunteers for community event setup", "Community Events"),
            
            # Environmental Projects
            ("Gardening assistance", "Looking for help with yard work and gardening", "Environmental Projects"),
            
            # Miscellaneous
            ("Document help", "Need assistance filling out forms", "Miscellaneous"),
            ("Tech support", "Need assistance with my laptop issues", "Miscellaneous"),
            ("Computer help needed", "Need help setting up my computer and internet", "Miscellaneous"),
            ("Language learning", "Need assistance learning English", "Miscellaneous"),
            ("Computer skills training", "Want to learn basic computer skills", "Miscellaneous"),
            ("Pet care help", "Need someone to walk my dog while I'm sick", "Miscellaneous"),
        ]
        
        # Status options - all requests start as Pending (newly submitted)
        status = 'Pending'
        
        # Generate 120 requests
        requests_created = 0
        start_date = datetime.now() - timedelta(days=90)  # Requests from last 90 days
        
        for i in range(120):
            # Randomly select a request template
            title_template, desc_template, category_title = random.choice(request_templates)
            
            # Get category_id from the mapping (fallback to first available category if not found)
            category_id = category_map.get(category_title)
            if not category_id:
                # If category doesn't exist, use the first available category
                category_id = categories[0].category_id if categories else None
                if not category_id:
                    print("✗ No categories available. Cannot create requests.")
                    return
            
            # Add variety to titles
            title_variations = [
                title_template,
                f"Urgent: {title_template}",
                f"Help needed: {title_template}",
                f"{title_template} - Immediate assistance",
            ]
            title = random.choice(title_variations)
            if i < len(request_templates):
                title = request_templates[i][0]  # Use unique titles for first batch
            
            # Add variety to descriptions
            description = desc_template
            if random.random() > 0.5:
                description += " Please contact me if you can help. Thank you!"
            if random.random() > 0.7:
                description += " This is urgent and would be greatly appreciated."
            
            # All requests start as Pending (newly submitted requests)
            
            # Random creation date (spread over last 90 days)
            days_ago = random.randint(0, 90)
            created_at = start_date + timedelta(days=days_ago)
            
            # Create request from the default PIN account
            request = Request(
                user_account_id=pin_account.id,  # Created by default PIN user
                title=title,
                category_id=category_id,  # Use dynamically resolved category_id
                description=description,
                status=status,
                created_at=created_at,
                updated_at=created_at + timedelta(hours=random.randint(0, 24))
            )
            
            session.add(request)
            requests_created += 1
            
            if (i + 1) % 20 == 0:
                print(f"  Created {i + 1} requests...")
        
        session.commit()
        print(f"\n✓ {requests_created} test requests created successfully")
        print(f"  All requests created by: {pin_account.username} (PIN user)")
        print(f"  Status: All requests are 'Pending' (newly submitted)")
        print(f"  Date range: Last 90 days")
        print(f"\n⚠️  Note: These requests are owned by the default PIN account.")
        print(f"   Each PIN user will only see requests they created.")
        print(f"   CSR Reps can see all requests to browse and shortlist them.")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error generating test requests: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    print("Generating test requests...")
    print("This will create 120 test requests from the default PIN user (username: 'pin')")
    confirm = input("Continue? (y/n): ").strip().lower()
    
    if confirm == 'y':
        generate_test_requests()
        print("\nDone!")
    else:
        print("Cancelled.")