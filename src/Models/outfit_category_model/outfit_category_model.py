from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship
from Models.outfit_category_join_model.outfit_category_join_model import OutfitCategoryJoinModel
if TYPE_CHECKING:
    from Models.outfit_model.outfit_model import OutfitModel


class OutfitCategoryModel(SQLModel, table=True):
    __tablename__ = "outfitCategories"

    index: Optional[int] = Field(default=None, primary_key=True)
    id: str
    name: str = Field(unique=True)
    created_at: Optional[datetime] = Field(
        default=datetime.utcnow(), nullable=False)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False)

    # Relationships
    outfits: List["OutfitModel"] = Relationship(
        back_populates="outfit_categories", link_model=OutfitCategoryJoinModel)

    def __repr__(self):
        return f"({self.id}) {self.name} {self.created_at} {self.updated_at}"
