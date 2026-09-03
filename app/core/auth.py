from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as firebase_auth
from sqlalchemy.orm import Session

from app.core.firebase import get_firebase_app
from app.db.session import get_db
from app.models.user import UserDB

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserDB:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    get_firebase_app()

    try:
        decoded = firebase_auth.verify_id_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )

    uid = decoded["uid"]
    user = db.query(UserDB).filter(UserDB.id == uid).first()
    if user is None:
        user = UserDB(
            id=uid,
            email=decoded.get("email"),
            display_name=decoded.get("name"),
            photo_url=decoded.get("picture"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
