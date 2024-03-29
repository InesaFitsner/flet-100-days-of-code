import flet as ft
from customcolorpicker import CustomColorPicker
from palettecolorpicker import PaletteColorPicker


def main(page: ft.Page):
    color_picker = CustomColorPicker(color="#c8df6f")

    d = ft.AlertDialog(content=color_picker)
    page.dialog = d

    def open_color_picker(e):
        d.open = True
        page.update()

    page.add(ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker))


ft.app(target=main)
