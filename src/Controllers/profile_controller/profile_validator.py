from pydantic import BaseModel, ValidationError, validator
import Utils


class ProfileValidatorSchema(BaseModel):
    name: str
    mbti: str | None = None
    hobbies: str | None = None
    social_media: str | None = None

    @validator("name")
    def validate_name(value):
        value = str(value).strip()

        if len(value) > 50:
            raise ValueError("Name maximum 50 characters 📛")
        elif len(value) == 0:
            raise ValueError("Name is required 📛")
        return value

    @validator("mbti")
    def validate_mbti(value):
        if not value or value == '':
            return value
        else:
            value = str(value).strip().upper()

        mbtis = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
        if value not in mbtis:
            raise ValueError("MBTI is not valid 📛")
        return value

    @validator("hobbies")
    def validate_hobbies(value):
        if not value:
            return value
        else:
            value = str(value).strip().lower()

        hobbies = value.split(",")

        if len(hobbies) > 1:
            for hobby in hobbies:
                if hobby.strip() == "":
                    raise ValueError("Hobbies is not valid 📛")
        if len(value) > 100:
            raise ValueError("Hobbies maximum 100 characters 📛")

        return value

    @validator("social_media")
    def validate_social_media(value):
        if not value:
            return value
        else:
            value = str(value).strip()

        if len(value) > 30:
            raise ValueError("Instagram username maximum 30 characters 📛")
        return value


class ProfileValidator():
    MAXIMUM_FILE_SIZE = 2e+6

    def validate_write_profile(self, request):
        try:
            result = ProfileValidatorSchema(
                name=request.get("name"),
                mbti=request.get("mbti"),
                hobbies=request.get("hobbies"),
                social_media=request.get("social_media")
            )
            return Utils.Response(
                is_success=True,
                message=None,
                data=result,
            )
        except ValidationError as e:
            return Utils.Response(
                is_success=False,
                message=e.errors()[0].get("msg"),
                data=None
            )

    def validate_edit_image(self, request):
        if request.get("size") > self.MAXIMUM_FILE_SIZE:
            return Utils.Response(
                is_success=False,
                message="Image",
                data=None
            )
        return Utils.Response(
            is_success=True,
            message=None,
            data=None,
        )
