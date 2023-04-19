import flet as ft
from Utils.components.navbar import Navbar
from Utils.components.notification import Notification
from Utils.components.outfitList import OutfitList, OutfitListConfig, OutfitListStyle
from Utils.components.deletePopup import DeletePopup

class OutfitView(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__()
        self.page = page

        # Component Refs
        self.contents = ft.Ref[ft.Column]()
        self.categoryDropdown = ft.Ref[ft.Dropdown]()
        self.colorDropdown = ft.Ref[ft.Dropdown]()
        self.dropdowns = ft.Ref[ft.Row]()
        self.outfit_list_component = None

        # Styles Data
        self.headerHeight = 75
        self.dropdownHeight = 100
        self.trashIcon = "\uf2ed;"
        self.editIcon = "\uf044;"
    
    
    def build(self):
        # Attribute
        self.isFiltered = False
        self.deletePopup = DeletePopup()
        
        return self.getOutfitPage()
    

    # View Methods
    def getOutfitPage(self):
        addButton = self.getAddButton()

        self.outfit_list_component = OutfitList(
            page=self.page,
            config=OutfitListConfig(
                style=OutfitListStyle(
                    pageWidth=self.getPageWidth(),
                    heightOffset= self.headerHeight + 20,
                ),
                editMode=True,
                contentRef=self.contents,
                categoryDropdownRef=self.categoryDropdown,
                colorDropdownRef=self.colorDropdown,
                dropdownsRef=self.dropdowns,
                editButtonAction=self.editButtonAction,
                deleteButtonAction=self.showDeletePopUp,
            )
        )

        outfitDisplay = ft.Container(
            bgcolor="#FFFFFF",
            width=self.getPageWidth(),
            content=ft.Column(
                ref=self.contents,
                spacing=0,
                controls=[
                    self.deletePopup,
                    self.getHeader(),
                    self.outfit_list_component
                ]
            )
        )

        return ft.Container(
            content=ft.Stack(
                controls=[
                    outfitDisplay,
                    addButton
                ]
            ),
            padding=20
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

    def getAddButton(self):
        return ft.IconButton(
            content=ft.Text(
                "\u002b;",
                font_family="FontAwesome",
                color="#F472B6",
                size=30,
                text_align="center"
            ),
            height=60,
            width=60,
            right=50,
            bottom=10,
            style=ft.ButtonStyle(
                bgcolor="#FDF2F8",
                padding=0,
                side=ft.border.BorderSide(5, color="#F9A8D4")
            ),
            on_click=lambda _:self.addOutfitButtonAction()
        )
    

    def showDeletePopUp(self, data):
        self.deletePopup.show(lambda: self.deleteButtonAction(data), title="Delete Outfit", actionTitle="Delete")
    

    # Other Methods
    def getPageWidth(self):
        return self.page.width - Navbar.width


    def addOutfitButtonAction(self):
        self.page.go("/outfits/edit")

    
    def editButtonAction(self, data):
        self.page.go(f"/outfits/edit/{data.id}")


    def deleteButtonAction(self, data):
        resp = self.outfit_list_component.outfitController.delete(data.id)
        self.outfit_list_component.outfitCategoryController.refreshTable()
        self.page.snack_bar = Notification(resp.message)

        self.outfit_list_component.outfitsRequest = self.outfit_list_component.outfitController.get_all()
        self.contents.current.controls = [self.contents.current.controls[0], self.outfit_list_component.getOutfitCards()]
        self.contents.current.update()
        
        self.outfit_list_component.refreshDropdown()
        if self.categoryDropdown.current.options[0].key == "No Categories Found" and self.colorDropdown.current.options[0].key == "No Colors Found":
            self.outfit_list_component.clearFilterAction()

        self.outfit_list_component.update()
        self.page.update()
    