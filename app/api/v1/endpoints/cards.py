import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.cache import get_cached_cards, invalidate_cards, set_cached_cards
from app.db.session import get_db
from app.models.loyalty_card import LoyaltyCardDB
from app.models.user import UserDB
from app.schemas.loyalty_card import LoyaltyCard, LoyaltyCardCreate

router = APIRouter()


@router.get("", response_model=List[LoyaltyCard], summary="List all loyalty cards")
async def list_cards(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> List[LoyaltyCard]:
    cached = get_cached_cards(current_user.id)
    if cached is not None:
        return cached

    cards = (
        db.query(LoyaltyCardDB)
        .filter(LoyaltyCardDB.user_id == current_user.id)
        .all()
    )
    result = [LoyaltyCard.model_validate(card).model_dump(mode="json") for card in cards]
    set_cached_cards(current_user.id, result)
    return result


@router.post(
    "",
    response_model=LoyaltyCard,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new loyalty card",
)
async def create_card(
    card_in: LoyaltyCardCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> LoyaltyCard:
    db_card = LoyaltyCardDB(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        **card_in.model_dump(),
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    invalidate_cards(current_user.id)
    return db_card


@router.get("/{card_id}", response_model=LoyaltyCard, summary="Get card by ID")
async def get_card(
    card_id: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> LoyaltyCard:
    card = (
        db.query(LoyaltyCardDB)
        .filter(LoyaltyCardDB.id == card_id, LoyaltyCardDB.user_id == current_user.id)
        .first()
    )
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
async def delete_card(
    card_id: str,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    card = (
        db.query(LoyaltyCardDB)
        .filter(LoyaltyCardDB.id == card_id, LoyaltyCardDB.user_id == current_user.id)
        .first()
    )
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found"
        )
    db.delete(card)
    db.commit()
    invalidate_cards(current_user.id)
    return None
