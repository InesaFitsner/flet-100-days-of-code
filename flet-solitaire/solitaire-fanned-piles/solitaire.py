CARD_OFFSET = 20
SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import flet as ft
from slot import Slot
from card import Card

class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.start_top = 0
        self.start_left = 0
        self.controls = []
        self.slots = []
        self.card_offset = CARD_OFFSET
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()

    def create_slots(self):
        slot1 = Slot(top=0, left=200)
        slot2 = Slot(top=0, left=300)
        slots = [slot1, slot2]
        self.slots.extend(slots)
        self.controls.extend(self.slots)
        self.update()

    def create_card_deck(self):
        card1 = Card(self, color="GREEN", top=0, left=0)
        card2 = Card(self, color="YELLOW", top=0, left=100)
        cards = [card1, card2]
        self.controls.extend(cards)
        self.update()

    def move_on_top(self, draggable_pile):
        """Brings draggable card pile to the top of the stack"""

        for card in draggable_pile:
            self.controls.remove(card)
            self.controls.append(card)
        self.update()
    
    def bounce_back(self, draggable_pile):
        """Returns draggable pile to its original position"""
        for card in draggable_pile:
            card.top = self.start_top + draggable_pile.index(card) * self.card_offset
            card.left = self.start_left
        self.update()