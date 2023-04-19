import flet as ft
from Utils.components.navbar import Navbar
from Utils.components.profileBox import ProfileBox, ProfileBoxConfig
from Utils.components.notification import Notification
from Utils.components.dateInfo import DateInfo
from Controllers.date_controller.date_controller import DateController
from Controllers.profile_controller.profile_controller import ProfileController
from Controllers.history_controller.history_controller import HistoryController
from Models.date_model.date_model import DateModel
import calendar
from Utils.components.outfitList import OutfitList, OutfitListConfig, OutfitListStyle
from Utils.components.rateDialog import RateDialog
from Utils.components.deletePopup import DeletePopup
import sys


class DateView(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__()
        self.page = page
        self.controller = DateController()
        self.profileController = ProfileController()
        self.historyController = HistoryController()

        # styles
        self.header_height = 75
        self.empty_icon = "\ue4ff;"
        self.delete_icon = "\uf2ed;"
        self.edit_icon = "\uf044;"
        self.note_icon = "\uf0c6;"

        self.selected_date: DateModel = None

    def build(self):

        # info
        self.show_detail = False
        self.selected_date = None

        # data
        self.dates = None

        # ref
        self.rate_popup_ref = ft.Ref[ft.AlertDialog]()
        self.delete_popup: DeletePopup = None

        # initialize
        if (self.page.date_edit_id):
            result = self.controller.get_one(self.page.date_edit_id)
            if (not result.is_success):
                self.page.snack_bar = Notification(result.message)

            self.selected_date = result.data
            self.page.date_edit_id = None

        dateList = self.getDateList()
        dateList.width = self.getPageWidth() / 2

        dateDetail = self.getDateDetail()

        self.delete_popup = DeletePopup()

        return ft.Row(
            width=self.getPageWidth(),
            spacing=0,
            controls=[
                self.delete_popup,
                dateList,
                dateDetail,
            ]
        )

    def getPageWidth(self):
        return self.page.width - Navbar.width + 20

    def getDateList(self):

        result = self.controller.get_many()
        if (not result.is_success):
            self.page.snack_bar = Notification(result.message)

        self.dates = result.data

        header = ft.Container(
            height=self.header_height,
            content=ft.Text(
                value="Dates",
                font_family="ShantellSans-SemiBold",
                size=40,
                color="#F472B6",
            )
        )

        if (self.dates and len(self.dates)):
            # jika  ada data
            content = self.fetchDateList()

        else:
            content = self.getEmptyColumn("EMPTY DATES DATA")

        addButton = self.getAddButton()

        dateList = ft.Container(
            bgcolor="#FFFFFF",
            width=self.getPageWidth() / 2,
            content=ft.Column(
                spacing=0,
                controls=[
                    header,
                    ft.Stack(
                        controls=[
                            content,
                            addButton,
                        ]
                    )

                ]
            )
        )

        return dateList

    def getAddButton(self):
        return ft.IconButton(
            content=ft.Text(
                value="\u002b;",
                font_family="FontAwesome",
                color="#F472B6",
                size=30,
            ),
            height=75,
            width=75,
            right=30,
            bottom=10,
            style=ft.ButtonStyle(
                bgcolor="#FDF2F8"
            ),
            on_click=lambda _: self.addDate()
        )

    def fetchDateList(self):

        cards = ft.ListView(
            width=350,
            spacing=25,
            height=550,

            padding=ft.padding.only(right=40),
        )

        for date in self.dates:
            cards.controls.append(self.getDateCard(date))

        return ft.Container(
            alignment=ft.alignment.center,
            content=cards
        )

    def getDateCard(self, date):

        datetimeString = DateInfo.getDatetimeStringFormat().format(
            hour=date.date.hour,
            minute=date.date.minute,
            date=date.date.day,
            month=calendar.month_name[date.date.month],
            year=date.date.year,
        )

        return ft.ElevatedButton(
            height=75,
            style=ft.ButtonStyle(
                bgcolor="#FAFAFA",
                overlay_color="#e6e3e3",
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=0.05,
            ),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.CHECK_CIRCLE_ROUNDED,
                        icon_color="#F472B6",
                        icon_size=32,
                        style=ft.ButtonStyle(
                            overlay_color="#FAFAFA",
                        ),
                        on_click=lambda _: self.finishDate(date),

                    ),

                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                value=datetimeString,
                                font_family="ShantellSans-SemiBold",
                                size=10,
                                color="#A1A1AA",
                            ),

                            ft.Text(
                                value=date.partner.name,
                                font_family="ShantellSans-SemiBold",
                                size=15,
                                color="#52525B",
                                width=200,
                            )
                        ]
                    )
                ]

            ),

            on_click=lambda _: self.showDetail(date)
        )

    def showDetail(self, date):
        self.selected_date = date
        self.updateDetail()

    def deleteDate(self, id):
        result = self.controller.delete(id)

        self.page.snack_bar = Notification(result.message)
        self.page.update()

        if result.is_success:
            self.selected_date = None
            self.updateDetail()
            self.updateList()

    def showDeletePopUp(self, id):
        self.delete_popup.show(lambda: self.deleteDate(
            id), title="Delete Dates?", actionTitle="DELETE")

    def save_rating(self, history, status, rate, review):  # Updating data in DB
        request = {
            "id": history.id,
            "status": status,
            "rating": rate,
            "review": review,
        }
        res = self.historyController.update(request)
        self.page.snack_bar = Notification(res.message)
        self.page.update()

    def finishDate(self, date):
        res = self.controller.finish_date(date.id)

        if (res.is_success):
            self.updateList()

            if (self.selected_date):
                self.selected_date = None
                self.updateDetail()

        self.page.snack_bar = Notification(res.message)
        self.page.update()

        if (self.rate_popup_ref.current):
            self.controls[0].controls.pop()

        rateDialog = RateDialog(
            history=date,
            save_data=self.save_rating,
            rate_popup_ref=self.rate_popup_ref
        ).build()

        self.controls[0].controls.append(rateDialog)
        self.rate_popup_ref.current.open = True
        self.update()

    def editDate(self, id):
        self.page.date_edit_id = id
        self.page.go("/dates/edit")

    def addDate(self):
        self.page.date_edit_id = None
        self.page.go("/dates/edit")

    def updateDetail(self):
        self.controls[0].controls.pop()
        self.controls[0].controls.append(self.getDateDetail())
        self.update()

    def updateList(self):
        self.controls[0].controls.pop(1)
        self.controls[0].controls.insert(1, self.getDateList())
        self.update()

    def getDateDetail(self):
        if (self.selected_date is not None):
            header = ft.Container(
                height=self.header_height,
                padding=ft.padding.only(left=20, right=60),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        self.getHeaderIconButton(
                            self.edit_icon, lambda _: self.editDate(self.selected_date.id)),
                        self.getHeaderIconButton(
                            self.delete_icon, lambda _: self.showDeletePopUp(self.selected_date.id)),

                    ]
                )
            )

            content = self.fetchDateDetail()

        else:
            header = ft.Container(
                height=self.header_height,
            )

            content = self.getEmptyColumn("NO DATE SELECTED")

        dateDetail = ft.Container(
            bgcolor="#FDF2F8",
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls=[
                    header,
                    content
                ]
            )
        )
        dateDetail.border = ft.border.only(
            left=ft.border.BorderSide(4, "#FCE7F3"))
        dateDetail.width = self.getPageWidth() / 2
        return dateDetail

    def getHeaderIconButton(self, iconUnicode, on_click_function):

        return ft.IconButton(
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=100),
                padding=5,
                bgcolor=ft.colors.TRANSPARENT,
                overlay_color=ft.colors.TRANSPARENT,
            ),

            content=ft.Text(
                value=iconUnicode,
                font_family="FontAwesome",
                color="#EC4899",
                size=25,
            ),
            on_click=on_click_function
        )

    def fetchDateDetail(self):
        dateDetail = ft.ListView(
            width=450,
            spacing=30,
            height=550,
            padding=ft.padding.only(right=40),
        )

        dateDetail.controls.append(self.fetchDateInfo())
        dateDetail.controls.append(self.fetchPartnerInfo())
        dateDetail.controls.append(self.fetchOutfitInfo())

        return ft.Container(
            alignment=ft.alignment.center,
            content=dateDetail
        )

    def fetchDateInfo(self):
        return DateInfo(selected_date=self.selected_date)

    def fetchPartnerInfo(self):

        return ProfileBox(
            profileConfig=ProfileBoxConfig(
                data=self.selected_date.partner
            )
        )

    def fetchPartnerInfo(self):

        return ProfileBox(
            profileConfig=ProfileBoxConfig(
                data=self.selected_date.partner
            )
        )

    def fetchOutfitInfo(self):

        selectedOutfits = []

        fetchDateResponse = self.controller.get_one(
            self.selected_date.id, includePartner=False, includeOutfits=True)

        if (fetchDateResponse.is_success):
            selectedOutfits = fetchDateResponse.data.outfits
        else:
            self.page.snack_bar = Notification(fetchDateResponse.message)
            self.page.update()

        outfitListHelper = OutfitList(
            page=self.page,
            config=OutfitListConfig(
                style=OutfitListStyle(
                    pageWidth=self.getPageWidth()/2 - 80,
                )
            )
        )

        outfitListHelper.build()

        return ft.Container(
            width=sys.maxsize,
            content=outfitListHelper.getOutfitCards(
                outfits=selectedOutfits, spacing=50),
            padding=ft.padding.only(bottom=80) if (len(selectedOutfits)) else 0
        )

    def getEmptyColumn(self, message):
        return ft.Container(
            height=self.page.height - 150,
            padding=ft.padding.only(bottom=self.page.height / 4),
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

    def getEmptyIcon(self, colorString):
        return ft.Text(
            value=self.empty_icon,
            font_family="FontAwesome",
            color=colorString,
            size=146,
        )
