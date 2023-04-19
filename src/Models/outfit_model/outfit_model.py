from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship
from Models.outfit_date_join_model.outfit_date_join_model import OutfitDateJoinModel
from Models.outfit_category_join_model.outfit_category_join_model import OutfitCategoryJoinModel
if TYPE_CHECKING:
    from Models.date_model.date_model import DateModel
    from Models.outfit_category_model.outfit_category_model import OutfitCategoryModel


class OutfitModel(SQLModel, table=True):
    __tablename__ = "outfits"

    index: Optional[int] = Field(default=None, primary_key=True)
    id: str
    name: str = Field(unique=True)
    description: Optional[str] = Field(default=None)
    picture: Optional[bytes] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default=datetime.utcnow(), nullable=False)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False)

    # Relationship
    dates: List["DateModel"] = Relationship(
        back_populates="outfits", link_model=OutfitDateJoinModel)
    outfit_categories: List["OutfitCategoryModel"] = Relationship(
        back_populates="outfits", link_model=OutfitCategoryJoinModel)

    def __repr__(self):
        return f"({self.id}) {self.name} {self.description} {self.created_at} {self.updated_at}"
