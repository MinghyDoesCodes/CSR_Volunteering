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
            # Moving/Transportation
            ("Need help moving furniture", "Looking for volunteers to help move heavy furniture to a new apartment"),
            ("Transportation to medical appointment", "Need a ride to the hospital for my check-up"),
            ("Help moving boxes", "Need assistance moving boxes to storage"),
            ("Moving assistance needed", "Can someone help me move my belongings this weekend?"),
            
            # Household/Home
            ("Home repairs needed", "Need help fixing a leaky faucet and broken door"),
            ("Gardening assistance", "Looking for help with yard work and gardening"),
            ("Cleaning help needed", "Need assistance with deep cleaning my apartment"),
            ("Furniture assembly", "Help needed to assemble IKEA furniture"),
            ("Painting assistance", "Looking for volunteers to help paint a room"),
            
            # Technology
            ("Computer help needed", "Need help setting up my computer and internet"),
            ("Phone assistance", "Help needed to learn how to use my smartphone"),
            ("Tech support", "Need assistance with my laptop issues"),
            
            # Food/Meals
            ("Meal preparation help", "Need help preparing meals for the week"),
            ("Food delivery assistance", "Looking for help getting groceries"),
            ("Cooking assistance", "Need someone to teach basic cooking skills"),
            
            # Education/Tutoring
            ("Tutoring needed", "Looking for help with math homework"),
            ("Language learning", "Need assistance learning English"),
            ("Computer skills training", "Want to learn basic computer skills"),
            
            # Companionship
            ("Companionship needed", "Looking for someone to visit and chat"),
            ("Elderly care assistance", "Need help with daily tasks"),
            ("Reading assistance", "Need someone to read documents for me"),
            
            # Miscellaneous
            ("Document help", "Need assistance filling out forms"),
            ("Shopping assistance", "Help needed with grocery shopping"),
            ("Pet care help", "Need someone to walk my dog while I'm sick"),
            ("Childcare assistance", "Looking for temporary childcare help"),
            ("Laundry help", "Need assistance with laundry"),
            ("Event setup help", "Need volunteers for community event setup"),
        ]
        
        # Status options
        statuses = ['Pending', 'Pending', 'Pending', 'Pending', 'Completed']  # Mostly pending, some completed
        
        # Generate 120 requests
        requests_created = 0
        start_date = datetime.now() - timedelta(days=90)  # Requests from last 90 days
        
        for i in range(120):
            # Randomly select a request template
            title_template, desc_template = random.choice(request_templates)
            
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
            
            # Random status (mostly pending)
            status = random.choice(statuses)
            
            # Random creation date (spread over last 90 days)
            days_ago = random.randint(0, 90)
            created_at = start_date + timedelta(days=days_ago)
            
            # Create request from the default PIN account
            request = Request(
                user_account_id=pin_account.id,  # Created by default PIN user
                title=title,
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
        print(f"  Status distribution: Mostly 'Pending', some 'Completed'")
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

