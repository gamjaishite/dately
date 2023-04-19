import flet as ft
from Controllers.profile_controller.profile_controller import ProfileController
from Utils.components.notification import Notification
import Models


class InitialView(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__()
        self.page = page
        self.controller = ProfileController()

    def build(self):
        return self.showInitialPageView()

    def showInitialPageView(self):
        self.name_input_field = ft.TextField(
            border_color="#FDF2F8",
            border_width=7,
            border_radius=10,
            bgcolor="#FAFAFA",
            width=400,
            height=50,
            content_padding=ft.padding.only(12, 0, 12, 0),
            selection_color="#fce7f3",
            cursor_color="#F472B6",
            color="#52525B",
            text_align=ft.TextAlign.CENTER,
        )
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Dately",
                    font_family="ShantellSans-SemiBold",
                    size=60,
                    color="#F472B6"
                ),
                ft.Text(
                    value="Please enter your name below to start using the app",
                    color="#A1A1AA",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(
                    margin=ft.margin.only(5, 30, 5, 5),
                    content=self.name_input_field
                ),
                ft.Container(
                    content=ft.TextButton(
                        content=ft.Text(
                            value="GO!",
                            font_family="ShantellSans-SemiBold",
                            size=20,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.MaterialState.HOVERED: "#FBCFE8",
                                ft.MaterialState.DEFAULT: "#FDF2F8",
                            },
                            color={
                                ft.MaterialState.DEFAULT: "#F472B6",
                            },
                            overlay_color=ft.colors.TRANSPARENT,
                            shape={
                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                    radius=10)
                            },
                            side={
                                ft.MaterialState.DEFAULT: ft.BorderSide(
                                    7, "#FBCFE8")
                            },
                        ),
                        width=400,
                        height=50,
                        on_click=self.go_button_clicked,
                    )
                ),
            ]
        )

    def go_button_clicked(self, e):
        assert self.page is not None

        req = {
            "name": self.name_input_field.value,
            "role": Models.RoleEnum.main.value,
        }

        result = self.controller.add_profile(req)

        self.page.snack_bar = Notification(result.message)
        self.page.update()

        if result.is_success:
            self.page.go("/dates")
