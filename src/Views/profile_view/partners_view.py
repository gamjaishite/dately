import flet as ft
import Controllers
import Utils
import Models


class PartnersView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.controller: Controllers.ProfileController = Controllers.ProfileController()

        self.default_window_width = 1000

    def build(self):
        self.partners_data = self.controller.get_partners()
        return self.show_partners_layout()

    def page_resize(self, e):
        self.main_row.width = self.page.window_width - \
            Utils.Navbar.width if self.page.window_width else self.default_window_width
        self.main_row.update()

    def show_partners_layout(self):
        return ft.Stack(
            controls=[
                ft.Column(
                    # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            padding=20,
                            content=ft.Text(
                                value="Profiles",
                                font_family="ShantellSans-SemiBold",
                                size=40,
                                color="#F472B6",
                            ),
                        ),
                        self.show_partners_page(),
                    ]),
                ft.Container(
                    margin=ft.Margin(0, 10, 0, 0),
                    right=30,
                    bottom=20,
                    content=ft.TextButton(
                        style=ft.ButtonStyle(
                            overlay_color=ft.colors.TRANSPARENT,
                            bgcolor={
                                ft.MaterialState.DEFAULT: "#FDF2F8",
                                ft.MaterialState.HOVERED: "#F9A8D4",
                            },
                            color={
                                ft.MaterialState.DEFAULT: "#F472B6",
                                ft.MaterialState.HOVERED: "#52525B",
                            }
                        ),
                        content=ft.Text(
                            value="\u002b;",
                            font_family="FontAwesome",
                            size=20,
                        ),
                        on_click=lambda _: self.page.go(
                            "/profiles/partners/add")
                    )
                )
            ]
        )

    def show_partners_page(self):
        self.page.on_resize = self.page_resize
        self.main_row = ft.Container(
            alignment=ft.alignment.center,
            width=self.page.width - Utils.Navbar.width,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.Padding(0, 10, 0, 10),
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.TextButton(
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.MaterialState.HOVERED: "#FBCFE8",
                                            ft.MaterialState.DEFAULT: "#FDF2F8",
                                        },
                                        color={
                                            ft.MaterialState.DEFAULT: "#52525B",
                                        },
                                        overlay_color=ft.colors.TRANSPARENT,
                                        shape={
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                                radius=10)
                                        },
                                        elevation=2,
                                        shadow_color={
                                            ft.MaterialState.DEFAULT: "#FBCFE8",
                                        }
                                    ),
                                    content=ft.Text(
                                        value="Me",
                                        weight=ft.FontWeight.W_600,
                                        size=20,
                                    ),
                                    width=200,
                                    on_click=lambda _: self.page.go(
                                        "/profiles")
                                ),
                                ft.TextButton(
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.MaterialState.HOVERED: "#FBCFE8",
                                            ft.MaterialState.DEFAULT: "#FBCFE8",
                                        },
                                        color={
                                            ft.MaterialState.DEFAULT: "#52525B",
                                        },
                                        overlay_color=ft.colors.TRANSPARENT,
                                        shape={
                                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                                radius=10)
                                        },
                                        elevation=2,
                                        shadow_color={
                                            ft.MaterialState.DEFAULT: "#FBCFE8",
                                        }
                                    ),
                                    content=ft.Text(
                                        value="Partners",
                                        weight=ft.FontWeight.W_600,
                                        size=20,
                                    ),
                                    width=200,
                                    on_click=lambda _: self.page.go(
                                        "/profiles/partners")
                                ),
                            ]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        margin=ft.Margin(0, 10, 0, 0),
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=2,
                            controls=[
                                self.fetchPartnersList(),
                            ]
                        ),
                    ),
                ]
            )
        )
        return self.main_row

    def fetchPartnersList(self):
        cards = ft.GridView(max_extent=400, child_aspect_ratio=0.75, width=1200, height=425, run_spacing=40, spacing=40,
                            padding=20)

        for partner in self.partners_data.data:
            cards.controls.append(self.getPartners(partner))

        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Container(
                # bgcolor="#FFFFFF",
                padding=10,
                content=ft.Container(
                    padding=ft.padding.only(top=20),
                    alignment=ft.alignment.center,
                    content=cards if len(
                        self.partners_data.data) > 0 else self.getEmptyColumn()
                ),
                border_radius=ft.BorderRadius(60, 60, 60, 60),
            )
        )

    def getPartners(self, data: Models.ProfileModel):
        self.avatarPartner = ft.Image(
            width=100,
            height=100,
            border_radius=ft.BorderRadius(50, 50, 50, 50),
            fit=ft.ImageFit.COVER,
        )
        if data.picture:
            self.avatarPartner.src_base64 = Utils.blob_to_base64(
                blob=data.picture)
        else:
            self.avatarPartner.src = "/Images/empty.jpg"

        self.namePartner_container = ft.Container(
            margin=ft.margin.only(left=30, right=30, top=30, bottom=10),
            padding=10,
            bgcolor="#FAFAFA",
            width=400,
            alignment=ft.alignment.center,
            border_radius=10,
            content=ft.Text(
                value=data.name,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER,
                color="#52525B",
                size=20,
            )
        )
        self.mbtiPartner_container = ft.Container(
            padding=10,
            margin=ft.margin.only(left=30, right=30, bottom=10),
            bgcolor="#FAFAFA",
            width=400,
            alignment=ft.alignment.center,
            border_radius=10,
            content=ft.Text(
                value=data.mbti if data.mbti else "---",
                weight=ft.FontWeight.W_600,
                color="#A1A1AA",
                size=15,
            )
        )
        self.social_media_partner_container = ft.Container(
            padding=40,
            margin=ft.margin.only(left=30, right=30, bottom=10),
            bgcolor="#FAFAFA",
            width=400,
            alignment=ft.alignment.center,
            border_radius=10,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=1,
                controls=[
                    ft.Text(
                        value="\uf16d;",
                        weight=ft.FontWeight.W_600,
                        font_family="FontAwesomeBrands",
                        color="#F472B6",
                        size=25,
                    ),
                    ft.Text(
                        value=f"@{data.social_media}",
                        weight=ft.FontWeight.W_600,
                        color="#A1A1AA",
                    )
                ],
            ),
        )
        result = ft.Container(
            border_radius=10,
            width=1200,
            height=450,
            # padding=ft.padding.symmetric(horizontal=100),
            bgcolor="#FDF2F8",
            content=ft.ElevatedButton(
                # height=75,
                style=ft.ButtonStyle(
                    bgcolor="#FDF2F8",
                    overlay_color="#e6e3e3",
                    shape=ft.RoundedRectangleBorder(radius=10),
                    elevation=0.05,
                ), content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                    controls=[
                        ft.Container(
                            bgcolor="#FBCFE8",
                            padding=5,
                            content=self.avatarPartner,
                            border_radius=ft.BorderRadius(60, 60, 60, 60),
                        ),
                        self.namePartner_container,
                        self.mbtiPartner_container,
                        self.social_media_partner_container
                    ]
                ),
                on_click=lambda _: self.page.go(
                    f"/profiles/partners/{data.id}")
            )
        )

        return result

    def getEmptyColumn(self):
        return ft.Container(
            # bgcolor="#FFFFFF",
            padding=10,
            content=ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value="\ue4ff;",
                            font_family="FontAwesome",
                            color="#FCE7F3",
                            size=146,
                        ),
                        ft.Text(
                            value="Empty Partners",
                            font_family="ShantellSans-SemiBold",
                            size=32,
                            color="#FCE7F3",
                        )
                    ]
                )
            ),
            border_radius=ft.BorderRadius(20, 20, 20, 20),
        )
