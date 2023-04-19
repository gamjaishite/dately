import uuid
import Models
import Utils
import Controllers
from sqlmodel import Session, select


class OutfitController():
    def __init__(self, engine=Utils.Connection.engine, **kwargs):
        self.validator = Controllers.OutfitValidator()
        self.engine = engine


    # Add New Outfit to Database
    def create(self, request) -> Utils.Response:
        validation = self.validator.validate_outfit(request)

        if validation.is_success:
            with Session(self.engine) as session:
                outfit = Models.OutfitModel(
                    id=str(uuid.uuid1()),
                    name=request.get("name"),
                    description=request.get("description"),
                    picture=request.get("picture"),
                )

                session.add(outfit)
                session.commit()

                return Utils.Response(
                    is_success=True,
                    message="Outfit successfully added 👍",
                    data=outfit.index,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=validation.message,
                data=None,
            )
    

    # Update Outfit in Database
    def update(self, id, request) -> Utils.Response:
        validation = self.validator.validate_outfit(request)

        if validation.is_success:
            with Session(self.engine) as session:
                outfit = self.get_one(id).data
                outfit.name = request.get("name")
                outfit.description = request.get("description")
                outfit.picture = request.get("picture")

                session.add(outfit)
                session.commit()

                return Utils.Response(
                    is_success=True,
                    message="Outfit successfully updated 👍",
                    data=outfit.index,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=validation.message,
                data=None,
            )
    

    # Delete Outfit in Database
    def delete(self, id) -> Utils.Response:
        get = self.get_one(id)

        if get.is_success:
            with Session(self.engine) as session:
                outfit = get.data
                
                session.delete(outfit)
                session.commit()

                return Utils.Response(
                    is_success=True,
                    message="Outfit successfully deleted 👍",
                    data=None,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=get.message,
                data=None,
            )
    

    # Add Outfit-Outfit Category Relationship to Database
    def create_relationship(self, request) -> Utils.Response:
        # Prereq: Outfit and Outfit Category must exist in database
        with Session(self.engine) as session:
            outfit_category_join = Models.OutfitCategoryJoinModel(
                outfit_id=request.get("outfit_id"),
                category_id=request.get("category_id"),
            )

            session.add(outfit_category_join)
            session.commit()
            
            return Utils.Response(
                is_success=True,
                message="Outfit-Category relationship successfully added 👍",
                data=None,
            )
    

    # Update Outfit-Outfit Category Relationship
    def update_relationship(self, request) -> Utils.Response:
        # Prereq: Outfit and Outfit Category must exist in database
        with Session(self.engine) as session:
            getCategory = session.exec(select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.index == request.get("category_id"))).first()
            
            if getCategory is not None:
                category_type = getCategory.name.split("_")[0]
            else:
                category_type = None

            query = select(Models.OutfitCategoryJoinModel).where(Models.OutfitCategoryJoinModel.outfit_id == request.get("outfit_id"))
            outfit_category_join = session.exec(query).all()

            for category in outfit_category_join:
                category_data = session.exec(select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.index == category.category_id)).first()
                
                if category_type == None or category_data.name.split("_")[0] == category_type:
                    category.category_id = request.get("category_id")
                    
                    session.add(category)
                    session.commit()
                    
            return Utils.Response(
                is_success=True,
                message="Outfit-Category relationship successfully updated 👍",
                data=None,
            )
    

    # Delete Outfit-Outfit Category Relationship
    def delete_relationship(self, request) -> Utils.Response:
        # Prereq: Outfit and Outfit Category must exist in database
        with Session(self.engine) as session:
            query = select(Models.OutfitCategoryJoinModel).where(Models.OutfitCategoryJoinModel.outfit_id == request.get("outfit_id"))
            outfit_category_join = session.exec(query).all()

            for category in outfit_category_join:
                if request.get("category_id") == category.category_id or request.get("category_id") == None:
                    session.delete(category)
            session.commit()
            
            return Utils.Response(
                is_success=True,
                message="Outfit-Category relationship successfully deleted 👍",
                data=None,
            )
    

    # Get Outfit Categories by Outfit ID
    def get_categories(self, id) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.OutfitCategoryJoinModel).where(Models.OutfitCategoryJoinModel.outfit_id == self.get_one(id).data.index)
            outfit_category_join = session.exec(query).all()

            categories = []
            for category in outfit_category_join:
                category_data = session.exec(select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.index == category.category_id)).first()
                categories.append(category_data)
            
            return Utils.Response(
                is_success=True,
                message="Outfit Categories successfully retrieved 👍",
                data=categories,
            )


    # Get All Outfits
    def get_all(self) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.OutfitModel)
            outfits = session.exec(query).all()

            return Utils.Response(
                is_success=True,
                message="Outfits successfully retrieved 👍",
                data=outfits,
            )
    

    def get_all_filtered(self, category=None, color=None) -> Utils.Response:
        outfits = self.get_all().data
        # print(data)

        if category:
            for i in range(len(outfits) - 1, -1, -1):
                categories = self.get_categories(outfits[i].id).data
                
                if "category_" + category not in [category.name for category in categories]:
                    outfits.pop(i)
        
        if color:
            for i in range(len(outfits) - 1, -1, -1):
                categories = self.get_categories(outfits[i].id).data

                if "color_" + color not in [category.name for category in categories]:
                    outfits.pop(i)

        return Utils.Response(
            is_success=True,
            message="Outfits successfully retrieved 👍",
            data=outfits,
        )

    
    # Get Outfit by ID
    def get_one(self, id) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.OutfitModel).where(Models.OutfitModel.id == id)
            outfit = session.exec(query).first()

            if outfit:
                return Utils.Response(
                    is_success=True,
                    message="Outfit successfully retrieved 👍",
                    data=outfit,
                )
            else:
                return Utils.Response(
                    is_success=False,
                    message="Outfit not found",
                    data=None,
                )
    

    # Get Outfit by Index
    def get_one_by_index(self, index) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.OutfitModel).where(Models.OutfitModel.index == index)
            outfit = session.exec(query).first()

            if outfit:
                return Utils.Response(
                    is_success=True,
                    message="Outfit successfully retrieved 👍",
                    data=outfit,
                )
            else:
                return Utils.Response(
                    is_success=False,
                    message="Outfit not found",
                    data=None,
                )


