import logging


import flet as ft
from solitaire import Solitaire
from layout import create_appbar

# logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    create_appbar(page)
    solitaire = Solitaire()
    page.add(solitaire)
    
    

ft.app(target=main, assets_dir="images")
