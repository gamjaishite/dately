from datetime import datetime
import enum
from typing import TYPE_CHECKING, Optional, List
from pydantic import constr
from sqlmodel import SQLModel, Field, Relationship
if TYPE_CHECKING:
    from Models.date_model.date_model import DateModel


class RoleEnum(enum.Enum):
    main = "MAIN"
    partner = "PARTNER"


class ProfileModel(SQLModel, table=True):
    __tablename__ = "profiles"

    index: Optional[int] = Field(default=None, primary_key=True)
    id: str
    name: str
    picture: Optional[bytes] = Field(default=None)
    hobbies: Optional[str] = Field(default=None)
    mbti: Optional[str] = Field(default=None)
    social_media: Optional[str] = Field(default=None)
    role: str = Field(default=RoleEnum.main.value)
    created_at: Optional[datetime] = Field(
        default=datetime.utcnow(), nullable=False)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=False)

    # Relationship
    dates: List["DateModel"] = Relationship(back_populates="partner")

    def __repr__(self):
        return f"({self.id}) {self.name} {self.hobbies} {self.mbti} {self.social_media} {self.role} {self.created_at} {self.updated_at}"
