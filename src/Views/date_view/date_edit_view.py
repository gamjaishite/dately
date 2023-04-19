import flet as ft
from Utils.components.navbar import Navbar
from Utils.components.notification import Notification
from Utils.components.profileBox import ProfileBox, ProfileBoxConfig
from Utils.components.outfitList import OutfitList, OutfitListConfig, OutfitListStyle
from Models.date_model.date_model import DateModel
from datetime import datetime
from Controllers.date_controller.date_controller import DateController
from Controllers.profile_controller.profile_controller import ProfileController
from Controllers.outfit_controller.outfit_controller import OutfitController
import calendar
import sys

class DateEditView(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__()
        self.page = page
        self.controller = DateController()
        self.profileController = ProfileController()
        self.outfitController = OutfitController()

    def build(self):

        #styles
        self.header_height = 75
        self.page_width = self.getPageWidth()
        self.page_width_middle_offset = 300

        #info
        self.selecting_time = False
        self.selecting_date = False
        self.selected_profile = None

        # data
        self.location_input = ""
        self.note_input = ""
        self.selected_partner = None
        self.partners = None
        self.date : DateModel = None

        fetchPartnersResponse = self.profileController.get_partners()
        if (not fetchPartnersResponse.is_success):
                self.page.snack_bar = Notification(fetchPartnersResponse.message)

        else:
            self.partners = fetchPartnersResponse.data
        
        self.year_limit_offset = 10
        self.minute_input = datetime.now().minute
        self.hour_input = datetime.now().hour
        self.year_input = datetime.now().year
        self.month_input = datetime.now().month
        self.date_input = datetime.now().day
        self.updateDateMax()

        self.hour_on_change_input = self.hour_input
        self.minute_on_change_input = self.minute_input
        self.year_on_change_input = self.year_input
        self.month_on_change_input = self.month_input
        self.date_on_change_input = self.date_input

        # refs
        self.date_input_ref = ft.Ref[ft.TextField]()
        self.time_column_ref = ft.Ref[ft.Column]()
        self.date_column_ref = ft.Ref[ft.Column]()
        self.time_info_ref = ft.Ref[ft.ElevatedButton]()
        self.date_info_ref = ft.Ref[ft.ElevatedButton]()
        self.partner_selection_ref = ft.Ref[ft.Column]()
        self.partner_dropdown_ref = ft.Ref[ft.Dropdown]()
        self.outfit_list_component = None

        if (self.page.date_edit_id):
            # info
            self.selected_profile = None

            # data

            fetchDateResponse = self.controller.get_one(self.page.date_edit_id)
            if (not fetchDateResponse.is_success):
                self.page.snack_bar = Notification(fetchDateResponse.message)

            else:
                self.date = fetchDateResponse.data
                self.location_input = self.date.location
                self.note_input = self.date.description
                self.selected_partner = self.date.partner
                self.minute_input = self.date.date.minute
                self.hour_input = self.date.date.hour
                self.year_input = self.date.date.year
                self.month_input = self.date.date.month
                self.date_input = self.date.date.day

        self.content = self.fetchDateForm()

        return ft.Column(
            spacing=0,
            expand=True,

            width=self.page_width,
            controls=[
                self.getHeader(),
                ft.ListView(
                    height=550,
                    controls=[self.content],
                ),
            ]
        )
    
    def getPageWidth(self):
        return self.page.width - Navbar.width
    
    def updateDateMax(self):
        self.date_max = calendar.monthrange(self.year_input, self.month_input)[1] + 1

    def updateTimeInfo(self):
        self.time_info_ref.current.text = self.getTimeString()
        self.time_info_ref.current.update()

    def updateDateInfo(self):
        self.date_info_ref.current.text = self.getDateString()
        self.date_info_ref.current.update()

    def getTimeString(self):
        return " {hour:02d}:{minute:02d}".format(hour=self.hour_input, minute=self.minute_input)

    def getDateString(self):

        dateString = str(self.date_input)
        monthString = calendar.month_name[self.month_input]
        yearString = str(self.year_input)

        return dateString + " " + monthString + " " + yearString
    
    def getDateTime(self):
        pass


    def getHeader(self):
        
        return ft.Container(
                height=self.header_height,
                padding=ft.padding.only(left=20, right=40),

                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(
                            value="Dates",
                            font_family="ShantellSans-SemiBold",
                            size=40,
                            color="#F472B6",
                        ),     
                        
                        ft.Container(
                            padding=ft.padding.only(top=30),
                            content=ft.Row(
                                controls=[
                                    self.getBorderedButton("CANCEL", lambda _:self.cancelDateChanges()),
                                    self.getBorderedButton("SAVE", lambda _:self.changeDate()),
                                ]
                            )
                        )
                    ]
                )
            )

    def getBorderedButton(self, label, on_click_function):

        return ft.Container(
            border=ft.border.all(width=3, color="#FBCFE8"),
            border_radius=10,
            bgcolor="#FDF2F8",
            content=ft.ElevatedButton(
                text=label,
                height=25,
                width=100,
                style=ft.ButtonStyle(
                    padding=ft.padding.only(bottom=5, top=3),
                    elevation=0,
                    color="#F472B6",
                    bgcolor=ft.colors.TRANSPARENT,
                    shape=ft.RoundedRectangleBorder(radius=7),
                ),

                on_click=on_click_function
            ),
        )


    def fetchDateForm(self):

        selectedOutfits = []

        if (self.date):

            fetchDateResponse = self.controller.get_one(self.date.id, includePartner=False, includeOutfits=True)

            if (fetchDateResponse.is_success):
                selectedOutfits = fetchDateResponse.data.outfits
            else:
                self.page.snack_bar = Notification(fetchDateResponse.message)
                self.page.update()

        self.outfit_list_component = OutfitList(
            page=self.page,
            config=OutfitListConfig(
                style=OutfitListStyle(
                    pageWidth=self.getPageWidth(),
                    heightOffset= self.header_height + 100,
                    widthOffset=20,
                    leftDropDownWidth=((self.page_width-self.page_width_middle_offset)/2 - 20)/2,
                ),
                selectMode=True,
                selectedOutfits=selectedOutfits
            )
        )

        return ft.Container(

            padding=ft.padding.only(left=40, right=40),
            content=ft.Column(
                spacing= 40,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            self.fetchDateInfoField(),
                            self.fetchPartnerSelection(),
                        ]
                    ),

                    self.getInputField(
                        "Select Your Outfit",
                        self.outfit_list_component
                    )
                ]
            )
        )

    def fetchDateInfoField(self):

        return ft.Column(
            width=(self.page_width-self.page_width_middle_offset)/2,
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.getButtonInputField("Time", self.timeClickHandler, self.getTimeString(), ref=self.time_info_ref),
                        ],
                        ref=self.time_column_ref,
                    )
                ),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.getButtonInputField("Date", self.dateClickHandler, self.getDateString(), ref=self.date_info_ref),
                        ],
                        ref=self.date_column_ref,
                    )
                ),
            
                self.getTextInputField("Location", "Enter Location...", self.locationInputHandler, self.location_input),
                self.getTextInputField("Note", "Enter Note....", self.noteInputHandler, self.note_input),
            ],
        )
    
    def partnerSelectionChangeHandler(self, e):
    
        fetchProfileResponse = self.profileController.get_partner_by_id(self.partner_dropdown_ref.current.value)

        if (not fetchProfileResponse.is_success):
            self.page.snack_bar = Notification(fetchProfileResponse.message)
            self.page.update()

        else:
            self.selected_partner = fetchProfileResponse.data
            partnerInfo = ProfileBox(
                profileConfig=ProfileBoxConfig(
                    data=fetchProfileResponse.data
                )
            )

            self.partner_selection_ref.current.controls = [
                self.partner_selection_ref.current.controls[0], 
                ft.Container(
                    bgcolor="#FDF2F8",
                    border_radius=10,
                    padding=20,
                    content=partnerInfo
                )
            ]
            
            self.partner_selection_ref.current.update()

    
    def fetchPartnerSelection(self):
        
        options = []
        selectedPartnerId = None
        if (self.selected_partner): 
            selectedPartnerId = self.selected_partner.id

        for partner in self.partners:
            options.append(
                ft.dropdown.Option(
                    text=partner.name,
                    key=partner.id
                )
            )

            

        controls = [
            self.getInputField(
                "Partner",
                ft.Dropdown(
                    width=400,
                    height=50,
                    filled=True,
                    bgcolor="#f2f2f2",
                    color="#A1A1AA",
                    border_radius=10,
                    border_width=0, 
                    hint_text="Select Partner",
                    hint_style=ft.TextStyle(
                        size=14,
                        color="#A1A1AA",
                        font_family="ShantellSans-SemiBold"
                    ),
                    text_style=ft.TextStyle(
                    size=14,
                    color="#A1A1AA",
                    font_family="ShantellSans-SemiBold",
                    ),
                    content_padding=ft.padding.only(top=30, left=20),
                    value=selectedPartnerId,
                    options=options,
                    ref=self.partner_dropdown_ref,
                    on_change=lambda e : self.partnerSelectionChangeHandler(e),
                ),
            ),
        ]
        
        if (self.date is not None):


            partnerInfo = ProfileBox(
                profileConfig=ProfileBoxConfig(
                    data = self.date.partner
                )
            )

            controls.append(
                ft.Container(
                    bgcolor="#FDF2F8",
                    border_radius=10,
                    padding=20,
                    content=partnerInfo
                )
            )
    
        return ft.Column(
            width=(self.page_width-self.page_width_middle_offset)/2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=controls,
            ref=self.partner_selection_ref
        )
    
    def getButtonInputField(self, label, handler_function, initialValue="", ref=None):
        width = sys.maxsize
        return self.getInputField(
            label,
            ft.ElevatedButton(
                text=initialValue,
                width=width,
                height = 30,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=7),
                    elevation=0,
                    bgcolor="#f2f2f2",
                    color="#A1A1AA",  
                    
                ),

                on_click=handler_function,
                ref=ref
            ),
        )

    def getTextInputField(self, label, hint, handler_function, initialValue=""):
        return self.getInputField(
            label, 
            ft.TextField(
                value=initialValue,
                max_length=255,
                bgcolor="#f2f2f2",
                border_width=0,
                multiline=True,
                text_style=ft.TextStyle(
                    size = 15,
                    color="#A1A1AA",
                    font_family="ShantellSans-Regular",
                ),
                hint_style=ft.TextStyle(
                    size = 15,
                    color="#A1A1AA",
                    font_family="ShantellSans-Regular",
                ),
                hint_text=hint,
                counter_style=ft.TextStyle(
                    color=ft.colors.TRANSPARENT,
                    size=0,
                ),
                on_blur=handler_function,
            )
        )
    
    def getInputField(self, label, inputBox):
        return ft.Column(
            spacing=5,
            controls=[
                ft.Text(
                    value=label,
                    color="#FBCFE8",
                    size=15
                ),
                inputBox
            ]
        )
    
    def getTimeInputField(self):
        return ft.Container(    
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.getNumberSelection(self.hourChangeHandler, self.hourOnChangeHandler, self.hour_input, maxDigit=2),
                    self.getNumberSelection(self.minuteChangeHandler, self.minuteOnChangeHandler, self.minute_input, maxDigit=2),
                ]
            )
        )
    
    def getDateInputField(self):

        return ft.Container(    
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.getNumberSelection(self.dateChangeHandler, self.dateOnChangeHandler, self.date_input, ref=self.date_input_ref, maxDigit=2),
                    self.getNumberSelection(self.monthChangeHandler, self.monthOnChangeHandler, self.month_input, maxDigit=2),
                    self.getNumberSelection(self.yearChangeHandler, self.yearOnChangeHandler, self.year_input, maxDigit=4),
                ]
            )
        )

    def getNumberSelection(self, changeHandler, onChangeHandler, initialValue, ref = None, maxDigit=None):
        
        target = ft.TextField(
            value=initialValue,
            keyboard_type=ft.KeyboardType.NUMBER,
            height=30,
            text_align=ft.TextAlign.CENTER,
            border_color="#F472B6",
            content_padding=ft.padding.only(bottom=7),
            text_style=ft.TextStyle(
                font_family="ShantellSans-Regular",
                color="A1A1AA",
                size=12,                            
            ),
            max_length=maxDigit,
            counter_style=ft.TextStyle(
                size=0,
            ),
            on_blur=lambda e: changeHandler(e.control, value=e.control.value),
            on_change=lambda e: onChangeHandler(e),
            ref=ref,
        )

        return ft.Container(
            padding=5,
            alignment=ft.alignment.center,
            content=ft.Column(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=60,
                controls=[
                    ft.Container(
                        margin=-10,
                        content=ft.IconButton(
                            content=ft.Text(
                                value="\uf0d8;",
                                font_family="FontAwesome",
                                color="#F472B6",
                                size=30,
                            ),
                            style=ft.ButtonStyle(
                                padding=0,

                            ),
                            on_click=lambda e: changeHandler(target, inc=1)
                        )
                    ),

                    target,

                    ft.Container(
                        margin=-15,
                        content=ft.IconButton(
                            content=ft.Text(
                                value="\uf0d7;",
                                font_family="FontAwesome",
                                color="#F472B6",
                                size=30,
                            ),
                            style=ft.ButtonStyle(
                                padding=0,

                            ),
                            on_click=lambda e: changeHandler(target, inc=-1),
                        )
                    )
                ]
            )
        )

    def locationInputHandler(self, e: ft.ControlEvent):
        self.location_input = str(e.control.value)

    def noteInputHandler(self, e: ft.ControlEvent):
        self.note_input = str(e.control.value)

    def timeClickHandler(self, e: ft.ControlEvent):
        self.selecting_time = not self.selecting_time

        if (self.selecting_time):
            self.time_column_ref.current.controls.append(self.getTimeInputField())

        else:
            self.time_column_ref.current.controls.pop()

        self.time_column_ref.current.update()

    def dateClickHandler(self, e: ft.ControlEvent):
        self.selecting_date = not self.selecting_date

        if (self.selecting_date):
            self.date_column_ref.current.controls.append(self.getDateInputField())

        else:
            self.date_column_ref.current.controls.pop()

        self.date_column_ref.current.update()
    
    def hourOnChangeHandler(self, e: ft.ControlEvent):

        textControl = e.control
        max = 24

        if (len(textControl.value) and (not textControl.value.isnumeric() or int(e.control.value) >= max)):
            textControl.value = self.hour_on_change_input
            textControl.update()
                
        else:
            self.hour_on_change_input = textControl.value

    def minuteOnChangeHandler(self, e: ft.ControlEvent):

        textControl = e.control
        max = 60

        if (len(textControl.value) and (not textControl.value.isnumeric() or int(e.control.value) >= max)):
            textControl.value = self.minute_on_change_input
            textControl.update()
                
        else:
            self.minute_on_change_input = textControl.value
    
    def yearOnChangeHandler(self, e: ft.ControlEvent):

        textControl = e.control
        max = datetime.now().year() + self.year_limit_offset
        if (len(textControl.value) and (not textControl.value.isnumeric() or int(e.control.value) >= max)):
            textControl.value = self.year_on_change_input
            textControl.update()
                
        else:
            self.year_on_change_input = textControl.value

    def monthOnChangeHandler(self, e: ft.ControlEvent):

        textControl = e.control
        max = 13
        if (len(textControl.value) and (not textControl.value.isnumeric() or int(e.control.value) >= max)):
            textControl.value = self.month_on_change_input
            textControl.update()
                
        else:
            self.month_on_change_input = textControl.value

    def dateOnChangeHandler(self, e: ft.ControlEvent):

        textControl = e.control
        max = self.date_max

        if (len(textControl.value) and (not textControl.value.isnumeric() or int(e.control.value) >= max)):
            textControl.value = self.date_on_change_input
            textControl.update()
                
        else:
            self.date_on_change_input = textControl.value

    def hourChangeHandler(self, target, inc=None, value=None):
        min = 0
        max = 24

        if (inc):
            temp = self.hour_input
            self.hour_input = ((temp - min + inc) % (max - min)) + min
            target.value = self.hour_input
            target.update()
        
        if (value):
            self.hour_input = int(value)

        else:
            target.value = self.hour_input
            target.update()

        self.updateTimeInfo()
        

    def minuteChangeHandler(self, target, inc=None, value=None):
        min = 0
        max = 60

        if (inc):
            temp = self.minute_input
            self.minute_input = (temp - min + inc) % (max - min) + min
            target.value = self.minute_input
            target.update()
        
        if (value):
            self.minute_input = int(value)

        else:
            target.value = self.minute_input
            target.update()

        self.updateTimeInfo()

    def yearChangeHandler(self, target, inc=None, value=None):

        min = datetime.now().year
        max = min + self.year_limit_offset

        if (inc):
            temp = self.year_input
            self.year_input = (temp - min + inc) % (max - min) + min
            target.value = self.year_input
            target.update()
        
        if (value):
            self.year_input = int(value)

        else:
            target.value = self.year_input
            target.update()

        self.updateDateInput()
        self.updateDateInfo()

    def monthChangeHandler(self, target, inc=None, value=None):

        min = 1
        max = 13

        if (inc):
            temp = self.month_input
            self.month_input = (temp - min + inc) % (max - min) + min
            target.value = self.month_input
            target.update()
        
        if (value):
            self.month_input = int(value)

        else:
            target.value = self.month_input
            target.update()
        
        self.updateDateInput()
        self.updateDateInfo()

    def dateChangeHandler(self, target, inc=None, value=None):
        min = 1
        max = self.date_max

        if (inc):
            temp = self.date_input
            self.date_input = (temp - min + inc) % (max - min) + min
            target.value = self.date_input
            target.update()
        
        if (value):
            self.date_input = int(value)

        else:
            target.value = self.date_input
            target.update()

        self.updateDateInfo()

    def updateDateInput(self):
        self.updateDateMax()

        if (self.date_input >= self.date_max):
            self.date_input = self.date_max-1
            self.date_input_ref.current.value = self.date_input
            self.date_input_ref.current.update()

    # create/edit date
    def changeDate(self):
        if (self.page.date_edit_id is None):
            self.createDate()

        else:
            if (self.date is None):
                self.page.snack_bar = Notification("Error occured while fetching data!")
                self.page.update()

            else:
                self.editDate()

    # create new date
    def createDate(self):

        req = {
            "description" : self.note_input,
            "date" : datetime(
                year=self.year_input, 
                month=self.month_input, 
                day=self.date_input, 
                hour=self.hour_input, 
                minute=self.minute_input
            ),
            "location" : self.location_input,
            "partner" : self.selected_partner,
            "outfits" : self.outfit_list_component.config.selectedOutfits,
        }

        result = self.controller.create(req)

        self.page.snack_bar = Notification(result.message)
        self.page.update()
        
        if result.is_success:
            self.page.go("/dates")

    # edit existing date
    def editDate(self):

        req = {
            "id" : self.date.id,
            "description" : self.note_input,
            "date" : datetime(
                year=self.year_input, 
                month=self.month_input, 
                day=self.date_input, 
                hour=self.hour_input, 
                minute=self.minute_input
            ),
            "location" : self.location_input,
            "partner" : self.selected_partner,
            "outfits" : self.outfit_list_component.config.selectedOutfits,
        }

        result = self.controller.update(req)

        self.page.snack_bar = Notification(result.message)
        self.page.update()
        
        if result.is_success:
            self.page.go("/dates")

    # cancel creating/editing date
    def cancelDateChanges(self):
        
        self.page.snack_bar = Notification("Creating/Editing Date is Canceled!")
        self.page.update()
        self.page.go("/dates")
    

