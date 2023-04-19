import flet as ft
from typing import List, Callable
import Models

class RateDialog(ft.UserControl):

    def __init__(
            self,
            history,
            save_data: Callable[[Models.DateModel, bool, int, str], None],
            rate_popup_ref: ft.Ref[ft.AlertDialog] = ft.Ref[ft.AlertDialog](),
            **kwargs):
        super().__init__()
        self.history = history
        self.rateCount = 0
        self.save_data = save_data
        self.rate_popup_ref = rate_popup_ref
        self.starsButton = []

    def build(self):
        return self.getRateDialog(self.history)
    
    def getRateDialog(self, history):
        review_input = ft.TextField(
            width=470,
            height=100,
            max_lines=10,
            max_length=165,
            border_color=ft.colors.TRANSPARENT,
            value="",
        )
        def save_dlg(e): #Save button
            
            self.save_data(history, True, self.rateCount, review_input.value)

            if (self.rateCount):
                rateDialog.open = False
                self.rate_popup_ref.current.update()
                self.rateCount = 0

        def close_dlg(e): #Cancel button
            rateDialog.open = False
            self.rate_popup_ref.current.update()

        def toggle_icon_button(e): #Star rate toggle
            self.rateCount = e.control.data
            for i in range(self.rateCount):
                self.starsButton[i].selected = True
                self.starsButton[i].update()
            for j in range(self.rateCount, 5):
                self.starsButton[j].selected = False
                self.starsButton[j].update()

        self.starsButton = [ft.IconButton( #Star buttons
                                data=1,
                                icon= ft.icons.STAR_BORDER_ROUNDED,
                                icon_size=40,
                                selected_icon=ft.icons.STAR_RATE,
                                on_click= toggle_icon_button,
                                selected=False,
                                style=ft.ButtonStyle(color={"selected": "#F472B6", "": "#F472B6"}),
                            ),
                            ft.IconButton(
                                data=2,
                                icon= ft.icons.STAR_BORDER_ROUNDED,
                                icon_size=40,
                                selected_icon=ft.icons.STAR_RATE,
                                on_click= toggle_icon_button,
                                selected=False,
                                style=ft.ButtonStyle(color={"selected": "#F472B6", "": "#F472B6"}),
                            ),
                            ft.IconButton(
                                data=3,
                                icon= ft.icons.STAR_BORDER_ROUNDED,
                                icon_size=40,
                                selected_icon=ft.icons.STAR_RATE,
                                on_click= toggle_icon_button,
                                selected=False,
                                style=ft.ButtonStyle(color={"selected": "#F472B6", "": "#F472B6"}),
                            ),
                            ft.IconButton(
                                data=4,
                                icon= ft.icons.STAR_BORDER_ROUNDED,
                                icon_size=40,
                                selected_icon=ft.icons.STAR_RATE,
                                on_click= toggle_icon_button,
                                selected=False,
                                style=ft.ButtonStyle(color={"selected": "#F472B6", "": "#F472B6"}),
                            ),
                            ft.IconButton(
                                data=5,
                                icon= ft.icons.STAR_BORDER_ROUNDED,
                                icon_size=40,
                                selected_icon=ft.icons.STAR_RATE,
                                on_click= toggle_icon_button,
                                selected=False,
                                style=ft.ButtonStyle(color={"selected": "#F472B6", "": "#F472B6"}),
                            )]

        rateDialog = ft.AlertDialog( #Rate and review alert dialog
            ref=self.rate_popup_ref,
            content_padding=-20,
            content= ft.Container(
                bgcolor="#FAFAFA",
                alignment=ft.alignment.center,
                margin=-20,
                width=687,
                height=465,
                border_radius=10,
                border= ft.border.all(10,color="#F472B6", ),
                content= ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(value="Rate Your Dates!", color="#F472B6",),
                        ft.Row( #Star rate buttons
                            alignment= ft.MainAxisAlignment.CENTER,
                            vertical_alignment= ft.CrossAxisAlignment.CENTER,
                            controls=
                            self.starsButton
                        ),
                        ft.Container(
                            bgcolor="#FDF2F8",
                            width=470,
                            content= review_input
                        ),
                        ft.Row(
                            alignment= ft.MainAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                ft.Container(
                                    bgcolor= "#A1A1AA",
                                    padding=5,
                                    width=234,
                                    height=60,
                                    border_radius=10,
                                    content= ft.TextButton(
                                        content= ft.Text(value="CANCEL", color="#A1A1AA", size=28, weight=ft.FontWeight.BOLD),
                                        style= ft.ButtonStyle(
                                            padding=-1,
                                            overlay_color= ft.colors.TRANSPARENT,
                                            bgcolor="#E4E4E7",
                                            shape= ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        on_click=close_dlg,
                                    )
                                ),
                                ft.Container(
                                    bgcolor= "#FBCFE8",
                                    padding=5,
                                    width=234,
                                    height=60,
                                    border_radius=10,
                                    content= ft.TextButton(
                                        content= ft.Text(value="SAVE", color="#F472B6", size=28, weight=ft.FontWeight.BOLD),
                                        style= ft.ButtonStyle(
                                            padding=-1,
                                            overlay_color= ft.colors.TRANSPARENT,
                                            bgcolor="#FDF2F8",
                                            shape= ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        on_click=save_dlg,
                                    )   
                                ),
                        ])
                    ]
                )
            )
        )
        return rateDialog