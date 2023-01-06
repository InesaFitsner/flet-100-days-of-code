SLOT_WIDTH = 70
SLOT_HEIGHT = 100

import flet as ft

class Slot(ft.Container):
    def __init__(self, top, left, slot_type, border):
        super().__init__()
        self.pile=[]
        self.width=SLOT_WIDTH
        self.height=SLOT_HEIGHT
        self.left=left
        self.top=top
        self.slot_type = slot_type
        self.border=border
        self.border_radius = ft.border_radius.all(6)
