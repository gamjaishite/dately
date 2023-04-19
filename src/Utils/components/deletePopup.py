import flet as ft
from typing import List, Callable
import Models

class DeletePopup(ft.UserControl):

    def __init__(
            self,
            **kwargs):
        super().__init__()
        self.callback: Callable[[], None] | None = None
        self.popup_ref = ft.Ref[ft.AlertDialog]()
        self.title_ref = ft.Ref[ft.Text]()
        self.action_title_ref = ft.Ref[ft.Text]()

    def build(self):
        return self.getDialog()
    
    def show(self, callback, title, actionTitle):
        self.callback = callback
        self.popup_ref.current.open= True
        self.popup_ref.current.update()
        self.title_ref.current.value = title
        self.title_ref.current.update()
        self.action_title_ref.current.value = actionTitle
        self.action_title_ref.current.update()

    def close(self):
        self.popup_ref.current.open = False
        self.popup_ref.current.update()
    
    def getDialog(self):

        def action(e): #Action button
            self.close()
            self.callback()

        def close_dlg(e): #Cancel button
            self.close()

        rateDialog = ft.AlertDialog(
            ref=self.popup_ref,
            content= ft.Container(
                bgcolor="#FAFAFA",
                alignment=ft.alignment.center,
                width=100,
                border_radius=10,
                height=100,
                margin=ft.margin.only(bottom=-25),
                content= ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value="", 
                            color="#F472B6", 
                            ref=self.title_ref
                        ),

                        ft.Row(
                            alignment= ft.MainAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                ft.Container(
                                    bgcolor= "#A1A1AA",
                                    padding=5,
                                    width=100,
                                    height=40,
                                    border_radius=10,
                                    content= ft.TextButton(
                                        content= ft.Text(value="CANCEL", color="#A1A1AA", size=10, weight=ft.FontWeight.BOLD),
                                        style= ft.ButtonStyle(
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
                                    width=100,
                                    height=40,
                                    border_radius=10,
                                    content= ft.TextButton(
                                        content= ft.Text(value="", color="#F472B6", size=10, weight=ft.FontWeight.BOLD, ref=self.action_title_ref),
                                        style= ft.ButtonStyle(
                                            overlay_color= ft.colors.TRANSPARENT,
                                            bgcolor="#FDF2F8",
                                            shape= ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        on_click=action,
                                    )   
                                ),
                        ])
                    ]
                )
            )
        )
        return rateDialog