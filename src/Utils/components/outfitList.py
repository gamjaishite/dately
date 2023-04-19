
import flet as ft
import Utils
from Models.outfit_model.outfit_model import OutfitModel
from Controllers.outfit_controller.outfit_controller import OutfitController, OutfitCategoryController
from typing import List, Callable

class OutfitListStyle():
    def __init__(
            self,
            pageWidth,
            heightOffset: int = 0,
            widthOffset: int = 20,
            leftDropDownWidth: int = 200,
        ):

        self.pageWidth = pageWidth
        self.heightOffset = heightOffset
        self.widthOffset = widthOffset
        self.leftDropDownWidth = leftDropDownWidth
        
    
class OutfitListConfig():


    def __init__(
                self, 
                style: OutfitListStyle,
                contentRef: ft.Ref[ft.Column] = ft.Ref[ft.Column](),
                categoryDropdownRef: ft.Ref[ft.Dropdown] = ft.Ref[ft.Dropdown](),
                colorDropdownRef: ft.Ref[ft.Dropdown] = ft.Ref[ft.Dropdown](),
                dropdownsRef: ft.Ref[ft.Row] = ft.Ref[ft.Row](),
                selectedCountRef: ft.Ref[ft.Text] = ft.Ref[ft.Text](),
                editMode: bool = False,
                selectMode: bool = False,
                selectedOutfits: List[OutfitModel] = [],
                editButtonAction: Callable[[OutfitModel], None] = lambda _ : None,
                deleteButtonAction: Callable[[OutfitModel], None] = lambda _ : None,
                selectAction: Callable[[ft.ControlEvent,OutfitModel], None] | None = None,

                **kwargs
            ):
        
        self.style = style
        self.editMode = editMode
        self.selectMode = selectMode
        self.editButtonAction = editButtonAction
        self.deleteButtonAction = deleteButtonAction
        self.selectAction = selectAction
        self.selectedOutfits = selectedOutfits
        # refs
        self.contentRef = contentRef
        self.categoryDropdownRef = categoryDropdownRef
        self.colorDropdownRef = colorDropdownRef
        self.dropdownsRef = dropdownsRef
        self.contentRef = contentRef
        self.selectedCountRef = selectedCountRef

