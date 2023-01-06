import flet as ft

class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.start_top = 0
        self.start_left = 0
        self.controls = []
        self.slots = []
        self.width = 1000
        self.height = 500

    def move_on_top(self, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            self.controls.remove(card)
            self.controls.append(card)
        self.update()
    
    def bounce_back(self, card):
        """Returns card to its original position"""
        card.top = self.start_top
        card.left = self.start_left