import flet as ft
from Views.views import ViewManager

import Utils
import Models


class Dately(ViewManager):
    def __init__(self, page: ft.Page):
        super().__init__(page)
        self.page = page


class MainApp():
    def main(self, page: ft.Page):
        theme = ft.Theme()
        theme.font_family = "ShantellSans-Regular"
        theme.page_transitions.windows = ft.PageTransitionTheme.ZOOM
        theme.page_transitions.macos = ft.PageTransitionTheme.ZOOM

        # window attribute
        page.title = "Dately"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.LIGHT
        page.theme = theme
        page.bgcolor = ft.colors.WHITE
        page.fonts = {
            "ShantellSans-Light": "/Fonts/ShantellSans-Light.ttf",
            "ShantellSans-LightItalic": "/Fonts/ShantellSans-LightItalic.ttf",
            "ShantellSans-Medium": "/Fonts/ShantellSans-Medium.ttf",
            "ShantellSans-MediumItalic": "/Fonts/ShantellSans-MediumItalic.ttf",
            "ShantellSans-Regular": "/Fonts/ShantellSans-Regular.ttf",
            "ShantellSans-Italic": "/Fonts/ShantellSans-Italic.ttf",
            "ShantellSans-SemiBold": "/Fonts/ShantellSans-SemiBold.ttf",
            "ShantellSans-SemiBoldItalic": "/Fonts/ShantellSans-SemiBoldItalic.ttf",
            "ShantellSans-Bold": "/Fonts/ShantellSans-Bold.ttf",
            "ShantellSans-BoldItalic": "/Fonts/ShantellSans-BoldItalic.ttf",
            "ShantellSans-ExtraBold": "/Fonts/ShantellSans-ExtraBold.ttf",
            "ShantellSans-ExtraBoldItalic": "/Fonts/ShantellSans-ExtraBoldItalic.ttf",

            "FontAwesome": "/Fonts/FontAwesome.otf",
            "FontAwesomeBrand": "/Fonts/FontAwesomeBrand.otf",
            "FontAwesomeBrands": "/Fonts/FontAwesomeBrands.otf",
        }

        page.update()
        window = Dately(page)
        page.on_route_change = window.route_change

        # params from date_view
        page.date_edit_id = None

        # Chnage this based on bagian masing2 (reference: view_list in views.py)
        # page.go("/outfits")
        page.go("/")


if __name__ == '__main__':
    app = MainApp()

    Utils.Connection.create_db_and_tables()
    ft.app(target=app.main, assets_dir="assets")
