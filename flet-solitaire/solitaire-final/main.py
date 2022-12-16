import logging
import random

import flet as ft
from solitaire import Solitaire

# This prototype is move slot and card creating and dealing to a class

# logging.basicConfig(level=logging.DEBUG)



def main(page: ft.Page):

    solitaire = Solitaire()

    page.add(solitaire)


ft.app(target=main, assets_dir="images")
