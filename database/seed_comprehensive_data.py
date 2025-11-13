"""
Comprehensive Seed Script for CSR Volunteering Platform
Generates large-scale demo data for final product demonstration:
- 100 PIN user accounts (pin, pin2, pin3...pin100)
- 100 CSR Rep user accounts (csr, csr2, csr3...csr100)
- 5 User Admin accounts (useradmin, useradmin2...useradmin5)
- 5 Platform Manager accounts (pm2, pm3...pm6) - pm already exists from init
- 120 Requests (distributed across PIN users, spread over past 3 months)
- 120 Shortlists (CSR Reps saving requests, spread over time)
- 120 Matches (completed volunteer services, spread over past 3 months)

This creates realistic data with timestamps for proper Daily/Weekly/Monthly report testing.
"""

from database.db_config import get_session
from entities.user_account import UserAccount
from entities.user_profile import UserProfile
from entities.request import Request
from entities.shortlist import Shortlist
from entities.match import Match
from entities.category import Category
from datetime import datetime, timedelta
import random
import bcrypt


def generate_comprehensive_data():
    """
    Generate comprehensive demo data for all entities
    """
    session = get_session()
    
    try:
        print("=" * 60)
        print("COMPREHENSIVE DATA GENERATION FOR CSR VOLUNTEERING PLATFORM")
        print("=" * 60)
        
        # Get user profiles
        pin_profile = session.query(UserProfile).filter_by(profile_name='PIN').first()
        csr_profile = session.query(UserProfile).filter_by(profile_name='CSR Rep').first()
        admin_profile = session.query(UserProfile).filter_by(profile_name='User Admin').first()
        pm_profile = session.query(UserProfile).filter_by(profile_name='Platform Manager').first()
        
        if not all([pin_profile, csr_profile, admin_profile, pm_profile]):
            print("✗ User profiles not found. Please run database initialization first.")
            return
        
        print("\n1. GENERATING USER ACCOUNTS")
        print("-" * 60)
        
        # Track created accounts for later use
        pin_accounts = []
        csr_accounts = []
        
        # Generate 100 PIN accounts (pin, pin2, pin3...pin100)
        print("Creating 100 PIN user accounts...")
        pin_password = bcrypt.hashpw("pin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        for i in range(1, 101):
            username = "pin" if i == 1 else f"pin{i}"
            
            # Check if already exists
            existing = session.query(UserAccount).filter_by(username=username).first()
            if existing:
                pin_accounts.append(existing)
                continue
            
            account = UserAccount(
                username=username,
                email=f"{username}@csrvolunteering.com",
                password_hash=pin_password,
                first_name=f"PIN{i}",
                last_name="User",
                phone_number=f"555-PIN-{i:04d}",
                user_profile_id=pin_profile.id,
                is_active=True
            )
            session.add(account)
            pin_accounts.append(account)
            
            if i % 20 == 0:
                session.flush()  # Flush to get IDs
                print(f"  Created {i}/100 PIN accounts...")
        
        session.commit()
        print(f"✓ {len(pin_accounts)} PIN accounts ready")
        
        # Generate 100 CSR Rep accounts (csr, csr2, csr3...csr100)
        print("\nCreating 100 CSR Rep user accounts...")
        csr_password = bcrypt.hashpw("csr123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        for i in range(1, 101):
            username = "csr" if i == 1 else f"csr{i}"
            
            # Check if already exists
            existing = session.query(UserAccount).filter_by(username=username).first()
            if existing:
                csr_accounts.append(existing)
                continue
            
            account = UserAccount(
                username=username,
                email=f"{username}@company.com",
                password_hash=csr_password,
                first_name=f"CSR{i}",
                last_name="Rep",
                phone_number=f"555-CSR-{i:04d}",
                user_profile_id=csr_profile.id,
                is_active=True
            )
            session.add(account)
            csr_accounts.append(account)
            
            if i % 20 == 0:
                session.flush()
                print(f"  Created {i}/100 CSR Rep accounts...")
        
        session.commit()
        print(f"✓ {len(csr_accounts)} CSR Rep accounts ready")
        
        # Generate 5 User Admin accounts (useradmin, useradmin2...useradmin5)
        print("\nCreating 5 User Admin accounts...")
        admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        for i in range(1, 6):
            username = "useradmin" if i == 1 else f"useradmin{i}"
            
            existing = session.query(UserAccount).filter_by(username=username).first()
            if existing:
                continue
            
            account = UserAccount(
                username=username,
                email=f"{username}@csrvolunteering.com",
                password_hash=admin_password,
                first_name=f"Admin{i}",
                last_name="User",
                phone_number=f"555-ADM-{i:04d}",
                user_profile_id=admin_profile.id,
                is_active=True
            )
            session.add(account)
        
        session.commit()
        print("✓ 5 User Admin accounts created")
        
        # Generate 5 additional Platform Manager accounts (pm already exists, add pm2...pm6)
        print("\nCreating 5 additional Platform Manager accounts...")
        pm_password = bcrypt.hashpw("pm123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        for i in range(2, 7):
            username = f"pm{i}"
            
            existing = session.query(UserAccount).filter_by(username=username).first()
            if existing:
                continue
            
            account = UserAccount(
                username=username,
                email=f"{username}@csrvolunteering.com",
                password_hash=pm_password,
                first_name=f"Manager{i}",
                last_name="Platform",
                phone_number=f"555-PM{i}-0000",
                user_profile_id=pm_profile.id,
                is_active=True
            )
            session.add(account)
        
        session.commit()
        print("✓ 5 additional Platform Manager accounts created")
        
        print("\n2. GENERATING REQUESTS")
        print("-" * 60)
        
        # Get all active categories
        categories = session.query(Category).filter_by(is_active=True).all()
        if not categories:
            print("✗ No categories found. Please run database initialization first.")
            return
        
        # Request templates with categories
        request_templates = [
            ("Transportation to medical appointment", "Need a ride to the hospital for my check-up", "Medical Assistance"),
            ("Help with medication pickup", "Need someone to pick up my prescription", "Medical Assistance"),
            ("Doctor appointment accompaniment", "Need companion for medical consultation", "Medical Assistance"),
            
            ("Wheelchair assistance needed", "Need help with wheelchair for mobility", "Mobility Support"),
            ("Help moving furniture", "Looking for volunteers to help move heavy furniture", "Mobility Support"),
            ("Moving assistance needed", "Can someone help me move my belongings this weekend?", "Mobility Support"),
            
            ("Home repairs needed", "Need help fixing a leaky faucet", "Household Assistance"),
            ("Cleaning help needed", "Need assistance with deep cleaning", "Household Assistance"),
            ("Furniture assembly", "Help needed to assemble furniture", "Household Assistance"),
            ("Gardening assistance", "Looking for help with yard work", "Household Assistance"),
            ("Painting assistance", "Looking for volunteers to help paint a room", "Household Assistance"),
            
            ("Companionship needed", "Looking for someone to visit and chat", "Elderly Care"),
            ("Reading assistance", "Need someone to read documents for me", "Elderly Care"),
            ("Phone assistance", "Help needed to learn how to use smartphone", "Elderly Care"),
            ("Elderly care assistance", "Need help with daily tasks", "Elderly Care"),
            
            ("Childcare assistance", "Looking for temporary childcare help", "Childcare Support"),
            ("After-school care needed", "Need help with after-school care for my child", "Childcare Support"),
            ("Homework help for kids", "Need volunteer to help child with homework", "Childcare Support"),
            
            ("Meal preparation help", "Need help preparing meals for the week", "Food & Essentials Aid"),
            ("Food delivery assistance", "Looking for help getting groceries", "Food & Essentials Aid"),
            ("Shopping assistance", "Help needed with grocery shopping", "Food & Essentials Aid"),
            
            ("Event setup help", "Need volunteers for community event setup", "Community Events"),
            ("Community cleanup", "Join us for neighborhood cleanup", "Community Events"),
            
            ("Tree planting help", "Help needed for tree planting initiative", "Environmental Projects"),
            ("Recycling drive assistance", "Need volunteers for recycling event", "Environmental Projects"),
            
            ("Document help", "Need assistance filling out forms", "Miscellaneous"),
            ("Tech support", "Need assistance with laptop issues", "Miscellaneous"),
            ("Computer help needed", "Need help setting up computer", "Miscellaneous"),
            ("Language learning", "Need assistance learning English", "Miscellaneous"),
        ]
        
        # Create category mapping
        category_map = {cat.title: cat.category_id for cat in categories}
        
        # Generate 120 requests distributed across PIN users
        print("Creating 120 requests distributed across PIN users...")
        requests_created = []
        start_date = datetime.now() - timedelta(days=90)  # Past 3 months
        
        for i in range(120):
            # Select random PIN user
            pin_user = random.choice(pin_accounts)
            
            # Select random template
            title_template, desc_template, category_title = random.choice(request_templates)
            
            # Get category_id
            category_id = category_map.get(category_title, categories[0].category_id)
            
            # Add variety to titles
            title = f"{title_template} #{i+1}"
            description = desc_template
            if random.random() > 0.5:
                description += " Please contact me if you can help. Thank you!"
            
            # Random status: 60% Pending, 40% Completed
            status = 'Completed' if random.random() < 0.4 else 'Pending'
            
            # Random creation date (spread over last 90 days)
            days_ago = random.randint(0, 90)
            created_at = start_date + timedelta(days=days_ago, hours=random.randint(0, 23))
            
            request = Request(
                user_account_id=pin_user.id,
                title=title,
                category_id=category_id,
                description=description,
                status=status,
                view_count=random.randint(0, 50),  # Random view counts
                created_at=created_at,
                updated_at=created_at + timedelta(hours=random.randint(1, 48))
            )
            
            session.add(request)
            requests_created.append(request)
            
            if (i + 1) % 30 == 0:
                session.flush()
                print(f"  Created {i + 1}/120 requests...")
        
        session.commit()
        print(f"✓ {len(requests_created)} requests created successfully")
        print(f"  Status distribution: ~60% Pending, ~40% Completed")
        print(f"  Date range: Past 90 days")
        
        print("\n3. GENERATING SHORTLISTS")
        print("-" * 60)
        
        # Generate 120 shortlists (CSR Reps saving requests)
        print("Creating 120 shortlists distributed across CSR Reps...")
        shortlists_created = 0
        
        # Get all requests for shortlisting
        all_requests = session.query(Request).all()
        
        for i in range(120):
            # Select random CSR Rep
            csr_user = random.choice(csr_accounts)
            
            # Select random request
            request = random.choice(all_requests)
            
            # Check if this CSR Rep already shortlisted this request
            existing = session.query(Shortlist).filter_by(
                request_id=request.request_id,
                csr_rep_id=csr_user.id
            ).first()
            
            if existing:
                continue  # Skip duplicate shortlists
            
            # Random shortlist date (between request creation and now)
            days_diff = (datetime.now() - request.created_at).days
            if days_diff < 0:
                days_diff = 0  # Handle same-day requests
            shortlist_date = request.created_at + timedelta(
                days=random.randint(0, max(1, days_diff)),
                hours=random.randint(0, 23)
            )
            
            shortlist = Shortlist(
                request_id=request.request_id,
                csr_rep_id=csr_user.id,
                shortlisted_at=shortlist_date
            )
            
            session.add(shortlist)
            shortlists_created += 1
            
            if (i + 1) % 30 == 0:
                session.flush()
                print(f"  Created {shortlists_created} shortlists...")
        
        session.commit()
        print(f"✓ {shortlists_created} shortlists created successfully")
        
        print("\n4. GENERATING MATCHES")
        print("-" * 60)
        
        # Generate 120 matches (completed volunteer services)
        print("Creating 120 matches between PINs and CSR Reps...")
        matches_created = 0
        
        # Get completed requests for matching
        completed_requests = [r for r in requests_created if r.status == 'Completed']
        pending_requests = [r for r in requests_created if r.status == 'Pending']
        
        # We need 120 matches, prioritize completed requests
        requests_to_match = completed_requests + random.sample(
            pending_requests, 
            min(120 - len(completed_requests), len(pending_requests))
        )
        
        for i in range(min(120, len(requests_to_match))):
            request = requests_to_match[i]
            
            # Select random CSR Rep
            csr_user = random.choice(csr_accounts)
            
            # Random match creation date (between request creation and now)
            days_diff = (datetime.now() - request.created_at).days
            if days_diff < 1:
                days_diff = 1  # Minimum 1 day difference
            match_created = request.created_at + timedelta(
                days=random.randint(0, days_diff)
            )
            
            # For completed requests, set completed_at
            if request.status == 'Completed':
                match_status = 'Completed'
                completed_at = match_created + timedelta(days=random.randint(1, 14))
            else:
                match_status = random.choice(['Pending', 'In Progress'])
                completed_at = None
            
            # Get service type from category
            category = session.query(Category).filter_by(category_id=request.category_id).first()
            service_type = category.title if category else "General Assistance"
            
            match = Match(
                request_id=request.request_id,
                pin_id=request.user_account_id,
                csr_rep_id=csr_user.id,
                status=match_status,
                service_type=service_type,
                notes=f"Volunteer service for: {request.title[:50]}",
                created_at=match_created,
                completed_at=completed_at,
                updated_at=completed_at or match_created
            )
            
            session.add(match)
            matches_created += 1
            
            if (i + 1) % 30 == 0:
                session.flush()
                print(f"  Created {matches_created} matches...")
        
        session.commit()
        print(f"✓ {matches_created} matches created successfully")
        print(f"  Status distribution: Mix of Pending, In Progress, Completed")
        
        print("\n" + "=" * 60)
        print("COMPREHENSIVE DATA GENERATION COMPLETE!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  ✓ 100 PIN user accounts (pin, pin2...pin100) - Password: pin123")
        print(f"  ✓ 100 CSR Rep accounts (csr, csr2...csr100) - Password: csr123")
        print(f"  ✓ 5 User Admin accounts (useradmin...useradmin5) - Password: admin123")
        print(f"  ✓ 5 Platform Manager accounts (pm2...pm6) - Password: pm123")
        print(f"  ✓ {len(requests_created)} requests distributed across PIN users")
        print(f"  ✓ {shortlists_created} shortlists from CSR Reps")
        print(f"  ✓ {matches_created} matches (volunteer services)")
        print(f"\nData spans: Past 90 days for realistic Daily/Weekly/Monthly reports")
        print("\nYour platform is now ready for final demonstration! 🎉")
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Error generating comprehensive data: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    print("\n⚠️  WARNING: This will generate a large amount of demo data!")
    print("This script will create:")
    print("  - 100 PIN user accounts")
    print("  - 100 CSR Rep user accounts")
    print("  - 5 User Admin accounts")
    print("  - 5 Platform Manager accounts")
    print("  - 120 Requests")
    print("  - 120 Shortlists")
    print("  - 120 Matches")
    print("\nThis may take a few minutes to complete.")
    
    confirm = input("\nContinue? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\nStarting comprehensive data generation...\n")
        generate_comprehensive_data()
        print("\nDone!")
    else:
        print("Cancelled.")

