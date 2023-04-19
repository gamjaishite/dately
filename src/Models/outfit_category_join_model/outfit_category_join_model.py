from typing import Optional
from sqlmodel import SQLModel, Field


class OutfitCategoryJoinModel(SQLModel, table=True):
    __tablename__ = "outfits_categories"

    outfit_id: Optional[int] = Field(
        default=None, foreign_key="outfits.index", primary_key=True)
    category_id: Optional[int] = Field(
        default=None, foreign_key="outfitCategories.index", primary_key=True)

    def __repr__(self):
        return f"({self.outfit_id}) ({self.category_id})"
