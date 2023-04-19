from typing import Optional
from sqlmodel import SQLModel, Field


class OutfitDateJoinModel(SQLModel, table=True):
    __tablename__ = "outfits_dates"

    outfit_id: Optional[int] = Field(
        default=None, foreign_key="outfits.index", primary_key=True)
    date_id: Optional[int] = Field(
        default=None, foreign_key="dates.index", primary_key=True)

    def __repr__(self):
        return f"({self.outfit_id}) ({self.date_id})"
