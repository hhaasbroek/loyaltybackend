from sqlalchemy.orm import Session
from app.db.session import Base, engine
from app.models.loyalty_card import LoyaltyCardDB


def init_db(db: Session) -> None:
    # Create tables if not created
    Base.metadata.create_all(bind=engine)

    # Seed default cards if empty
    count = db.query(LoyaltyCardDB).count()
    if count == 0:
        seed_cards = [
            LoyaltyCardDB(
                id="1",
                store_name="Starbucks",
                card_holder_name="Alex Morgan",
                card_number="9842 1092 8841",
                category="Coffee & Cafe",
                gradient_colors=["#006241", "#003D29"],
                icon_name="lab_flask",
                points=340,
            ),
            LoyaltyCardDB(
                id="2",
                store_name="Woolworths",
                card_holder_name="Alex Morgan",
                card_number="6011 4829 1049",
                category="Groceries",
                gradient_colors=["#1E5631", "#4C9A2A"],
                icon_name="cart_fill",
                points=1250,
            ),
            LoyaltyCardDB(
                id="3",
                store_name="Sephora",
                card_holder_name="Alex Morgan",
                card_number="5029 3847 1192",
                category="Beauty",
                gradient_colors=["#111111", "#333333"],
                icon_name="sparkles",
                points=820,
            ),
            LoyaltyCardDB(
                id="4",
                store_name="Nike Pass",
                card_holder_name="Alex Morgan",
                card_number="7723 9012 4431",
                category="Sports & Apparel",
                gradient_colors=["#FF5E36", "#FFAE36"],
                icon_name="sportscourt_fill",
                points=540,
            ),
        ]
        db.add_all(seed_cards)
        db.commit()
