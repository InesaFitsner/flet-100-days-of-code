

import flet as ft
from solitaire import Solitaire
from card import Card
from slot import Slot


def main(page: ft.Page):
    slot1 = Slot(top=0, left=200)
    slot2 = Slot(top=0, left=300)

    slots = [slot1, slot2]

    solitaire = Solitaire()
    solitaire.slots = slots
    
    card1 = Card(solitaire, color="GREEN", top=0, left=0)
    card2 = Card(solitaire, color="YELLOW", top=0, left=100)
    cards = [card1, card2]
    
    solitaire.controls = slots + cards

    page.add(solitaire)


ft.app(target=main)
