import flet as ft

class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.pile=[]
        self.width=70
        self.height=100
        self.left=left
        self.top=top
        self.border=ft.border.all(1)
