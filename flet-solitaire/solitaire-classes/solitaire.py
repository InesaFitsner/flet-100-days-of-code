SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import flet as ft

class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.start_top = 0
        self.start_left = 0
        self.controls = []
        self.slots = []
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT

    def move_on_top(self, card):
        """Moves draggable card to the top of the stack"""
        self.controls.remove(card)
        self.controls.append(card)
        self.update()

    def bounce_back(self, card):
        """Returns card to its original position"""
        card.top = self.start_top
        card.left = self.start_left
        self.update()