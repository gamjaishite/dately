import flet as ft
from Utils.components.navbar import Navbar
from Utils.components.dateInfo import DateInfo
from Utils.components.profileBox import ProfileBox, ProfileBoxConfig
from Utils.components.rateDialog import RateDialog
from Utils.components.notification import Notification
from Utils.components.deletePopup import DeletePopup
from datetime import datetime
import Controllers
import calendar

class HistoryView(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__()
        self.page : ft.Page = page
        self.selected_date = None
        self.rateDialog = False
        self.rateCount = 0
        self.buttonClicked = None

        #Controllers for accessing DB
        self.controllerProfile: Controllers.ProfileController = Controllers.ProfileController()
        self.controllerHistory: Controllers.HistoryController = Controllers.HistoryController()
        self.controllerDates: Controllers.DateController = Controllers.DateController()

        #Icons
        self.empty_icon = "\ue4ff;"
        self.delete_icon = "\uf2ed;"
        self.instagram_icon = "\uf16d;"
        self.undo_icon = "\uf0e2;"
        self.filled_star_icon = "\uf005"
        self.empty_star_icon = "\uf005"

    def build(self):
        #Ref
        self.rate_popup_ref = ft.Ref[ft.AlertDialog]()
        self.delete_popup: DeletePopup = None

        self.selected_date = 0
        historyList = self.getHistoryList()
        emptyDetails = self.getEmptyColumn("NO DATE SELECTED")

        self.delete_popup = DeletePopup()
        result = ft.Row(
                    width = self.getPageWidth(),
                    controls=[self.delete_popup,historyList, emptyDetails]
                )
        return result

    def getPageWidth(self):
        return self.page.width - Navbar.width + 20

    def getPageHeight(self):
        return self.page.height
    
    def getHistoryList(self):
        title = ft.Container(
            content=ft.Text(
                value="Histories",
                font_family="ShantellSans-SemiBold",
                size=40,
                color="#F472B6",

            )
        )

        self.data = self.getHistoryData()

        historyList = ft.Container(
                width=self.getPageWidth()/2,
                bgcolor=ft.colors.WHITE,
                content= ft.Stack(
                controls = [self.data, title],
            )
        )

        return historyList

    def getHistoryData(self):
        histories = ft.ListView(
            width=300,
            height=self.getPageHeight() - 100,
            spacing=20,
            padding=ft.padding.only(top=35)
        )

        self.historyDates = self.controllerHistory.get_many().data
        self.partnersProfile = self.controllerProfile.get_partners().data
        for history in self.historyDates:
            for partners in self.partnersProfile:
                if(history.partner_id == partners.index):
                    histories.controls.append(self.getHistoryCards(history, partners))

        if(len(self.historyDates)):
            return ft.Container(
                    alignment=ft.alignment.center,
                    content= histories
                )
            
        else:
            return self.getEmptyColumn("HISTORY EMPTY")

    def getHistoryCards(self, history, partners):

        dating_date = self.getDatetimeStringFormat().format(
            hour=history.date.hour,
            minute=history.date.minute,
            date=history.date.day,
            month=calendar.month_name[history.date.month],
            year=history.date.year,
        )

        partner_name_button = ft.Text(
                value = partners.name,
                font_family="ShantellSans-SemiBold",
                size=15 ,
                color="#52525B",
            )
        undoIcon = ft.IconButton(
                content=ft.Text(value=self.undo_icon, color="#F472B6", size=20, font_family="FontAwesome"),
                on_click= lambda _ :self.clickedUndo(history)
            )
        
        rateIcon = ft.IconButton(
                content=ft.Text(value=self.filled_star_icon, color="#F472B6", size=20, font_family="FontAwesome"),
                on_click = lambda _:self.clickedRate(history)
            )
        
        cardsIcon = ft.Column(
            spacing=0,
            controls=
            [undoIcon]
        )

        if (history.date < datetime.now()):
            undoIcon.content = ft.Text(value=self.undo_icon, color=ft.colors.TRANSPARENT, size=20, font_family="FontAwesome")
            undoIcon.disabled = True
            # undoIcon.on_click = lambda _: ""

        if(history.rating == 0 or history.rating == None):
            cardsIcon.controls.append(rateIcon)

        cardsInfo = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=
            [ft.Text(
                value = dating_date,
                size=10,
                color="#A1A1AA",
            ),
            partner_name_button
            ]
        )

        cards = ft.ElevatedButton(
            height=90,
            style= ft.ButtonStyle(
                bgcolor="#FAFAFA",
                overlay_color="#e6e3e3",
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=0.05,
            ),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        cardsIcon,
                        cardsInfo,
                    ],

                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            on_click= lambda _: self.clickedDetails(history,partners),
        )
        return cards

    def getHistoryDetails(self, history, partners):
        detailWidth = self.getPageWidth()/2
        
        deleteIcon = ft.Container( #Display delete icon
            width= detailWidth - 40,
            alignment= ft.alignment.top_right,
            padding=ft.padding.only(right=40, top=20),
            content= ft.IconButton(
                icon_color="#F472B6",
                icon_size=30,
                tooltip="Delete history",
                content= ft.Text(
                    value= self.delete_icon,
                    size = 25,
                    font_family="FontAwesome",
                    color="#EC4899",
                ),
                on_click= lambda _: self.showDeletePopUp(self.id)
            )
        )

        if(self.selected_date != 0):
            info = ft.ListView(
                width=450,
                spacing=30,
                height=550,
                padding=ft.padding.only(right=40),
            )

            info = self.fetchHistoryDetail(history, partners)
        else:
            info= self.getEmptyColumn("NO DATE SELECTED")

        return ft.Container(
                width= detailWidth,
                alignment= ft.alignment.center,
                bgcolor="#FDF2F8",
                content = ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls = [deleteIcon, info]
                )
            )
    
    def fetchHistoryDetail(self, history, partners):
        
        starRate = ft.Row( #Display default rating star
            alignment= ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(
                    name= ft.icons.STAR_BORDER_OUTLINED,
                    color="#F472B6",
                    size=25,
                ),
                ft.Icon(
                    name= ft.icons.STAR_BORDER_OUTLINED,
                    color="#F472B6",
                    size=25,
                ),
                ft.Icon(
                    name= ft.icons.STAR_BORDER_OUTLINED,
                    color="#F472B6",
                    size=25,
                ),
                ft.Icon(
                    name= ft.icons.STAR_BORDER_OUTLINED,
                    color="#F472B6",
                    size=25,
                ),
                ft.Icon(
                    name= ft.icons.STAR_BORDER_OUTLINED,
                    color="#F472B6",
                    size=25,
                ),
            ]
        )

        starFill = ft.Icon( #Display rating star filled
            name= ft.icons.STAR_RATE,
            color="#F472B6",
            size=25,
        )
        starEmpty = ft.Icon( #Display epty rating star
            name= ft.icons.STAR_BORDER_ROUNDED,
            color="#F472B6",
            size=25,
        )
        
        #For displaying rated rating star
        starNum = 5
        if history.rating != 0 and history.rating:
            starRate.controls.clear()
            for i in range(history.rating):
                starRate.controls.append(starFill)
                starNum-=1
            for i in range(starNum):
                starRate.controls.append(starEmpty)
            
        reviewTextBox = ft.Container( #Review Text Box
            alignment= ft.alignment.center,
            padding=10,
            bgcolor= ft.colors.WHITE,
            width=450,
            height=100,
            border_radius=10,
            content=ft.Text(
                value= history.review if history.review else "No Review",
                size=13,
                color="#A1A1AA",
            )
        )
        
        
        historyDetail = ft.ListView(
            width=450,
            spacing=30,
            height=550,
            padding=ft.padding.only(right=40),
            controls=[
                starRate, 
                reviewTextBox,
                self.fetchHistoryInfo(history),
                self.fetchPartnerInfo(partners),
            ]
        )

        return ft.Container(
            alignment=ft.alignment.center,
            content=historyDetail
        )

    def fetchHistoryInfo(self, history):
        return DateInfo(history)
    
    def fetchPartnerInfo(self, partners):
        return ProfileBox(
            profileConfig=ProfileBoxConfig(
                data = partners
            )
        )
    
    def clickedDetails(self, history, partners):
        self.buttonClicked = 0
        self.selected_date+=1
        self.id = history.id

        rateDialog = ft.Container()
        if(self.rateDialog == True):
            rateDialog = self.controls[0].controls[-1]
            # self.rateDialog = False

        self.controls[0].controls.clear()
        self.controls[0].controls.append(self.getHistoryList())
        self.controls[0].controls.append(self.getHistoryDetails(history, partners))
        self.controls[0].controls.append(self.delete_popup)
        if(rateDialog is not None):
            self.controls[0].controls.append(rateDialog)
        self.update()

    def clickedRate(self, history):
        self.rateCount = 0
        self.buttonClicked = 1
        self.rateDialog = True
        rateDialog = None

        if (self.rate_popup_ref.current):
            self.controls[0].controls.pop()

        rateDialog = self.getRateDialogHelper(history).build()
        self.controls[0].controls.append(rateDialog)
        rateDialog = self.rate_popup_ref.current

        self.dialog = rateDialog
        rateDialog.open = True
        self.update()

    def clickedUndo(self, history):
        self.buttonClicked = 2
        self.save_data(history, False, history.rating, history.review)
        self.update()

    def showDeletePopUp(self, id):
        self.delete_popup.show(lambda : self.delete_data(id), title="Delete Dates?", actionTitle="DELETE")

    def getRateDialogHelper(self, history):
        return RateDialog(
            history=history,
            rate_popup_ref=self.rate_popup_ref,
            save_data=self.save_data,
        )
    
    def getEmptyHistoryList(self):
         emptyHistory = ft.Container(
            height=1564,
            content= ft.Container(
                alignment= ft.alignment.center,
                content = ft.Column(
                    alignment= ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                    controls=
                    [
                        ft.Icon(name=ft.icons.HEART_BROKEN_OUTLINED, color="#F472B6",),
                        ft.Text(value="NO HISTORY", color="#F472B6", size=50),
                    ]
                )
            )
        )
         return emptyHistory

    def getEmptyColumn(self, message):
        if(message == "NO DATE SELECTED"):
            return ft.Container(
                width= self.getPageWidth()/2,
                bgcolor="#FDF2F8",
                border= ft.border.only(left=ft.border.BorderSide(4, "#FCE7F3")),
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.getEmptyIcon("#FCE7F3"),
                        ft.Text(
                            value=message,
                            font_family="ShantellSans-SemiBold",
                            size=32,
                            color="#FCE7F3",
                        )
                    ]
                )
            )
        if(message == "HISTORY EMPTY"):
            return ft.Container(
                width= self.getPageWidth()/2,
                bgcolor="#FFFFFF",
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.getEmptyIcon("#FCE7F3"),
                        ft.Text(
                            value=message,
                            font_family="ShantellSans-SemiBold",
                            size=32,
                            color="#FCE7F3",
                        )
                    ]
                )
            )
    
    def getEmptyIcon(self, colorString): #Dately empty icon
        return ft.Text(
            value=self.empty_icon,
            font_family="FontAwesome",
            color=colorString,
            size=146,
        )
    
    def getDatetimeStringFormat(self): #Date time formatter from DB
        return "{hour:02d}:{minute:02d}, {date} {month} {year}"
    
    def save_data(self, history, status, rate, review): #Updating data in DB
        request = {
            "id" : history.id,
            "description" : history.description,
            "date" : history.date,
            "location" : history.location,
            "status" : status,
            "rating" : None if status == False else rate,
            "review" : None if status == False else review,
            "partner_id" : history.partner_id,
        }
        result = self.controllerHistory.update(request)
        if(self.buttonClicked == 1): # Add review and rate
            self.page.snack_bar = Notification(result.message)
            self.page.update()
            if(result.is_success):
                updatedHistory = self.controllerHistory.get_one(history.id).data
                updatedProfile = self.controllerProfile.get_partner_by_index(history.partner_id).data
                self.clickedDetails(updatedHistory, updatedProfile)

        if(self.buttonClicked == 2): # Restore date
            self.page.snack_bar = Notification(result.message)
            self.page.update()
            self.defaultHistoryPage()

    def delete_data(self, id): #Delete data in DB
        result = self.controllerHistory.deleteHistory(id)
        self.page.snack_bar = Notification(result.message)
        self.page.update()
        if(result.is_success):
            self.defaultHistoryPage()

    def defaultHistoryPage(self): # Reload page into default
        self.controls[0].controls.clear()
        self.controls[0].controls.append(self.getHistoryList())
        self.controls[0].controls.append(self.getEmptyColumn("NO DATE SELECTED"))
        self.update()