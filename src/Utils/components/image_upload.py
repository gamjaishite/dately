import flet as ft


class ImageUpload(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__()

    def build(self):
        self.image_upload_modal = ft.AlertDialog(
            title=ft.Text("upload image"),
            open=True,
        )
        return self.image_upload_modal