class OutfitList(ft.UserControl):

    def __init__(self, page, config: OutfitListConfig, **kwargs):
        super().__init__()
        self.page = page
        self.config = config
        self.outfitCategoryController = OutfitCategoryController()
        self.outfitController = OutfitController()

    def build(self):

        # styles
        self.dropdownHeight = 100
        self.trashIcon = "\uf2ed;"
        self.editIcon = "\uf044;"
        self.selectedBorderWidth = 7

        # data
        self.outfitsRequest = self.outfitController.get_all()
        self.isFiltered = False

        return ft.Column(
            ref=self.config.contentRef,
            controls=[
                self.getDropdowns(),
                self.getOutfitCards()
            ]
        )
    
    def getDropdowns(self):
        categoryDropdown = ft.Dropdown(
            ref=self.config.categoryDropdownRef,
            height=60,
            width=self.config.style.leftDropDownWidth,
            filled=True,
            bgcolor="#F2F2F2",
            color="#A1A1AA",
            border_radius=10,
            border_width=0,
            hint_text="Category",
            hint_style=ft.TextStyle(
                size=14,
                color="#A1A1AA",
                font_family="ShantellSans-SemiBold"
            ),
            text_style=ft.TextStyle(
                size=14,
                color="#A1A1AA",
                font_family="ShantellSans-SemiBold"
            ),
            content_padding=15,
            on_change=lambda _: self.categoryDropdownAction(),
        )

        colorDropdown = ft.Dropdown(
            ref=self.config.colorDropdownRef,
            height=60,
            width=self.config.style.leftDropDownWidth,
            filled=True,
            bgcolor="#F2F2F2",
            color="#A1A1AA",
            border_radius=10,
            border_width=0,
            hint_text="Color",
            hint_style=ft.TextStyle(
                size=14,
                color="#A1A1AA",
                font_family="ShantellSans-SemiBold"
            ),
            text_style=ft.TextStyle(
                size=14,
                color="#A1A1AA",
                font_family="ShantellSans-SemiBold"
            ),
            content_padding=15,
            on_change=lambda _: self.colorDropdownAction(),
        )

        self.refreshDropdown()

        componentHeight = 55
        controls = [
            ft.Row(
                ref=self.config.dropdownsRef,
                height=self.dropdownHeight,
                spacing=20,
                controls=[
                    ft.Container(
                        height=componentHeight,
                        alignment=ft.alignment.top_left,
                        content=categoryDropdown,
                        border_radius=10
                    ),
                    ft.Container(
                        height=componentHeight,
                        alignment=ft.alignment.top_left,
                        content=colorDropdown,
                        border_radius=10
                    )
                ]
            )
        ]

        if (not self.config.editMode):

            selectInfo = ft.Container(
                height=componentHeight,
                alignment=ft.alignment.center,
                border_radius=10,
                content=ft.Row(
                    controls=[
                        ft.Text(
                            value=len(self.config.selectedOutfits),
                            size=14,
                            color="#F9A8D4",
                            font_family="ShantellSans-SemiBold",
                            ref=self.config.selectedCountRef
                            
                        ),
                        ft.Text(
                            value="outfits selected",
                            size=14,
                            color="#A1A1AA",
                            font_family="ShantellSans-SemiBold"
                        ),
                    ]
                ),
            )

            controls.append(selectInfo)

        return ft.Row(
            width=self.config.style.pageWidth,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN if not self.config.editMode else None,
            controls=controls
        )
    

    def getClearFilterButton(self):
        return ft.TextButton(
            height=55,
            width=200,
            text="Clear Filter",
            on_click=lambda _: self.clearFilterAction()
        )

    def getOutfitCards(self, outfits = None,  height = None, spacing=None):

        displayOutfits = outfits

        if (displayOutfits is None):
            displayOutfits = self.outfitsRequest.data

        emptyList = ft.Container(
            height=self.page.height - self.config.style.heightOffset - self.dropdownHeight,
            width=self.config.style.pageWidth - self.config.style.widthOffset,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="\ue4ff;",
                        font_family="FontAwesome",
                        color="#FCE7F3",
                        size=120,
                    ),
                    ft.Text(
                        value="NO OUTFITS AVAILABLE",
                        font_family="ShantellSans-SemiBold",
                        size=32,
                        color="#FCE7F3",
                    )
                ]
            ),
            padding=ft.padding.only(bottom=100)
        )
            
        if displayOutfits is not None:
            if len(displayOutfits) > 0:
                content = ft.GridView(
                    height=height,
                    spacing=25 if spacing is None else spacing,
                    run_spacing=25,
                    max_extent=275,
                    width=self.config.style.pageWidth - self.config.style.widthOffset,
                    padding=ft.padding.only(right=50) if outfits is None else 0
                )

                for outfit in displayOutfits:
                    content.controls.append(
                        self.getOutfitCard(outfit)
                    )
            else:
                if(outfits is None): 
                    content = emptyList

                else:
                    content = ft.Container()
        else:
            content = emptyList
            
        return content

    def findSelectedOutfit(self, data: OutfitModel):
        foundIdx = -1
        for i in range(len(self.config.selectedOutfits)):
            if (self.config.selectedOutfits[i].id == data.id):
                foundIdx = i
                break

        return foundIdx
    
    def selectAction(self, e: ft.ControlEvent, data: OutfitModel):
        
        foundIdx = self.findSelectedOutfit(data)

        if (foundIdx == -1):
            self.config.selectedOutfits.append(data)
            e.control.border=ft.border.all(width=self.selectedBorderWidth, color="#FCE7F3")
            self.config.selectedCountRef.current.value += 1
        
        else:
            del self.config.selectedOutfits[foundIdx]
            e.control.border=None
            self.config.selectedCountRef.current.value -= 1

        self.config.selectedCountRef.current.update()
        e.control.update()

        

    def getOutfitCard(self, outfitData):

        clickHandler = None

        if (self.config.selectMode):
            if (self.config.selectAction is None):
                clickHandler = lambda e : self.selectAction(e, outfitData)
            
            else:
                clickHandler = lambda e : self.config.selectAction(e, outfitData)
                
        controls = [
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Image(
                    height=200,
                    width=150,
                    src_base64=Utils.blob_to_base64(outfitData.picture),
                    fit=ft.ImageFit.COVER,
                ),
                padding=0,
            ),
        ]

        if (self.config.editMode):
            
            controls.insert(
                0, 
                ft.Container(
                    height=200,
                    width=50,
                    alignment=ft.alignment.top_center,
                    content=ft.TextButton(
                        content=ft.Text(
                            value=self.trashIcon,
                            font_family="FontAwesome",
                            size=25,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.MaterialState.DEFAULT: "#FAFAFA",
                                ft.MaterialState.HOVERED: "#F9A8D4",
                            },
                            color={
                                ft.MaterialState.DEFAULT: "#F472B6",
                                ft.MaterialState.HOVERED: "#FFFFFF",
                            }
                        ),
                        on_click=lambda _: self.config.deleteButtonAction(outfitData)
                    ),
                )
                    
            )
            controls.append(
                ft.Container(
                    height=200,
                    width=50,
                    alignment=ft.alignment.top_center,
                    content=ft.TextButton(
                        content=ft.Text(
                            value=self.editIcon,
                            font_family="FontAwesome",
                            size=25,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.MaterialState.DEFAULT: "#FAFAFA",
                                ft.MaterialState.HOVERED: "#F9A8D4",
                            },
                            color={
                                ft.MaterialState.DEFAULT: "#F472B6",
                                ft.MaterialState.HOVERED: "#FFFFFF",
                            }
                        ),
                        on_click=lambda _: self.config.editButtonAction(outfitData)
                    ),
                )
            )

        card = ft.Container(
            height=200,
            width=250,
            bgcolor="#FAFAFA",
            ink=True,
            on_click=clickHandler,
            border=None if self.findSelectedOutfit(outfitData) == -1 else ft.border.all(width=self.selectedBorderWidth, color="#FCE7F3"),
            border_radius=10,
            content=ft.Row(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=controls
            )
        )

        name = ft.Container(
            margin=ft.margin.only(top=5),
            width=250,
            alignment=ft.alignment.center,
            content=ft.Text(
                outfitData.name,
                size=16,
                color="#A1A1AA",
                font_family="ShantellSans-SemiBold"
            )
        )

        return ft.Column(
            spacing=0,
            controls=[
                card,
                name
            ]
        )
    

    def refreshDropdown(self):
        self.config.categoryDropdownRef.current.options.clear()
        self.config.colorDropdownRef.current.options.clear()

        getCategories = self.outfitCategoryController.get_all_categories()
        if getCategories.is_success and getCategories.data:
            self.config.categoryDropdownRef.current.hint_text = "Select Category"
            for category in getCategories.data:
                self.config.categoryDropdownRef.current.options.append(ft.dropdown.Option(category.name.split("_")[1]))
        else:
            self.config.categoryDropdownRef.current.hint_text = "No Categories Found"
            self.config.categoryDropdownRef.current.options.append(ft.dropdown.Option("No Categories Found"))
        
        getColors = self.outfitCategoryController.get_all_colors()
        if getColors.is_success and getColors.data:
            self.config.colorDropdownRef.current.hint_text = "Select Color"
            for color in getColors.data:
                self.config.colorDropdownRef.current.options.append(ft.dropdown.Option(color.name.split("_")[1]))
        else:
            self.config.colorDropdownRef.current.hint_text = "No Colors Found"
            self.config.colorDropdownRef.current.options.append(ft.dropdown.Option("No Colors Found"))


    def categoryDropdownAction(self):
        if self.config.categoryDropdownRef.current.value == "No Categories Found":
            return
        
        if not self.isFiltered:
            self.config.dropdownsRef.current.controls.append(self.getClearFilterButton())
            self.isFiltered = True

        self.outfitsRequest = self.outfitController.get_all_filtered(category=self.config.categoryDropdownRef.current.value, color=self.config.colorDropdownRef.current.value)
        self.config.contentRef.current.controls.pop(1)
        self.config.contentRef.current.controls.append(self.getOutfitCards())

        self.config.dropdownsRef.current.update()
        self.config.contentRef.current.update()
        self.page.update()
    

    def colorDropdownAction(self):
        if self.config.colorDropdownRef.current.value == "No Colors Found":
            return
        
        if not self.isFiltered:
            self.config.dropdownsRef.current.controls.append(self.getClearFilterButton())
            self.isFiltered = True

        self.outfitsRequest = self.outfitController.get_all_filtered(category=self.config.categoryDropdownRef.current.value, color=self.config.colorDropdownRef.current.value)
        self.config.contentRef.current.controls.pop(1)
        self.config.contentRef.current.controls.append(self.getOutfitCards())

        self.config.dropdownsRef.current.update()
        self.config.contentRef.current.update()
        self.page.update()
    

    def clearFilterAction(self):
        self.isFiltered = False

        if (len(self.config.dropdownsRef.current.controls) > 2):
            self.config.dropdownsRef.current.controls.pop(2)

            self.config.categoryDropdownRef.current.value = None
            self.config.colorDropdownRef.current.value = None

            self.outfitsRequest = self.outfitController.get_all()
            self.config.contentRef.current.controls.pop(1)
            self.config.contentRef.current.controls.append(self.getOutfitCards())

            self.config.dropdownsRef.current.update()
            self.config.contentRef.current.update()
            self.page.update()