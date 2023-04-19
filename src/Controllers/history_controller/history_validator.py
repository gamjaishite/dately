from pydantic import BaseModel, ValidationError, validator
import Utils

class HistoryValidatorSchema(BaseModel):
    rating: int | None = None
    review: str | None = None

    @validator("rating")
    def validate_rating(value):
        if value is not None and (value < 1 or value > 5):
            raise ValueError("Rating should be 1 to 5 📛")
        return value
    
    @validator("review")
    def validate_review(value):
        if value and len(value) > 255:
            raise ValueError("Review maximum 255 characters 📛")
        return value


class HistoryValidator():
    """ Validate here """
    def validate_add_rate(self, request):
        try:
            HistoryValidatorSchema(
                rating=request.get("rating"),
                review=request.get("review"),
            )
            return Utils.Response(
                is_success=True,
                message="Rate and review successfuly added👍",
                data=None,
            )
        except ValidationError as e:
            return Utils.Response(
                is_success=False,
                message=e.errors()[0].get("msg"),
                data=None
            )