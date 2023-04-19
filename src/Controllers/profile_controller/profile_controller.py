import json
import uuid
import Models
import Utils
import Controllers

from sqlmodel import Session, select


class ProfileController():
    def __init__(self, engine=Utils.Connection.engine):
        self.validator = Controllers.ProfileValidator()
        self.engine = engine

    def add_profile(self, request) -> Utils.Response:
        validate: Utils.Response = self.validator.validate_write_profile(
            request)
        if validate.is_success:
            with Session(self.engine) as session:
                user = Models.ProfileModel(
                    id=str(uuid.uuid1()),
                    role=request.get("role"),
                    name=validate.data.name,
                    hobbies=validate.data.hobbies,
                    mbti=validate.data.mbti,
                    social_media=str(json.dumps({
                        "instagram": validate.data.social_media
                    })),
                )
                session.add(user)
                session.commit()
                return Utils.Response(
                    is_success=True,
                    message=f"{'User' if request.get('role') == Models.RoleEnum.main.value else 'Partner'} {validate.data.name} created successfuly 👍🎉",
                    data=None,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=validate.message,
                data=None,
            )

    def edit_image(self, request) -> Utils.Response:
        validate = self.validator.validate_edit_image(request)
        if validate.is_success:
            with Session(self.engine) as session:
                # Get profile data
                query = select(Models.ProfileModel).where(
                    Models.ProfileModel.id == request.get("id"))
                profile = session.exec(query).one()
                profile.picture = request.get("picture")
                session.add(profile)
                session.commit()
                return Utils.Response(
                    is_success=True,
                    message="Avatar updated successfuly 👍🎉",
                    data=None,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=validate.message,
                data=None,
            )

    def edit_profile(self, request) -> Utils.Response:
        validate = self.validator.validate_write_profile(request)
        if validate.is_success:
            with Session(self.engine) as session:
                query = select(Models.ProfileModel).where(
                    Models.ProfileModel.id == request.get("id"))
                profile = session.exec(query).one()
                profile.name = validate.data.name
                profile.mbti = validate.data.mbti
                profile.hobbies = validate.data.hobbies
                profile.social_media = str(json.dumps({
                    "instagram": validate.data.social_media
                }))
                session.add(profile)
                session.commit()
                return Utils.Response(
                    is_success=True,
                    message="Profile updated successfuly 👍🎉",
                    data=None,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=validate.message,
                data=None,
            )

    def get_user(self) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.ProfileModel).where(
                Models.ProfileModel.role == Models.RoleEnum.main.value)
            profile = session.exec(query).first()

            if not profile:
                return Utils.Response(
                    is_success=False,
                    message=None,
                    data=None,
                )

            if profile.social_media:
                profile.social_media = json.loads(
                    profile.social_media).get("instagram")

            return Utils.Response(
                is_success=True,
                message=None,
                data=profile,
            )

    def get_partners(self) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.ProfileModel).where(
                Models.ProfileModel.role == Models.RoleEnum.partner.value)
            partners = session.exec(query).all()

            for partner in partners:
                if partner.social_media:
                    partner.social_media = json.loads(
                        partner.social_media).get("instagram")

            return Utils.Response(
                is_success=True,
                message=None,
                data=partners
            )

    def get_partner_by_id(self, id: str | None) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.ProfileModel).where(
                Models.ProfileModel.id == id)
            partner = session.exec(query).first()

            if partner and partner.social_media:
                partner.social_media = json.loads(
                    partner.social_media).get("instagram")

            return Utils.Response(
                is_success=True,
                message=None,
                data=partner,
            )

    def get_partner_by_index(self, idx: int) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.ProfileModel).where(
                Models.ProfileModel.index == idx)
            partner = session.exec(query).first()

            if partner and partner.social_media:
                partner.social_media = json.loads(
                    partner.social_media).get("instagram")

            return Utils.Response(
                is_success=True,
                message=None,
                data=partner,
            )

    def delete_partner(self, id: str | None) -> Utils.Response:
        with Session(self.engine) as session:
            query_get_partner = select(Models.ProfileModel).where(
                Models.ProfileModel.id == id)
            partner = session.exec(query_get_partner).first()

            if partner:
                query_get_dates = select(Models.DateModel).where(
                    Models.DateModel.partner_id == partner.index
                )

                dates = session.exec(query_get_dates).all()
                for date in dates:
                    session.delete(date)

            session.delete(partner)
            session.commit()

            # temporary
            return Utils.Response(
                is_success=True,
                message="Parter deleted successfuly 👍🎉",
                data=None,
            )
