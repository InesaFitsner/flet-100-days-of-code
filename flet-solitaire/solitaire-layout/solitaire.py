CARD_OFFSET = 20
SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import flet as ft
from slot import Slot

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
        #self.create_card_deck()
        #self.deal_cards()


    def create_slots(self):
        self.slots.append(Slot(
            top=0, left=0, slot_type="stock", border=ft.border.all(1)
        ))

        self.slots.append(Slot(
            top=0, slot_type="waste", left=100, border=None
        ))

        x = 300
        for i in range(4):
            self.slots.append(
                Slot(
                    slot_type="foundation",
                    top=0,
                    left=x,
                    border=ft.border.all(1, "outline"),
                )
            )
            x += 100

        x = 0
        for i in range(7):
            self.slots.append(
                Slot(
                    slot_type="tableau",
                    top=150,
                    left=x,
                    border=None
                )
            )
            x += 100

        self.controls.extend(self.slots)
        print(len(self.slots))
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