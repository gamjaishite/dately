from typing import List, Literal
import flet as ft


class Navbar(ft.UserControl):
    width: Literal[100] = 100

    def __init__(self, page: ft.Page, route: str, **kwargs):
        super().__init__()
        self.page = page

    def build(self):
        self.bgcolor_default = "#FDF2F8"
        self.fgcolor_default = "#EC4899"
        self.bgcolor_selected = "#FBCFE8"
        self.fgcolor_selected = "#DB2777"

        self.navbar_icons = {
            "profiles": "\uf007;",
            "dates": "\uf073;",
            "histories": "\uf1da;",
            "outfits": "\uf553;",
        }

        self.navbar_button_list: List[ft.Control] = [
            ft.IconButton(
                content=ft.Text(
                    value=self.navbar_icons["profiles"],
                    font_family="FontAwesome",
                    color=f"{self.fgcolor_selected if '/profiles' in self.page.route else self.fgcolor_default}",
                    size=20,
                ),
                style=ft.ButtonStyle(
                    overlay_color=ft.colors.TRANSPARENT,
                    bgcolor={
                        ft.MaterialState.DEFAULT: f"{self.bgcolor_selected if '/profiles' in self.page.route else self.bgcolor_default}",
                        ft.MaterialState.HOVERED: self.bgcolor_selected,
                    },
                ),
                width=65,
                height=65,
                on_click=lambda _: self.page.go("/profiles"),
            ),
            ft.IconButton(
                content=ft.Text(
                    value=self.navbar_icons["dates"],
                    font_family="FontAwesome",
                    color=f"{self.fgcolor_selected if '/dates' in self.page.route else self.fgcolor_default}",
                    size=20,
                ),
                style=ft.ButtonStyle(
                    overlay_color=ft.colors.TRANSPARENT,
                    bgcolor={
                        ft.MaterialState.DEFAULT: f"{self.bgcolor_selected if '/dates' in self.page.route else self.bgcolor_default}",
                        ft.MaterialState.HOVERED: self.bgcolor_selected,
                    },
                ),
                width=65,
                height=65,
                on_click=lambda _: self.page.go("/dates"),
            ),
            ft.IconButton(
                content=ft.Text(
                    value=self.navbar_icons["histories"],
                    font_family="FontAwesome",
                    color=f"{self.fgcolor_selected if '/histories' in self.page.route else self.fgcolor_default}",
                    size=20,
                ),
                style=ft.ButtonStyle(
                    overlay_color=ft.colors.TRANSPARENT,
                    bgcolor={
                        ft.MaterialState.DEFAULT: f"{self.bgcolor_selected if  '/histories' in self.page.route else self.bgcolor_default}",
                        ft.MaterialState.HOVERED: self.bgcolor_selected,
                    },
                ),
                width=65,
                height=65,
                on_click=lambda _: self.page.go("/histories"),
            ),
            ft.IconButton(
                content=ft.Text(
                    value=self.navbar_icons["outfits"],
                    font_family="FontAwesome",
                    color=f"{self.fgcolor_selected if  '/outfits' in self.page.route else self.fgcolor_default}",
                    size=20,
                ),
                style=ft.ButtonStyle(
                    overlay_color=ft.colors.TRANSPARENT,
                    bgcolor={
                        ft.MaterialState.DEFAULT: f"{self.bgcolor_selected if  '/outfits' in self.page.route else self.bgcolor_default}",
                        ft.MaterialState.HOVERED: self.bgcolor_selected,
                    },
                ),
                width=65,
                height=65,
                on_click=lambda _: self.page.go("/outfits"),
            ),
        ]

        self.navbar_columns = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=self.navbar_button_list,
        )

        return ft.Container(
            bgcolor="#FAFAFA",
            width=self.width,
            alignment=ft.alignment.center,
            padding=ft.Padding(10, 10, 10, 10),
            content=self.navbar_columns,
        )
