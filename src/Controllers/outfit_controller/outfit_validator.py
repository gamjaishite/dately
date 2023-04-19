from pydantic import BaseModel, ValidationError, validator
import Utils


class OutfitValidatorSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    picture: bytes | None = None

    @validator("name")
    def validate_name(value):
        if value == None or value == "":
            raise ValueError("Name is required 📛")
        elif len(value) > 40:
            raise ValueError("Name maximum 40 characters 📛")
        return value
    
    @validator("description")
    def validate_description(value):
        if value != None and len(value) > 255:
            raise ValueError("Description maximum 255 characters 📛")
        return value
    
    @validator("picture")
    def validate_picture(value):
        MAXIMUM_FILE_SIZE = 2e+6
        if value == None:
            raise ValueError("Picture is required 📛")
        elif len(value) > MAXIMUM_FILE_SIZE:
            raise ValueError("Picture is over 2 MB 📛")
        return value


class OutfitValidator():
    def validate_outfit(self, request):
        try:
            OutfitValidatorSchema(
                name=request.get("name"),
                description=request.get("description"),
                picture=request.get("picture"),
            )
            
            return Utils.Response(
                is_success=True,
                message=None,
                data=None
            )
        except ValidationError as e:
            return Utils.Response(
                is_success=False,
                message=e.errors()[0].get("msg"),
                data=None
            )


class OutfitCategoryValidatorSchema(BaseModel):
    name: str

    @validator("name")
    def validate_name(value):
        if value == None or value == "":
            raise ValueError("Category is required 📛")
        elif len(value.split("_")) != 2:
            raise ValueError("Wrong Format in Database 📛")
        elif value.split("_")[0] != "category" and value.split("_")[0] != "color":
            raise ValueError("Wrong Format in Database 📛")
        elif len(value.split("_")[1]) > 30:
            raise ValueError("Category maximum 30 characters 📛")
        return value


class OutfitCategoryValidator():
    def validate_outfit_category(self, request):
        try:
            OutfitCategoryValidatorSchema(
                name=request.get("name")
            )

            return Utils.Response(
                is_success=True,
                message=None,
                data=None
            )
        except ValidationError as e:
            return Utils.Response(
                is_success=False,
                message=e.errors()[0].get("msg"),
                data=None
            )
