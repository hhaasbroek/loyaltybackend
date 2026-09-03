from typing import List
from pydantic import BaseModel, ConfigDict, Field


class LoyaltyCardBase(BaseModel):
    store_name: str = Field(..., description="Name of store or brand")
    card_holder_name: str = Field(..., description="Card member name")
    card_number: str = Field(..., description="Card serial or barcode number")
    category: str = Field(..., description="Category name")
    gradient_colors: List[str] = Field(
        default=["#006241", "#003D29"],
        description="Hex color strings for UI background gradient",
    )
    icon_name: str = Field(
        default="creditcard", description="Icon identifier for mobile UI"
    )
    points: int = Field(default=0, description="Loyalty points total")


class LoyaltyCardCreate(LoyaltyCardBase):
    pass


class LoyaltyCard(LoyaltyCardBase):
    id: str

    model_config = ConfigDict(from_attributes=True)

