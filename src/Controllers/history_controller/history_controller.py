import uuid
import Models
import Utils
import Controllers

from sqlmodel import Session, select


class HistoryController():
    def __init__(self, engine=Utils.Connection.engine):
        self.validator = Controllers.HistoryValidator()
        self.engine = engine

    """ Add here... """
        # get all dates if id is None, get certain date if id is not None
    def get_many(self, id = None):
        
        data = None
        if (id is None):
            with Session(self.engine) as session:            
                data = session.exec(select(Models.DateModel).where(Models.DateModel.status == True)).all()
        
        else:
            with Session(self.engine) as session:            
                data = session.exec(select(Models.DateModel).where(Models.DateModel.id == id, Models.DateModel.status == True)).all()
        
        data.sort(key=lambda x: x.date, reverse=True)

        return Utils.Response(
                is_success=True,
                message=None,
                data=data
            )    
    
    # get first date with matching id
    def get_one(self, id):
        with Session(self.engine) as session:    
            return Utils.Response(
                is_success=True,
                message=None,
                data=session.exec(select(Models.DateModel).where(Models.DateModel.id == id, Models.DateModel.status == True)).one()
            )
        
    def deleteHistory(self, id) -> Utils.Response:
        with Session(self.engine) as session:
            date = self.get_one(id)
            session.delete(date.data)
            # session.delete(partner)
            session.commit()

            # temporary
            return Utils.Response(
                is_success=True,
                message="History deleted successfuly 👍🎉",
                data=None,
            )

    def update(self, request) -> Utils.Response:
        validate = self.validator.validate_add_rate(request)
        if validate.is_success:
            try:
                with Session(self.engine) as session:
                    query = select(Models.DateModel).where(Models.DateModel.id == request.get("id") and Models.DateModel.status == True)
                    date = session.exec(query).one()
                    date.status=request.get("status")
                    date.rating=request.get("rating")
                    date.review=request.get("review")

                    session.add(date)
                    session.commit()
                    return Utils.Response( 
                        is_success=True,
                        message=f"History successfuly updated👍",
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