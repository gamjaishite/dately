import flet as ft
import sys
from Models.profile_model.profile_model import ProfileModel
import Utils

class ProfileBoxStyle():
    def __init__(
            self, 
            bgColor: str = ft.colors.TRANSPARENT, 
            rowBackgroundColor: str = "#FFFFFF",
            nameFontColor: str = "#52525B",
            defaultFontColor: str = "#A1A1AA",
            hobbyBackgroundColor: str = "#FCE7F3",
            rowWidth: int = sys.maxsize,
            padding: int = 5,
            borderRadius: int = 10,
            profilPictureRadius: int = 100,
            profilBorderWidth: int = 4,
            normalFontSize: int = 15,
            smallFontSize: int = 12,
            instagram_icon: str = "\uf16d;"
        ):

        self.bgColor = bgColor
        self.rowBackgroundColor = rowBackgroundColor
        self.nameFontColor = nameFontColor
        self.defaultFontColor = defaultFontColor
        self.hobbyBackgroundColor = hobbyBackgroundColor
        self.rowWidth = rowWidth
        self.padding = padding
        self.borderRadius = borderRadius
        self.profilPictureRadius = profilPictureRadius
        self.profilBorderWidth = profilBorderWidth
        self.normalFontSize = normalFontSize
        self.smallFontSize = smallFontSize
        self.instagram_icon = instagram_icon
        
    
class ProfileBoxConfig():
    def __init__(self, data: ProfileModel, style: ProfileBoxStyle = ProfileBoxStyle(), **kwargs):
        self.data = data
        self.style = style


class ProfileBox(ft.UserControl):

    def __init__(self, profileConfig: ProfileBoxConfig, **kwargs):
        super().__init__()
        self.config = profileConfig

    def build(self):
        
        # Styles
        bgColor = self.config.style.bgColor
        rowBackgroundColor = self.config.style.rowBackgroundColor
        nameFontColor = self.config.style.nameFontColor
        defaultFontColor = self.config.style.defaultFontColor
        hobbyBackgroundColor = self.config.style.hobbyBackgroundColor
        rowWidth = self.config.style.rowWidth
        padding = self.config.style.padding
        borderRadius = self.config.style.borderRadius
        profilPictureRadius = self.config.style.profilPictureRadius
        profilBorderWidth = self.config.style.profilBorderWidth
        normalFontSize = self.config.style.normalFontSize
        smallFontSize = self.config.style.smallFontSize
        instagram_icon = self.config.style.instagram_icon

        # Data
        hobbiesString = ""
        contactString = "@"
        mbti = "---"

        if (self.config.data.hobbies):
            hobbiesString = self.config.data.hobbies.split(",")

        if (self.config.data.social_media):
            contactString += self.config.data.social_media

        if (self.config.data.mbti):
            mbti = self.config.data.mbti

        avatar = ft.Image(
            width=100,
            height=100,
            border_radius=profilPictureRadius,
            fit=ft.ImageFit.COVER,
        )

        if self.config.data.picture:
            avatar.src_base64 = Utils.blob_to_base64(self.config.data.picture)
        else:
            avatar.src = "/Images/empty.jpg"

        hobbies = []
        for hobby in hobbiesString:
            hobbies.append(
                ft.Container(
                    padding=padding,
                    bgcolor=hobbyBackgroundColor,
                    border_radius=borderRadius,
                    content=ft.Text(
                        value=hobby,
                        font_family="ShantellSans-SemiBold",
                        size=smallFontSize,
                        color=defaultFontColor,
                        bgcolor=hobbyBackgroundColor,
                        text_align=ft.TextAlign.CENTER
                    ),
                ),
            )

        contacts = []
        contacts.append(
            ft.Container(
                padding=padding,
                border_radius=borderRadius,
                content=ft.Text(
                    value=contactString,
                    font_family="ShantellSans-SemiBold",
                    size=smallFontSize,
                    color=defaultFontColor,
                    text_align=ft.TextAlign.CENTER
                ),
            ),

        )

        return ft.Container(
            bgcolor=bgColor,
            border_radius=borderRadius,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Container(
                        border=ft.border.all(
                            width=profilBorderWidth, color="#FBCFE8"),
                        border_radius=profilPictureRadius,
                        image_fit=ft.ImageFit.FILL,

                        content=avatar
                    ),

                    ft.Container(
                        padding=padding,
                        bgcolor=rowBackgroundColor,
                        width=rowWidth,
                        border_radius=borderRadius,
                        content=ft.Text(
                            value=self.config.data.name,
                            font_family="ShantellSans-SemiBold",
                            size=normalFontSize,
                            color=nameFontColor,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ),

                    ft.Container(
                        padding=padding,
                        bgcolor=rowBackgroundColor,
                        width=rowWidth,
                        border_radius=borderRadius,
                        content=ft.Text(
                            value=mbti,
                            font_family="ShantellSans-SemiBold",
                            size=smallFontSize,
                            color=defaultFontColor,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ),

                    ft.Container(
                        padding=padding,
                        bgcolor=rowBackgroundColor,
                        width=rowWidth,
                        border_radius=borderRadius,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    value="Hobbies",
                                    font_family="ShantellSans-SemiBold",
                                    size=smallFontSize,
                                    color=defaultFontColor,
                                    text_align=ft.TextAlign.CENTER
                                ),

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    wrap=True,
                                    controls=hobbies
                                )
                            ]
                        )
                    ),

                    ft.Container(
                        padding=padding,
                        bgcolor=rowBackgroundColor,
                        width=rowWidth,
                        border_radius=borderRadius,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    value=instagram_icon,
                                    font_family="FontAwesomeBrands",
                                    color="#F472B6",
                                    size=30,
                                ),

                                ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=contacts
                                )
                            ]
                        )
                    )
                ]
            )
        )