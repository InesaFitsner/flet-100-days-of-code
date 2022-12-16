import logging


import flet as ft
from solitaire import Solitaire

# logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    def start_new_game(e):
        print("New game clicked")
        page.update()

    def show_rules(e):
        print("Solitaire rules")
        page.update()

    def show_settings(e):
        print("Show settings")
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Image(src=f"/images/card.png"),
        leading_width=30,
        title=ft.Text("Flet solitaire"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.TextButton(text="New game", on_click=start_new_game),
            ft.TextButton(text="Rules", on_click=show_rules),
            ft.IconButton(ft.icons.SETTINGS, on_click=show_settings),
            
        ],
    )

    solitaire = Solitaire()

    page.add(solitaire)


ft.app(target=main, assets_dir="images")
