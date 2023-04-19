from pydantic import BaseModel, ValidationError, validator
from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship
from Models.profile_model.profile_model import ProfileModel
import Utils

class DateValidatorSchema(BaseModel):
    """ Add attributes here """
    description: Optional[str] = Field(default=None)
    date: Optional[datetime] = Field(default=None)
    location: str
    
    Relationship
    partner: ProfileModel | None = Relationship(back_populates="dates")


    """ Add custom validation here """
    @validator("description")
    def validate_description(value):
        if value and len(value) > 255:
            raise ValueError("Description maximum 255 characters 📛")
        return value
    
    @validator("date")
    def validate_date(value):
        if value is None:
            raise ValueError("Date schedule should be filled 📛")
        if value < datetime.now():
            raise ValueError("Date schedule has already been missed 📛")
        return value
    
    @validator("location")
    def validate_location(value):
        if (not value or len(value) == 0):
            raise ValueError("Location is required 📛")
        if len(value) > 255:
            raise ValueError("Location maximum 255 characters 📛")
        return value
    
    @validator("partner")
    def validate_partner(value):
        if not value:
            raise ValueError("Partner is required 📛")
        return value

class DateValidator():
    """ Validate here """
    def validate_add_date(self, request):
        try:
            DateValidatorSchema(
                description=request.get("description"),
                date=request.get("date"),
                location=request.get("location"),
                partner=request.get("partner"),
            )
            return Utils.Response(
                is_success=True,
                message=None,
                data=None,
            )
        except ValidationError as e:
            return Utils.Response(
                is_success=False,
                message=e.errors()[0].get("msg"),
                data=None
            )
