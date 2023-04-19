import uuid
import Models
import Utils
import Controllers
from sqlmodel import Session, select
from Controllers.profile_controller.profile_controller import ProfileController
import json

class DateController():
    def __init__(self, engine=Utils.Connection.engine, **kwargs):
        self.validator = Controllers.DateValidator()
        self.engine = engine
        self.profileController = ProfileController(engine)

    # add new date to database
    def create(self, request):

        validate = self.validator.validate_add_date(request)

        if validate.is_success:
            try:
                with Session(self.engine) as session:

                    partner = request.get("partner")
                    partner.social_media = str(json.dumps({
                        "instagram": partner.social_media
                    }))

                    date = Models.DateModel(
                        id=str(uuid.uuid1()),
                        description=request.get("description"),
                        date=request.get("date"),
                        location=request.get("location"),
                        status=False,
                        rating=None,
                        review=None,
                        partner=partner,
                        outfits=request.get("outfits")
                    )

                    session.add(date)
                    session.commit()

                    return Utils.Response(
                        is_success=True,
                        message=f"Date successfuly added👍",
                        data=None
                    )
                
            except BaseException as e:
                return Utils.Response (
                    is_success=False,
                    message=e.args[0],
                    data=None
                )
        else:
            return Utils.Response(
                is_success=False,
                message=validate.message,
                data=None
            )
    
    # get all dates if id is None, get certain date if id is not None
    def get_many(self, id = None):
        
        try:
            data = None

            if (id is None):
                with Session(self.engine) as session:            
                    data = session.exec(select(Models.DateModel).where(Models.DateModel.status == False)).all()
            
            else:
                with Session(self.engine) as session:            
                    data = session.exec(select(Models.DateModel).where(Models.DateModel.id == id, Models.DateModel.status == False)).all()

            for date in data:
                fetchPartnerResponse = self.profileController.get_partner_by_index(date.partner_id)

                if (fetchPartnerResponse.is_success):
                    date.partner = fetchPartnerResponse.data

                else:
                    return Utils.Response(
                        is_success=False,
                        message=fetchPartnerResponse.message,
                        data=None
                    )
                
            data.sort(key=lambda x: x.date)
                
            return Utils.Response(
                is_success=True,
                message= f"Dates successfuly fetched👍",
                data=data
            )
            
        except BaseException as e:
            return Utils.Response(
                is_success=False,
                message=e.args[0],
                data=None
            )

    # get first date with matching id
    def get_one(self, id, includePartner=True, includeOutfits=False):

        try:
            with Session(self.engine) as session:  

                data = session.exec(select(Models.DateModel).where(Models.DateModel.id == id, Models.DateModel.status == False)).one()

                if (includePartner):
                    fetchPartnerResponse = self.profileController.get_partner_by_index(data.partner_id)

                    if (fetchPartnerResponse.is_success):
                        data.partner = fetchPartnerResponse.data

                    else:
                        return Utils.Response(
                            is_success=False,
                            message=fetchPartnerResponse.message,
                            data=None
                        )
                    
                if (includeOutfits):
                    outfitsRelationship = session.exec(select(Models.OutfitDateJoinModel).where(Models.OutfitDateJoinModel.date_id == data.index)).all()

                    outfits = []
                    for relationship in outfitsRelationship:
                        outfits.append(session.exec(select(Models.OutfitModel).where(Models.OutfitModel.index == relationship.outfit_id)).one())

                    data.outfits = outfits
                    
                return Utils.Response(
                    is_success=True,
                    message= f"Date successfuly fetched👍",
                    data=data
                )
            
        except BaseException as e:
            return Utils.Response(
                is_success=False,
                message=e.args[0],
                data=None
            )
    
    # edit certain date
    def update(self, request):

        validate = self.validator.validate_add_date(request)
        if validate.is_success:
            try:
                with Session(self.engine) as session:

                    partner = request.get("partner")
                    partner.social_media = str(json.dumps({
                        "instagram": partner.social_media
                    }))
                    
                    # date = res.data
                    date = session.exec(select(Models.DateModel).where(Models.DateModel.id == request.get("id"), Models.DateModel.status == False)).first()
                    date.description = request.get("description")
                    date.date=request.get("date")
                    date.location=request.get("location")
                    date.partner=partner

                    date.outfits.clear()

                    session.add(date)
                    session.commit()

                    for outfit in request.get("outfits"):
                        date.outfits.append(outfit)

                    session.add(date)
                    session.commit()

                    return Utils.Response(
                        is_success=True,
                        message=f"Date successfuly edited👍",
                        data=None
                    )
                
            except BaseException as e:
                return Utils.Response(
                    is_success=False,
                    message=e.args[0],
                    data=None
                )
        
        else:
            return Utils.Response(
                is_success=False,
                message=validate.message,
                data=None
            )
        
    def finish_date(self, id):

        try:
            with Session(self.engine) as session:
                
                # date = res.data
                date = session.exec(select(Models.DateModel).where(Models.DateModel.id == id, Models.DateModel.status == False)).one()

                if (not date):
                    return Utils.Response(
                        is_success=False,
                        message="Date not found or already finished!",
                        data=None
                    )
                
                date.status = True

                session.add(date)
                session.commit()

                return Utils.Response(
                    is_success=True,
                    message=f"Date successfuly finished👍",
                    data=None
                )
            
        except BaseException as e:
            return Utils.Response(
                is_success=False,
                message=e.args[0],
                data=None
            )
    

    def delete(self, id):
        try:
            with Session(self.engine) as session:
                res = self.get_one(id, includePartner=False)

                if (not res.is_success):
                    return Utils.Response(
                        is_success=False,
                        message=res.message,
                        data=None
                    )
                
                date = self.get_one(id, includePartner=False).data
                session.delete(date)
                session.commit()

                return Utils.Response(
                    is_success=True,
                    message=f"Date successfuly deleted👍",
                    data=None
                )
        except BaseException as e:
            return Utils.Response(
                is_success=False,
                message=e.args[0],
                data=None
            )
        

