import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.loyalty_card import LoyaltyCardDB
from app.schemas.loyalty_card import LoyaltyCard, LoyaltyCardCreate

router = APIRouter()


@router.get("", response_model=List[LoyaltyCard], summary="List all loyalty cards")
async def list_cards(db: Session = Depends(get_db)) -> List[LoyaltyCard]:
    cards = db.query(LoyaltyCardDB).all()
    return cards


@router.post(
    "",
    response_model=LoyaltyCard,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new loyalty card",
)
async def create_card(
    card_in: LoyaltyCardCreate, db: Session = Depends(get_db)
) -> LoyaltyCard:
    db_card = LoyaltyCardDB(
        id=str(uuid.uuid4()),
        **card_in.model_dump(),
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@router.get("/{card_id}", response_model=LoyaltyCard, summary="Get card by ID")
async def get_card(card_id: str, db: Session = Depends(get_db)) -> LoyaltyCard:
    card = db.query(LoyaltyCardDB).filter(LoyaltyCardDB.id == card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found"
        )
    return card


@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete card",
)
async def delete_card(card_id: str, db: Session = Depends(get_db)):
    card = db.query(LoyaltyCardDB).filter(LoyaltyCardDB.id == card_id).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found"
        )
    db.delete(card)
    db.commit()
    return None
