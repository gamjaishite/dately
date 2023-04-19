import flet as ft

import Views as v
from Utils.components.navbar import Navbar
from Controllers import ProfileController
from Models import RoleEnum


class ViewList():
    def __init__(self, page: ft.Page):
        self.page = page
        self.viewlist = {
            "/": ft.View(
                route="/",
                controls=[
                    v.InitialView(self.page)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
            ),
            "/profiles": ft.View(
                route="/profiles",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/profiles"),
                            v.ProfileView(
                                self.page, RoleEnum.main.value, None),
                        ]
                    )
                ],
                padding=0,
            ),
            "/profiles/edit": ft.View(
                route="/profiles/edit",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/profiles"),
                            v.ProfileEditView(
                                self.page, RoleEnum.main.value, None),
                        ]
                    )
                ],
                padding=0,
            ),
            "/profiles/partners": ft.View(
                route="profiles/partners",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/profiles"),
                            v.PartnersView(self.page),
                        ]
                    )
                ],
                padding=0,
            ),
            "/profiles/partners/add": ft.View(
                route="profiles/partners/add",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, '/profiles'),
                            v.ProfileEditView(
                                self.page, RoleEnum.partner.value, None),
                        ]
                    )
                ],
                padding=0,
            ),
            "/dates": ft.View(
                route="/dates",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/dates"),
                            v.DateView(self.page),
                        ]
                    ),
                ],
                padding=0,
            ),
            "/dates/edit": ft.View(
                route="/dates/edit",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/dates"),
                            v.DateEditView(self.page),
                        ]
                    ),
                ],
                padding=0,
            ),

            "/histories": ft.View(
                route="/histories",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/histories"),
                            v.HistoryView(self.page),
                        ]
                    ),
                ],
                padding=0,
            ),
            "/outfits": ft.View(
                route="/outfits",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/outfits"),
                            v.OutfitView(self.page),
                        ]
                    ),
                ],
                padding=0,
            ),
            "/outfits/edit": ft.View(
                route="/outfits/edit",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(page, "/outfits"),
                            v.OutfitEditView(page),
                        ]
                    ),
                ],
                padding=0,
            ),
        }

    def get_view(self, path):
        self.troute = ft.TemplateRoute(str(self.page.route))
        if self.troute.match("/profiles/partners/:id") and self.troute.id != 'add':
            self.viewlist[f"/profiles/partners/{self.troute.id}"] = ft.View(
                route=f"/profiles/partners/{self.troute.id}",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/profiles"),
                            v.ProfileView(
                                self.page, RoleEnum.partner.value, self.troute.id),
                        ]
                    ),
                ],
                padding=0,
            )
        elif self.troute.match("/profiles/partners/:id/edit"):
            self.viewlist[f"/profiles/partners/{self.troute.id}/edit"] = ft.View(
                route=f"/profiles/partners/{self.troute.id}/edit",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/profiles"),
                            v.ProfileEditView(
                                self.page, RoleEnum.partner.value, self.troute.id),
                        ]
                    )
                ],
                padding=0,
            )
        elif self.troute.match("/outfits/edit/:id"):
            self.viewlist[f"/outfits/edit/{self.troute.id}"] = ft.View(
                route=f"/outfits/edit/{self.troute.id}",
                controls=[
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            Navbar(self.page, "/outfits"),
                            v.OutfitEditView(self.page, id=self.troute.id),
                        ]
                    ),
                ],
                padding=0,
            )

        return self.viewlist[path]


class ViewManager():
    def __init__(self, page: ft.Page):
        self.page = page
        self.view_list = ViewList(page)

    def route_change(self, route):
        self.page.views.clear()

        if ProfileController().get_user().is_success:
            if self.page.route == "/":
                self.page.route = "/dates"
        else:
            self.page.route = "/"

        self.page.views.append(self.view_list.get_view(self.page.route))

        self.page.update()
