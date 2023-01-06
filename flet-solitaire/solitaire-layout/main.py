import flet as ft
from solitaire import Solitaire
from card import Card


def main(page: ft.Page):

    solitaire = Solitaire()
    
    card1 = Card(solitaire, color="GREEN", top=0, left=0)
    card2 = Card(solitaire, color="YELLOW", top=0, left=100)
    cards = [card1, card2]
    
    solitaire.controls.extend(cards)

    page.add(solitaire)


ft.app(target=main)
