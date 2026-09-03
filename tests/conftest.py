from app.core.auth import get_current_user
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.main import app
from app.models.user import UserDB

# TestClient doesn't run the app's lifespan (which normally creates tables)
# unless used as a context manager, so create tables directly here instead.
init_db()

FAKE_UID = "test-uid-123"

# Overriding get_current_user bypasses the real JIT user-provisioning logic,
# but loyalty_cards.user_id still has a FK to users.id, so the fake user needs
# to actually exist in the DB for card creation to succeed.
with SessionLocal() as _db:
    if _db.query(UserDB).filter(UserDB.id == FAKE_UID).first() is None:
        _db.add(UserDB(id=FAKE_UID, email="test@example.com", display_name="Test User"))
        _db.commit()


def _fake_current_user() -> UserDB:
    return UserDB(id=FAKE_UID, email="test@example.com", display_name="Test User")


app.dependency_overrides[get_current_user] = _fake_current_user
