from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from Models.profile_model.profile_model import ProfileModel
from Models.outfit_model.outfit_model import OutfitModel
from Models.outfit_date_join_model.outfit_date_join_model import OutfitDateJoinModel


class DateModel(SQLModel, table=True):
    __tablename__ = "dates"

    index: Optional[int] = Field(default=None, primary_key=True)
    id: str
    description: Optional[str] = Field(default=None)
    date: datetime
    location: str
    status: bool
    rating: Optional[int] = Field(default=None)
    review: Optional[str] = Field(default=None)
    partner_id: Optional[int] = Field(
        default=None, foreign_key="profiles.index")
    created_at: Optional[datetime] = Field(
        default=datetime.utcnow())
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow)

    # Relationship
    partner: ProfileModel = Relationship(back_populates="dates")
    outfits: List[OutfitModel] = Relationship(
        back_populates="dates", link_model=OutfitDateJoinModel)

    def __repr__(self):
        return f"({self.id}) {self.description} {self.date} {self.location} {self.status} {self.rating} {self.review} {self.partner_id} {self.created_at} {self.updated_at}"
