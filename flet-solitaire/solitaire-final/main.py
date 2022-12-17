import logging


import flet as ft
from solitaire import Solitaire
from settings import Settings
from layout import create_appbar

# logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    
    def on_new_game(settings):
        page.controls.pop()
        new_solitaire = Solitaire(settings)
        page.add(new_solitaire)
        page.update()
    
    settings = Settings()
    create_appbar(page, settings, on_new_game)

    
    solitaire = Solitaire(settings)
    page.add(solitaire)
    

ft.app(target=main, assets_dir="images")
