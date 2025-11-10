"""
seed_matches.py
Script to seed test *completed* match data so your CSR/PIN history pages stop looking lonely.
Run:  python seed_matches.py
"""

from datetime import datetime, timedelta, time
from typing import List

from sqlalchemy.orm import joinedload

from database.db_config import get_session
from entities.match import Match
from entities.request import Request
from entities.user_account import UserAccount
from entities.user_profile import UserProfile
from entities.category import Category  # only used if we need a fallback title


def _pick_service_type(req: Request, session) -> str:
    """
    Choose a service_type from the request's category title if available.
    Otherwise fall back to 'Miscellaneous'.
    """
    if getattr(req, "category", None) and getattr(req.category, "title", None):
        return req.category.title

    # If relationship isn't loaded but category_id exists, fetch it
    if getattr(req, "category_id", None):
        cat = session.query(Category).filter_by(category_id=req.category_id).first()
        if cat and cat.title:
            return cat.title

    return "Miscellaneous"


def _already_has_completed_match(session, req: Request, pin_user: UserAccount, csr_user: UserAccount) -> Match | None:
    """
    Return an existing match for the same request/pin/csr if it exists (any status).
    """
    return (
        session.query(Match)
        .filter(
            Match.request_id == req.request_id,
            Match.pin_id == pin_user.id,
            Match.csr_rep_id == csr_user.id,
        )
        .first()
    )


def seed_completed_matches(limit: int = 3) -> None:
    """
    Create up to `limit` completed matches across the most recent requests
    owned by a PIN user, assigned to a CSR Rep. Skips anything that already exists.
    If a match exists but isn't Completed, we flip it to Completed (you’re welcome).
    """
    session = get_session()
    try:
        # Ensure required profiles exist
        pin_profile = session.query(UserProfile).filter_by(profile_name="PIN").first()
        csr_profile = session.query(UserProfile).filter_by(profile_name="CSR Rep").first()
        if not pin_profile or not csr_profile:
            print("✗ User profiles not found. Run DB init first.")
            return

        # Grab any PIN and any CSR Rep (first ones will do for seeding)
        pin_user = session.query(UserAccount).filter_by(user_profile_id=pin_profile.id).first()
        csr_user = session.query(UserAccount).filter_by(user_profile_id=csr_profile.id).first()
        if not pin_user:
            print("✗ No PIN user found. Create a PIN user first.")
            return
        if not csr_user:
            print("✗ No CSR Rep user found. Create a CSR Rep user first.")
            return

        # Pull a few recent requests *belonging to that PIN* (with category eager-loaded)
        requests: List[Request] = (
            session.query(Request)
            .options(joinedload(Request.category))
            .filter(Request.user_account_id == pin_user.id)
            .order_by(Request.created_at.desc())
            .limit(max(1, limit + 2))  # grab a few extra in case some are already matched
            .all()
        )
        if not requests:
            print("✗ No requests found for the PIN user. Create some requests first.")
            return

        matches_created = 0
        matches_updated = 0
        day_cursor = 1

        for req in requests[:limit]:
            existing = _already_has_completed_match(session, req, pin_user, csr_user)

            completed_at = datetime.now() - timedelta(days=day_cursor)
            created_at = completed_at - timedelta(days=2)
            day_cursor += 1

            if existing:
                if existing.status != "Completed":
                    existing.status = "Completed"
                    existing.service_type = existing.service_type or _pick_service_type(req, session)
                    existing.completed_at = existing.completed_at or completed_at
                    existing.updated_at = datetime.now()
                    matches_updated += 1
                    print(f"  ↺ Updated existing match #{existing.match_id} to Completed for request {req.request_id}")
                else:
                    print(f"  - Completed match already exists for request {req.request_id}, skipping")
                continue

            # Create a fresh completed match
            service_type = _pick_service_type(req, session)
            match = Match(
                request_id=req.request_id,
                pin_id=pin_user.id,
                csr_rep_id=csr_user.id,
                status="Completed",
                service_type=service_type,
                notes=f"Completed assistance for request: {req.title}",
                completed_at=completed_at,
                created_at=created_at,
                updated_at=completed_at,
            )
            session.add(match)
            matches_created += 1
            print(f"  ✓ Created completed match for Request ID {req.request_id} (Service Type: {service_type})")

        if matches_created or matches_updated:
            session.commit()
            print(
                f"\n✓ Done. Created: {matches_created}, Updated: {matches_updated} "
                f"| PIN: {pin_user.username} | CSR: {csr_user.username}"
            )
        else:
            print("\nℹ Nothing to do. You already had enough completed matches. Show-off.")

    except Exception as e:
        session.rollback()
        print(f"✗ Error seeding matches: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            session.close()
        except Exception:
            pass


if __name__ == "__main__":
    print("Seeding completed matches...")
    seed_completed_matches(limit=3)
    print("\nDone!")
