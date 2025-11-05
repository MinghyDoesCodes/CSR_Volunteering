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
        
        # Request templates for variety
        request_templates = [
            # category_id = 1 → Medical Assistance
            ("Transportation to medical appointment", "Need a ride to the hospital for my check-up", 1),
            
            # category_id = 2 → Mobility Support
            ("Need help moving furniture", "Looking for volunteers to help move heavy furniture to a new apartment", 2),
            ("Help moving boxes", "Need assistance moving boxes to storage", 2),
            ("Moving assistance needed", "Can someone help me move my belongings this weekend?", 2),
            
            # category_id = 3 → Household Assistance
            ("Home repairs needed", "Need help fixing a leaky faucet and broken door", 3),
            ("Gardening assistance", "Looking for help with yard work and gardening", 3),
            ("Cleaning help needed", "Need assistance with deep cleaning my apartment", 3),
            ("Furniture assembly", "Help needed to assemble IKEA furniture", 3),
            ("Painting assistance", "Looking for volunteers to help paint a room", 3),
            ("Laundry help", "Need assistance with laundry", 3),
            
            # category_id = 4 → Elderly Care
            ("Companionship needed", "Looking for someone to visit and chat", 4),
            ("Elderly care assistance", "Need help with daily tasks", 4),
            ("Reading assistance", "Need someone to read documents for me", 4),
            ("Phone assistance", "Help needed to learn how to use my smartphone", 4),
            
            # category_id = 5 → Childcare Support
            ("Childcare assistance", "Looking for temporary childcare help", 5),
            
            # category_id = 6 → Food & Essentials Aid
            ("Meal preparation help", "Need help preparing meals for the week", 6),
            ("Food delivery assistance", "Looking for help getting groceries", 6),
            ("Cooking assistance", "Need someone to teach basic cooking skills", 6),
            ("Shopping assistance", "Help needed with grocery shopping", 6),
            
            # category_id = 7 → Community Events
            ("Event setup help", "Need volunteers for community event setup", 7),
            
            # category_id = 8 → Environmental Projects
            ("Gardening assistance", "Looking for help with yard work and gardening", 8),
            
            # category_id = 9 → Miscellaneous
            ("Document help", "Need assistance filling out forms", 9),
            ("Tech support", "Need assistance with my laptop issues", 9),
            ("Computer help needed", "Need help setting up my computer and internet", 9),
            ("Language learning", "Need assistance learning English", 9),
            ("Computer skills training", "Want to learn basic computer skills", 9),
            ("Pet care help", "Need someone to walk my dog while I'm sick", 9),
        ]
        
        # Status options - all requests start as Pending (newly submitted)
        status = 'Pending'
        
        # Generate 120 requests
        requests_created = 0
        start_date = datetime.now() - timedelta(days=90)  # Requests from last 90 days
        
        for i in range(120):
            # Randomly select a request template
            title_template, desc_template, categoryID = random.choice(request_templates)
            
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
                category_id = categoryID,
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