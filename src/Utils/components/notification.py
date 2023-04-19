import flet as ft

class Notification(ft.UserControl):

    def __init__(self, msg, **kwargs):
        super().__init__()
        self.msg = msg

    def build(self):
        return ft.SnackBar(
            content=ft.Text(
                value=self.msg,
                text_align=ft.TextAlign.CENTER,
                color="#52525B"
            ),
            open=True,
            bgcolor="#FBCFE8"
        )