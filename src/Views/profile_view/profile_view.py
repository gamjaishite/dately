from typing import List

import flet as ft
import Utils
import Controllers
import Models
from Utils.components.notification import Notification
from Utils.components.deletePopup import DeletePopup


class ProfileView(ft.UserControl):
    def __init__(self, page: ft.Page, role: str, id: str | None):
        super().__init__()
        self.page: ft.Page = page
        self.id = id
        self.controller: Controllers.ProfileController = Controllers.ProfileController()

        # Get profile data
        self.role = role
        self.default_window_width = 1000

    def build(self):
        if self.role == Models.RoleEnum.main.value:
            self.profile_data: Models.ProfileModel = self.controller.get_user().data
        elif self.id:
            self.profile_data: Models.ProfileModel = self.controller.get_partner_by_id(
                self.id).data

        self.delete_popup_component = DeletePopup()

        self.main = ft.Row(
            spacing=0,
            controls=[
                self.delete_popup_component,
                self.show_profile_layout(),
            ]
        )
        return self.main

    def show_profile_layout(self):
        modify_button_row: List[ft.Control] = [
            ft.TextButton(
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
                    value="\uf044;",
                    font_family="FontAwesome",
                    size=20,
                ),
                on_click=lambda _: self.page.go(
                    "/profiles/edit" if self.role == Models.RoleEnum.main.value else f"/profiles/partners/{self.id}/edit")
            )
        ]

        if self.role == Models.RoleEnum.partner.value:
            modify_button_row.append(
                ft.TextButton(
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
                        value="\uf2ed;",
                        font_family="FontAwesome",
                        size=20,
                    ),
                    on_click=lambda _: self.showDeletePopUp()
                )
            )

        self.modify_buttons = ft.Container(
            margin=ft.Margin(0, 10, 0, 0),
            right=30,
            bottom=20,
            content=ft.Row(
                controls=modify_button_row
            )
        )

        return ft.Stack(
            controls=[
                ft.Column(
                    # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                        self.show_profile_user_page(),
                    ]
                ),
                self.modify_buttons,
            ]
        )

    def page_resize(self, e):
        self.main_row.width = self.page.window_width - \
            Utils.Navbar.width if self.page.window_width else self.default_window_width
        self.main_row.update()

    def show_profile_user_page(self):
        self.page.on_resize = self.page_resize
        self.row_buttons = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.TextButton(
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.MaterialState.HOVERED: "#FBCFE8",
                            ft.MaterialState.DEFAULT: "#FBCFE8" if self.role == Models.RoleEnum.main.value else "#FDF2F8",
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
                    on_click=lambda _: self.page.go("/profiles")
                ),
                ft.TextButton(
                    style=ft.ButtonStyle(
                        bgcolor={
                            ft.MaterialState.HOVERED: "#FBCFE8",
                            ft.MaterialState.DEFAULT: "#FBCFE8" if self.role == Models.RoleEnum.partner.value else "#FDF2F8",
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
                    on_click=lambda _: self.page.go("/profiles/partners")
                ),
            ]
        )

        # Content Section

        self.picture = self.profile_data.picture
        self.avatar = ft.Image(
            width=100,
            height=100,
            border_radius=ft.BorderRadius(50, 50, 50, 50),
            fit=ft.ImageFit.COVER,
        )
        if self.picture:
            self.avatar.src_base64 = Utils.blob_to_base64(self.picture)
        else:
            self.avatar.src = "/Images/empty.jpg"

        def get_image(e: ft.FilePickerResultEvent):
            # Get the data and save to database
            if e.files:
                image_path = e.files[0].path
                image_size = e.files[0].size
                with open(image_path, 'rb') as f:
                    blob = f.read()

                    request = {
                        "id": self.profile_data.id,
                        "picture": blob,
                        "size": image_size,
                    }

                    result = self.controller.edit_image(request)

                self.page.snack_bar = Notification(result.message)
                self.page.update()

                if result.is_success:
                    self.avatar.src_base64 = Utils.blob_to_base64(blob)
                    self.avatar.update()

        self.image_file_picker = ft.FilePicker(
            on_result=get_image,
        )
        self.page.overlay.append(self.image_file_picker)

        self.change_avatar_button = ft.TextButton(
            content=ft.Text(
                value="change"
            ),
            style=ft.ButtonStyle(
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                    ft.MaterialState.HOVERED: "#FDF2F8",
                },
                overlay_color={
                    ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
                },
                color="#F9A8D4"
            ),
            on_click=lambda _: self.image_file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["jpg", "png"]
            )
        )

        self.name_caontainer = ft.Container(
            padding=10,
            bgcolor="#FAFAFA",
            width=400,
            alignment=ft.alignment.center,
            border_radius=10,
            content=ft.Text(
                value=self.profile_data.name,
                weight=ft.FontWeight.W_600,
                text_align=ft.TextAlign.CENTER,
                color="#52525B",
                size=20,
            )
        )

        self.mbti_container = ft.Container(
            padding=10,
            bgcolor="#FAFAFA",
            width=400,
            alignment=ft.alignment.center,
            border_radius=10,
            content=ft.Text(
                value=self.profile_data.mbti if self.profile_data.mbti else "---",
                weight=ft.FontWeight.W_600,
                color="#A1A1AA",
                size=15,
            )
        )

        hobbies = []
        if self.profile_data.hobbies:
            for hobby in self.profile_data.hobbies.split(","):
                if len(hobby.strip()) > 0:
                    hobbies.append(hobby.strip().lower())
        hobbies_rows: List[ft.Control] = []

        for hobby in hobbies:
            hobbies_rows.append(
                ft.Container(
                    bgcolor="#FCE7F3",
                    padding=ft.Padding(5, 5, 5, 5),
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                    content=ft.Text(
                        value=hobby,
                        weight=ft.FontWeight.W_600,
                        color="#A1A1AA",
                        size=15,
                    )
                )
            )

        self.hobbies_container = ft.Container(
            padding=10,
            bgcolor="#FAFAFA",
            width=400,
            alignment=ft.alignment.center,
            border_radius=10,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="Hobbies",
                        weight=ft.FontWeight.W_600,
                        color="#A1A1AA",
                        size=15,
                    ),
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=hobbies_rows,
                    )
                ],
            ),
        )

        instagram_handle = ""
        if self.profile_data.social_media:
            instagram_handle = self.profile_data.social_media

        self.social_media_container = ft.Container(
            padding=10,
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
                        value=f"@{instagram_handle}",
                        weight=ft.FontWeight.W_600,
                        color="#A1A1AA",
                    )
                ],
            ),
        )

        self.attributes_container = ft.Container(
            margin=ft.Margin(0, 10, 0, 0),
            content=ft.Column(
                spacing=10,
                height=350,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    self.name_caontainer,
                    self.mbti_container,
                    self.hobbies_container,
                    self.social_media_container,
                ],
            )
        )

        self.content_columns = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=2,
            controls=[
                ft.Container(
                    bgcolor="#FDF2F8",
                    padding=10,
                    content=self.avatar,
                    border_radius=ft.BorderRadius(60, 60, 60, 60),
                ),
                self.change_avatar_button,
                self.attributes_container,
            ]
        )

        self.main_row = ft.Container(
            alignment=ft.alignment.center,
            width=self.page.width - Utils.Navbar.width,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.Padding(0, 10, 0, 10),
                        alignment=ft.alignment.center,
                        content=self.row_buttons,
                    ),
                    ft.Container(
                        expand=True,
                        margin=ft.Margin(0, 10, 0, 0),
                        alignment=ft.alignment.center,
                        content=self.content_columns,
                    ),
                ]
            )
        )

        return self.main_row

    def showDeletePopUp(self):
        self.delete_popup_component.show(lambda: self.delete_profile(), title="Delete Dates?", actionTitle="DELETE")

    def delete_profile(self):
        result = self.controller.delete_partner(self.id)

        self.page.snack_bar = Notification(result.message)
        self.page.update()

        self.page.go("/profiles/partners")
