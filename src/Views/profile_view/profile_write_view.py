import flet as ft
import Models
import Utils
import Controllers
from Utils.components.notification import Notification


class ProfileEditView(ft.UserControl):
    def __init__(self, page: ft.Page, role: str, id: str | None):
        super().__init__()
        self.page: ft.Page = page
        self.id: str | None = id
        self.controller: Controllers.ProfileController = Controllers.ProfileController()
        self.role = role

        self.default_window_width = 1000

    def build(self):
        if self.role == Models.RoleEnum.main.value:
            self.profile_data: Models.ProfileModel | None = self.controller.get_user().data
        else:
            self.profile_data: Models.ProfileModel | None = self.controller.get_partner_by_id(
                self.id).data
        return self.show_profile_edit_layout()

    def show_profile_edit_layout(self):
        self.save_cancel_buttons = ft.Container(
            right=50,
            bottom=30,
            content=ft.Row(
                controls=[
                    ft.TextButton(
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.MaterialState.HOVERED: "#E4E4E7",
                                ft.MaterialState.DEFAULT: "#FAFAFA",
                            },
                            color={
                                ft.MaterialState.DEFAULT: "#A1A1AA",
                                ft.MaterialState.HOVERED: "#52525B"
                            },
                            overlay_color=ft.colors.TRANSPARENT,
                            shape={
                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                    radius=10)
                            },
                            side=ft.BorderSide(5, "#E4E4E7"),
                        ),
                        content=ft.Text(
                            value="CANCEL",
                            weight=ft.FontWeight.W_600,
                            size=15,
                        ),
                        width=100,
                        on_click=lambda _: self.page.go("/profiles" if self.role == Models.RoleEnum.main.value else
                                                        f"/profiles/partners/{self.id}" if self.id else f"/profiles/partners"),
                    ),
                    ft.TextButton(
                        style=ft.ButtonStyle(
                            bgcolor={
                                ft.MaterialState.HOVERED: "#FBCFE8",
                                ft.MaterialState.DEFAULT: "#FDF2F8",
                            },
                            color={
                                ft.MaterialState.DEFAULT: "#F472B6",
                                ft.MaterialState.HOVERED: "#52525B"
                            },
                            overlay_color=ft.colors.TRANSPARENT,
                            shape={
                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                    radius=10)
                            },
                            side=ft.BorderSide(5, "#FBCFE8"),
                        ),
                        content=ft.Text(
                            value="SAVE",
                            weight=ft.FontWeight.W_600,
                            size=15,
                        ),
                        width=100,
                        on_click=self.save_data,
                    ),
                ]
            )
        )

        return ft.Stack(
            controls=[
                ft.Column(
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
                        self.showProfileEditPage(),
                    ]
                ),
                self.save_cancel_buttons,
            ]
        )

    def page_resize(self, e):
        self.main_row.width = self.page.window_width - \
            Utils.Navbar.width if self.page.window_width else self.default_window_width
        self.main_row.update()

    def showProfileEditPage(self):
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
                    on_click=lambda _: self.page.go('/profiles/partners')
                ),
            ]
        )

        self.picture = self.profile_data.picture if self.profile_data else None
        self.avatar = ft.Image(
            width=100,
            height=100,
            border_radius=ft.BorderRadius(50, 50, 50, 50),
            fit=ft.ImageFit.COVER,
        )

        if self.picture:
            self.avatar.src_base64 = Utils.blob_to_base64(blob=self.picture)
        else:
            self.avatar.src = "/Images/empty.jpg"

        def get_image(e: ft.FilePickerResultEvent):
            # Get the data and save to database
            if e.files and not ("add" in str(self.page.route)):
                image_path = e.files[0].path
                image_size = e.files[0].size
                with open(image_path, 'rb') as f:
                    blob = f.read()

                    request = {
                        "id": self.profile_data.id if self.profile_data else None,
                        "picture": blob,
                        "size": image_size,
                    }

                    result = self.controller.edit_image(request)

                self.page.snack_bar = Notification(result.message)
                self.page.update()

                if result.is_success:
                    self.avatar.src_base64 = Utils.blob_to_base64(blob)
                    self.avatar.update()
            else:
                self.page.snack_bar = Notification(
                    "Please create the profile first 😊")
                self.page.update()

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
            disabled="add" in str(self.page.route),
            on_click=lambda _: self.image_file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["jpg", "png"]
            )
        )

        self.edit_name_input = ft.TextField(
            width=400,
            height=50,
            border_radius=10,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=ft.Padding(12, 0, 12, 0),
            color="#A1A1AA",
            selection_color="#fce7f3",
            cursor_color="#F472B6",
            hint_text="Kazuha Nakamura",
            hint_style=ft.TextStyle(
                color="#d4d4d8",
            ),
            value=self.profile_data.name if self.profile_data else None,
        )
        self.edit_name_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Name",
                        weight=ft.FontWeight.W_600,
                        color="#FBCFE8",
                        size=12,
                    ),
                    self.edit_name_input,
                ]
            )
        )

        self.edit_mbti_input = ft.TextField(
            width=400,
            height=50,
            border_radius=10,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=ft.Padding(12, 0, 12, 0),
            color="#A1A1AA",
            selection_color="#fce7f3",
            cursor_color="#F472B6",
            hint_text="ISTP",
            hint_style=ft.TextStyle(
                color="#d4d4d8",
            ),
            value=self.profile_data.mbti if self.profile_data else None,
        )
        self.edit_mbti_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="MBTI",
                        weight=ft.FontWeight.W_600,
                        color="#FBCFE8",
                        size=12,
                    ),
                    self.edit_mbti_input,
                ]
            )
        )

        self.edit_hobbies_input = ft.TextField(
            width=400,
            height=50,
            border_radius=10,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=ft.Padding(12, 0, 12, 0),
            color="#A1A1AA",
            selection_color="#fce7f3",
            cursor_color="#F472B6",
            hint_text="sleep,Singing,DANCING",
            hint_style=ft.TextStyle(
                color="#d4d4d8",
            ),
            value=self.profile_data.hobbies if self.profile_data else None,
        )
        self.edit_hobbies_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Hobbies (seperates with coma)",
                        weight=ft.FontWeight.W_600,
                        color="#FBCFE8",
                        size=12,
                    ),
                    self.edit_hobbies_input,
                ]
            )
        )

        self.edit_instagram_input = ft.TextField(
            width=400,
            height=50,
            border_radius=10,
            bgcolor="#FAFAFA",
            border_width=0,
            content_padding=ft.Padding(12, 0, 12, 0),
            color="#A1A1AA",
            selection_color="#fce7f3",
            cursor_color="#F472B6",
            hint_text="k_a_z_u_h_a__",
            hint_style=ft.TextStyle(
                color="#d4d4d8",
            ),
            value=self.profile_data.social_media if self.profile_data else None
        )
        self.edit_instagram_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Instagram Username",
                        weight=ft.FontWeight.W_600,
                        color="#FBCFE8",
                        size=12,
                    ),
                    self.edit_instagram_input,
                ]
            )
        )

        self.inputs_container = ft.Container(
            margin=ft.Margin(0, 10, 0, 0),
            height=250,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                height=250,
                controls=[
                    self.edit_name_container,
                    self.edit_mbti_container,
                    self.edit_hobbies_container,
                    self.edit_instagram_container,
                ]
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
                self.inputs_container,
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

    def save_data(self, e):
        request = {
            "id": self.profile_data.id if self.profile_data else None,
            "role": self.role,
            "name": self.edit_name_input.value,
            "mbti": self.edit_mbti_input.value,
            "hobbies": self.edit_hobbies_input.value,
            "social_media": self.edit_instagram_input.value,
        }

        result = self.controller.add_profile(request) if "add" in str(
            self.page.route) else self.controller.edit_profile(request)

        self.page.snack_bar = Notification(result.message)
        self.page.update()

        if result.is_success:
            self.page.go("/profiles" if self.role ==
                         Models.RoleEnum.main.value else f"/profiles/partners/{self.id}" if self.id else "/profiles/partners")
