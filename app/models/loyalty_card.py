import uuid
from sqlalchemy import Column, Integer, JSON, String
from app.db.session import Base


class LoyaltyCardDB(Base):
    __tablename__ = "loyalty_cards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    store_name = Column(String, nullable=False, index=True)
    card_holder_name = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    gradient_colors = Column(JSON, nullable=False)
    icon_name = Column(String, nullable=False, default="creditcard_fill")
    points = Column(Integer, nullable=False, default=0)
