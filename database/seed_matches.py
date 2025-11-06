"""
Script to seed test completed match data
Run this to create sample completed matches for testing
"""

from database.db_config import get_session
from entities.match import Match
from entities.request import Request
from entities.user_account import UserAccount
from datetime import datetime, timedelta


def seed_completed_matches():
    """
    Create sample completed matches for testing
    """
    session = get_session()
    
    try:
        from entities.user_profile import UserProfile
        
        # Find PIN profile ID
        pin_profile = session.query(UserProfile).filter_by(profile_name='PIN').first()
        csr_profile = session.query(UserProfile).filter_by(profile_name='CSR Rep').first()
        
        if not pin_profile or not csr_profile:
            print("✗ User profiles not found. Please run database initialization first.")
            return
        
        # Find a PIN user and a CSR Rep user
        pin_user = session.query(UserAccount).filter_by(user_profile_id=pin_profile.id).first()
        csr_rep = session.query(UserAccount).filter_by(user_profile_id=csr_profile.id).first()
        
        if not pin_user:
            print("✗ No PIN user found. Please create a PIN user account first.")
            return
        
        if not csr_rep:
            print("✗ No CSR Rep user found. Please create a CSR Rep user account first.")
            return
        
        # Find requests from the PIN user (with category relationship loaded)
        from sqlalchemy.orm import joinedload
        requests = session.query(Request).options(
            joinedload(Request.category)
        ).filter_by(user_account_id=pin_user.id).limit(5).all()
        
        if not requests:
            print("✗ No requests found for PIN user. Please create some requests first.")
            return
        
        matches_created = 0
        
        # Create completed matches for some requests
        for i, req in enumerate(requests[:3]):  # Create matches for up to 3 requests
            # Check if match already exists
            existing = session.query(Match).filter_by(
                request_id=req.request_id,
                pin_id=pin_user.id,
                csr_rep_id=csr_rep.id
            ).first()
            
            if existing:
                print(f"  - Match already exists for Request ID {req.request_id}, skipping")
                continue
            
            # Get service type from the request's category
            # If request has a category, use its title; otherwise use "Miscellaneous" as fallback
            service_type = 'Miscellaneous'  # Default fallback
            if req.category:
                service_type = req.category.title
            elif req.category_id:
                # If category relationship isn't loaded, query it directly
                from entities.category import Category
                category = session.query(Category).filter_by(category_id=req.category_id).first()
                if category:
                    service_type = category.title
            
            # Create completed match
            completed_at = datetime.now() - timedelta(days=i+1)  # Different dates for each
            
            match = Match(
                request_id=req.request_id,
                pin_id=pin_user.id,
                csr_rep_id=csr_rep.id,
                status='Completed',
                service_type=service_type,  # Use category title from request
                notes=f'Completed assistance for request: {req.title}',
                completed_at=completed_at,
                created_at=completed_at - timedelta(days=2),
                updated_at=completed_at
            )
            
            session.add(match)
            matches_created += 1
            print(f"  ✓ Created completed match for Request ID {req.request_id} (Service Type: {service_type})")
        
        if matches_created > 0:
            session.commit()
            print(f"\n✓ {matches_created} completed match(es) created successfully")
            print(f"  PIN User: {pin_user.username}")
            print(f"  CSR Rep: {csr_rep.username}")
        else:
            print("\n✗ No new matches created")
        
    except Exception as e:
        session.rollback()
        print(f"✗ Error seeding matches: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    print("Seeding completed matches...")
    seed_completed_matches()
    print("\nDone!")

