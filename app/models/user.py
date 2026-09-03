from sqlalchemy import Column, String
from app.db.session import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # Firebase UID
    email = Column(String, nullable=True, index=True)
    display_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
