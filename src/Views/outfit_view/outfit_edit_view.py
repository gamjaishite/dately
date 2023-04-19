import flet as ft
import Utils
from Utils.components.navbar import Navbar
from Utils.components.notification import Notification
from Controllers.outfit_controller.outfit_controller import OutfitController, OutfitCategoryController


class OutfitEditView(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__()
        self.page = page
        self.mode = "Create"
        if kwargs.get("id"):
            self.id = kwargs.get("id")
            self.mode = "Edit"

        # Controllers
        self.outfitController = OutfitController()
        self.outfitCategoryController = OutfitCategoryController()

        # Styles Data
        self.headerHeight = 75
        self.textStyle = ft.TextStyle(
                font_family="ShantellSans-SemiBold",
                size=14,
                color="#A1A1AA"
            )
        self.hintStyle = ft.TextStyle(
            font_family="ShantellSans-SemiBold",
            size=14,
            color="#A1A1AA"
        )

        # Component Refs
        self.nameForm = ft.Ref[ft.TextField]()
        self.categoryDropdown = ft.Ref[ft.Dropdown]()
        self.newCategoryForm = ft.Ref[ft.TextField]()
        self.colorDropdown = ft.Ref[ft.Dropdown]()
        self.newColorForm = ft.Ref[ft.TextField]()
        self.noteForm = ft.Ref[ft.TextField]()
        self.picture = ft.Ref[ft.Image]()

        # Other Attributes
        self.pictureData = None


    def build(self):
        page = self.getOutfitEditPage()

        # Update Attributes for Edit
        if self.mode == "Edit":
            outfit = self.outfitController.get_one(self.id)
            self.nameForm.current.value = outfit.data.name
            self.noteForm.current.value = outfit.data.description
            self.pictureData = outfit.data.picture
            self.picture.current.src_base64 = Utils.blob_to_base64(self.pictureData)

            getCategory = self.outfitController.get_categories(self.id)
            if getCategory.is_success and len(getCategory.data) > 0:
                for category in getCategory.data:
                    if category.name.startswith("category_"):
                        self.categoryDropdown.current.value = category.name.split("_")[1]
                    else:
                        self.colorDropdown.current.value = category.name.split("_")[1]
        else:
            self.pictureData = None
            image_path = "Assets/Images/OutfitDefault.png"
            with open(image_path, 'rb') as f:
                blob = f.read()
            self.picture.current.src_base64 = Utils.blob_to_base64(blob)

        return page
    

    # View Methods
    def getOutfitEditPage(self):
        return ft.Stack(
            controls=[
                ft.Container(
                    bgcolor="#FFFFFF",
                    width=self.getPageWidth(),
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            self.getHeader(),
                            ft.Row(
                                controls=[
                                    self.getFormsView(),
                                    self.getPictureFormView(),
                                ]
                            ),
                        ]
                    ),
                    padding=20
                ),
                self.getButtons()
            ]
        )
    

    def getHeader(self):
        return ft.Container(
            height=self.headerHeight,
            content=ft.Text(
                value="Outfits",
                font_family="ShantellSans-SemiBold",
                size=40,
                color="#F472B6",
            )
        )
    

    def getFormsView(self):
        forms = ft.Container(
            width=self.getPageWidth() * 0.6,
            content=ft.Column(
                height=self.page.height - 200,
                controls=[
                    self.getNameForm(),
                    self.getCategoryDropdown(),
                    self.getNewCategoryForm(),
                    self.getColorDropdown(),
                    self.getNewColorForm(),
                    self.getNoteForm()
                ],
                scroll="auto"
            )
        )

        return forms
    

    def getNameForm(self):
        desc = ft.Text(
            value="Name",
            font_family="ShantellSans-SemiBold",
            size=14,
            color="#FBCFE8"
        )

        form = ft.TextField(
            ref=self.nameForm,
            hint_text="Insert Outfit Name",
            hint_style=self.hintStyle,
            text_style=self.textStyle,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=10,
        )
        
        return ft.Column(
            controls=[
                desc,
                form
            ]
        )
    

    def getCategoryDropdown(self):
        desc = ft.Text(
            value="Category",
            font_family="ShantellSans-SemiBold",
            size=14,
            color="#FBCFE8"
        )

        options = ft.Dropdown(
            ref=self.categoryDropdown,
            height=60,
            width=240,
            filled=True,
            bgcolor="#FAFAFA",
            color="#A1A1AA",
            border_radius=10,
            border_width=0,
            hint_style=self.hintStyle,
            text_style=self.textStyle,
            alignment=ft.alignment.top_left,
            content_padding=15,
            on_change=lambda _:self.resetNewCategory()
        )

        getCategories = self.outfitCategoryController.get_all_categories()
        if getCategories.is_success and getCategories.data:
            options.hint_text = "Select Category"
            for category in getCategories.data:
                options.options.append(ft.dropdown.Option(category.name.split("_")[1]))
        else:
            options.hint_text = "No Categories Found"
            options.options.append(ft.dropdown.Option("No Categories Found"))

        return ft.Column(
            controls=[
                desc,
                options
            ]
        )
    

    def getNewCategoryForm(self):
        desc = ft.Text(
            value="or Add New Category",
            font_family="ShantellSans-SemiBold",
            size=14,
            color="#FBCFE8"
        )

        form = ft.TextField(
            ref=self.newCategoryForm,
            hint_text="Add New Category",
            hint_style=self.hintStyle,
            text_style=self.textStyle,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=10,
            on_change=lambda _:self.resetCategory(),
        )
        
        return ft.Column(
            controls=[
                desc,
                form
            ]
        )


    def getColorDropdown(self):
        desc = ft.Text(
            value="Color",
            font_family="ShantellSans-SemiBold",
            size=14,
            color="#FBCFE8"
        )

        options = ft.Dropdown(
            ref=self.colorDropdown,
            height=60,
            width=240,
            filled=True,
            bgcolor="#FAFAFA",
            color="#A1A1AA",
            border_radius=10,
            border_width=0,
            hint_style=self.hintStyle,
            text_style=self.textStyle,
            alignment=ft.alignment.top_left,
            content_padding=15,
            on_change=lambda _:self.resetNewColor(),
        )

        getColors = self.outfitCategoryController.get_all_colors()
        if getColors.is_success and getColors.data:
            options.hint_text = "Select Color"
            for color in getColors.data:
                options.options.append(ft.dropdown.Option(color.name.split("_")[1]))
        else:
            options.hint_text = "No Colors Found"
            options.options.append(ft.dropdown.Option("No Colors Found"))

        return ft.Column(
            controls=[
                desc,
                options
            ]
        )
    

    def getNewColorForm(self):
        desc = ft.Text(
            value="or Add New Color",
            font_family="ShantellSans-SemiBold",
            size=14,
            color="#FBCFE8"
        )

        form = ft.TextField(
            ref=self.newColorForm,
            hint_text="Add New Color",
            hint_style=self.hintStyle,
            text_style=self.textStyle,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=10,
            on_change=lambda _:self.resetColor(),
        )
        
        return ft.Column(
            controls=[
                desc,
                form
            ]
        )


    def getNoteForm(self):
        desc = ft.Text(
            value="Note",
            font_family="ShantellSans-SemiBold",
            size=14,
            color="#FBCFE8"
        )

        form = ft.TextField(
            ref=self.noteForm,
            hint_text="Add Note",
            hint_style=self.hintStyle,
            text_style=self.textStyle,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=10,
            multiline=True
        )
        
        return ft.Column(
            controls=[
                desc,
                form
            ]
        )


    def getPictureFormView(self):
        self.image_file_picker = ft.FilePicker(
            on_result=self.get_image,
        )
        self.page.overlay.append(self.image_file_picker)

        pictureForm = ft.Container(
            alignment=ft.alignment.center,
            width=self.getPageWidth() * 0.4,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        ref=self.picture,
                        width=300,
                        height=400,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.TextButton(
                        content=ft.Text(
                            value="change",
                            size=20,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                                ft.MaterialState.HOVERED: "#FDF2F8",
                            },
                            overlay_color={
                                ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                            },
                            color="#F9A8D4"
                        ),
                        on_click=lambda _: self.image_file_picker.pick_files(
                            allow_multiple=False,
                            allowed_extensions=["png", "jpg"],
                        )
                    )
                ]
            )
        )

        return pictureForm
    

    def getButtons(self):
        return ft.Container(
            bottom=25,
            width=self.getPageWidth(),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    self.getCancelButton(),
                    self.getSaveButton(),
                    # self.getTestButton(),
                ]
            )
        )
    

    def getCancelButton(self):
        return ft.TextButton(
            height=50,
            width=140,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.MaterialState.HOVERED: "#E4E4E7",
                    ft.MaterialState.DEFAULT: "#FAFAFA",
                },
                color={
                    ft.MaterialState.DEFAULT: "#A1A1AA",
                    ft.MaterialState.HOVERED: "#52525B"
                },
                overlay_color=ft.colors.TRANSPARENT,
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                        radius=10)
                },
                side=ft.BorderSide(5, "#E4E4E7"),
            ),
            content=ft.Text(
                value="CANCEL",
                weight=ft.FontWeight.W_600,
                size=24,
            ),
            on_click=lambda _: self.cancelButtonAction(),
        )
    
    
    def getSaveButton(self):
        return ft.TextButton(
            height=50,
            width=140,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.MaterialState.HOVERED: "#FBCFE8",
                    ft.MaterialState.DEFAULT: "#FDF2F8",
                },
                color={
                    ft.MaterialState.DEFAULT: "#F472B6",
                    ft.MaterialState.HOVERED: "#52525B"
                },
                overlay_color=ft.colors.TRANSPARENT,
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                        radius=10)
                },
                side=ft.BorderSide(5, "#FBCFE8"),
            ),
            content=ft.Text(
                value="SAVE",
                weight=ft.FontWeight.W_600,
                size=24,
            ),
            on_click=lambda _:self.saveButtonAction(),
        ) 

    # Reset Methods    
    def resetCategory(self):
        self.categoryDropdown.current.value = None
        self.categoryDropdown.current.update()

    
    def resetNewCategory(self):
        if self.categoryDropdown.current.value == "No Categories Found":
            self.resetCategory()
        else:
            self.newCategoryForm.current.value = None
            self.newCategoryForm.current.update()

    
    def resetColor(self):
        self.colorDropdown.current.value = None
        self.colorDropdown.current.update()

    
    def resetNewColor(self):
        if self.colorDropdown.current.value == "No Colors Found":
            self.resetColor()
        else:
            self.newColorForm.current.value = None
            self.newColorForm.current.update()


    # Response Methods
    def cancelButtonAction(self):
        if self.mode == "Create":
            self.page.snack_bar = Notification(f"Outfit Creation is Cancelled!")
        else:
            self.page.snack_bar = Notification(f"Outfit Edit is Cancelled!")
        self.page.go("/outfits")

    
    def saveButtonAction(self):
        if self.mode == "Create":
            outfitRequest = {
                "name": self.nameForm.current.value,
                "description": self.noteForm.current.value,
                "picture": self.pictureData,
            }
            outfitResp = self.outfitController.create(request=outfitRequest)
            success = outfitResp.is_success

            outfitCategory = self.categoryDropdown.current.value if self.categoryDropdown.current.value else self.newCategoryForm.current.value
            if success and outfitCategory:
                outfitCategory = "category_" + outfitCategory
                categoryIndex = self.outfitCategoryController.get_category_index(outfitCategory).data

                if categoryIndex != None:
                    success = True
                else:
                    categRequest = {
                        "name": outfitCategory,
                    }
                    categResp = self.outfitCategoryController.create(request=categRequest)
                    success = success and categResp.is_success
                    categoryIndex = categResp.data

                if success:
                    relationRequest = {
                        "outfit_id": outfitResp.data,
                        "category_id": categoryIndex,
                    }
                    relationResp = self.outfitController.create_relationship(request=relationRequest)
                    success = success and relationResp.is_success

            outfitColor = self.colorDropdown.current.value if self.colorDropdown.current.value else self.newColorForm.current.value
            if success and outfitColor:
                outfitColor = "color_" + outfitColor
                colorIndex = self.outfitCategoryController.get_category_index(outfitColor).data

                if colorIndex != None:
                    success = True
                else:
                    colorRequest = {
                        "name": outfitColor,
                    }
                    colorResp = self.outfitCategoryController.create(request=colorRequest)
                    success = success and colorResp.is_success
                    colorIndex = colorResp.data

                if success:
                    relationRequest = {
                        "outfit_id": outfitResp.data,
                        "category_id": colorIndex,
                    }
                    relationResp = self.outfitController.create_relationship(request=relationRequest)
                    success = success and relationResp.is_success

            self.page.snack_bar = Notification(outfitResp.message)
            self.page.update()

            if success:
                self.page.go("/outfits")
        else:
            outfitRequest = {
                "name": self.nameForm.current.value,
                "description": self.noteForm.current.value,
                "picture": self.pictureData,
            }
            outfitResp = self.outfitController.update(id=self.id, request=outfitRequest)
            success = outfitResp.is_success

            outfitCategory = self.categoryDropdown.current.value if self.categoryDropdown.current.value else self.newCategoryForm.current.value
            if outfitCategory:
                outfitCategory = "category_" + outfitCategory
                categoryIndex = self.outfitCategoryController.get_category_index(outfitCategory).data

                if categoryIndex != None:
                    success = True
                else:
                    categRequest = {
                        "name": outfitCategory,
                    }
                    categResp = self.outfitCategoryController.create(request=categRequest)
                    success = success and categResp.is_success
                    categoryIndex = categResp.data

                if success:
                    relationRequest = {
                        "outfit_id": outfitResp.data,
                        "category_id": categoryIndex,
                    }
                    relationResp = self.outfitController.update_relationship(request=relationRequest)
                    success = success and relationResp.is_success

            outfitColor = self.colorDropdown.current.value if self.colorDropdown.current.value else self.newColorForm.current.value
            if outfitColor:
                outfitColor = "color_" + outfitColor
                colorIndex = self.outfitCategoryController.get_category_index(outfitColor).data

                if colorIndex != None:
                    success = True
                else:
                    colorRequest = {
                        "name": outfitColor,
                    }
                    colorResp = self.outfitCategoryController.create(request=colorRequest)
                    success = success and colorResp.is_success
                    colorIndex = colorResp.data

                if success:
                    relationRequest = {
                        "outfit_id": outfitResp.data,
                        "category_id": colorIndex,
                    }
                    relationResp = self.outfitController.update_relationship(request=relationRequest)
                    success = success and relationResp.is_success

            self.page.snack_bar = Notification(outfitResp.message)
            self.page.update()
            self.outfitCategoryController.refreshTable()

            if success:
                self.page.go("/outfits")
        

    # Other Methods
    def getPageWidth(self):
        return self.page.width - Navbar.width - 40
    

    def get_image(self, e: ft.FilePickerResultEvent):
        if e.files:
            image_path = e.files[0].path
            with open(image_path, 'rb') as f:
                blob = f.read()

            self.pictureData = blob
            self.picture.current.src_base64 = Utils.blob_to_base64(blob)
            self.picture.current.update()