class OutfitCategoryController():
    def __init__(self, engine=Utils.Connection.engine, **kwargs):
        self.validator = Controllers.OutfitCategoryValidator()
        self.engine = engine

    
    # Add New Outfit Category to Database
    def create(self, request) -> Utils.Response:
        validation = self.validator.validate_outfit_category(request)

        if validation.is_success:
            with Session(self.engine) as session:
                outfit_category = Models.OutfitCategoryModel(
                    id=str(uuid.uuid1()),
                    name=request.get("name"),
                )

                session.add(outfit_category)
                session.commit()

                return Utils.Response(
                    is_success=True,
                    message="Outfit Category successfully added 👍",
                    data=outfit_category.index,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=validation.message,
                data=None,
            )
    

    # Refresh Category Table by Delete Unused Categories
    def refreshTable(self) -> Utils.Response:
        with Session(self.engine) as session:
            query = select(Models.OutfitCategoryModel)
            categories = session.exec(query).all()

            for category in categories:
                query = select(Models.OutfitCategoryJoinModel).where(Models.OutfitCategoryJoinModel.category_id == category.index)
                outfit_category_join = session.exec(query).all()

                if len(outfit_category_join) == 0:
                    session.delete(category)
            session.commit()

            return Utils.Response(
                is_success=True,
                message="Outfit Categories successfully refreshed 👍",
                data=None,
            )


    # Delete Outfit Category in Database
    def delete(self, id) -> Utils.Response:
        get = self.get_category(id)

        if get.is_success:
            with Session(self.engine) as session:
                outfit_category = get.data
                
                session.delete(outfit_category)
                session.commit()

                return Utils.Response(
                    is_success=True,
                    message="Outfit Category successfully deleted 👍",
                    data=None,
                )
        else:
            return Utils.Response(
                is_success=False,
                message=get.message,
                data=None,
            )


    # Get All Outfit Categories
    def get_all_categories(self) -> Utils.Response:
        with Session(self.engine) as session:
            # Return categories where name starts with "category_"
            query = select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.name.startswith("category_"))
            categories = session.exec(query).all()

            return Utils.Response(
                is_success=True,
                message="Categories successfully retrieved 👍",
                data=categories,
            )
            

    # Get All Outfit Colors
    def get_all_colors(self) -> Utils.Response:
        with Session(self.engine) as session:
            # Return categories where name starts with "color_"
            query = select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.name.startswith("color_"))
            colors = session.exec(query).all()

            return Utils.Response(
                is_success=True,
                message="Colors successfully retrieved 👍",
                data=colors,
            )
    

    # Get Category Index by Name
    def get_category_index(self, name) -> Utils.Response:
        with Session(self.engine) as session:
            # Return category id where name is equal to name
            query = select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.name == name)
            category = session.exec(query).first()

            if category:
                return Utils.Response(
                    is_success=True,
                    message="Category index successfully retrieved 👍",
                    data=category.index,
                )
            else:
                return Utils.Response(
                    is_success=False,
                    message="Category not found",
                    data=None,
                )


    # Get Category by Id
    def get_category(self, id) -> Utils.Response:
        with Session(self.engine) as session:
            # Return category where id is equal to id
            query = select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.id == id)
            category = session.exec(query).first()

            if category:
                return Utils.Response(
                    is_success=True,
                    message="Category successfully retrieved 👍",
                    data=category,
                )
            else:
                return Utils.Response(
                    is_success=False,
                    message="Category not found",
                    data=None,
                )
            
    
    # Get Category by Index
    def get_category_by_index(self, index) -> Utils.Response:
        with Session(self.engine) as session:
            # Return category where index is equal to index
            query = select(Models.OutfitCategoryModel).where(Models.OutfitCategoryModel.index == index)
            category = session.exec(query).first()

            if category:
                return Utils.Response(
                    is_success=True,
                    message="Category successfully retrieved 👍",
                    data=category,
                )
            else:
                return Utils.Response(
                    is_success=False,
                    message="Category not found",
                    data=None,
                )
