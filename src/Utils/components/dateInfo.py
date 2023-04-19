import flet as ft
import calendar

class DateInfo(ft.UserControl):

    def __init__(self, selected_date, **kwargs):
        super().__init__()
        self.selected_date = selected_date
        self.note_icon = "\uf0c6;"

    def getDatetimeStringFormat():
        return "{hour:02d}:{minute:02d}, {date} {month} {year}"
    
    def build(self):
        iconSize = 20
        smallFontSize = 10

        datetimeString = DateInfo.getDatetimeStringFormat().format(
            hour=self.selected_date.date.hour,
            minute=self.selected_date.date.minute,
            date=self.selected_date.date.day,
            month=calendar.month_name[self.selected_date.date.month],
            year=self.selected_date.date.year,
        )

        return ft.Container(
            padding=20,
            bgcolor="#FFFFFF",

            border_radius=10,
            content=ft.Column(
                controls=[
                    self.getDateInfoRow(
                        ft.Icon(
                            name=ft.icons.ACCESS_TIME,
                            color="#F472B6",
                            size=iconSize,
                        ),
                        datetimeString
                    ),

                    self.getDateInfoRow(
                        ft.Icon(
                            name=ft.icons.LOCATION_ON,
                            color="#F472B6",
                            size=iconSize,
                        ),
                        self.selected_date.location
                    ),

                    self.getDateInfoRow(
                        ft.Text(
                            value=self.note_icon,
                            font_family="FontAwesome",
                            color="#F472B6",
                            size=iconSize,
                        ),
                        self.selected_date.description,
                        smallFontSize
                    ),
                ]
            )
        )
    
    def getDateInfoRow(self, iconComponent, text, fontSize=12):

            text_width = 300

            return ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
                controls=[
                    iconComponent,
                    ft.Text(
                        value=text,
                        font_family="ShantellSans-SemiBold",
                        size=fontSize,
                        color="#A1A1AA",
                        width=text_width,
                    )
                ]
            )