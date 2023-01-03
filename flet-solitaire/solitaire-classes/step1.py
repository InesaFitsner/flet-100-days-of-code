import flet as ft

# Solitaire class will be inherited from Stack 
# Card class will be inherited from GestureDetector 
# We will move all related to methods and properties to Solitaire(ft.Stack) and Card(ft.GestureDetector)


class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.start_top = 0
        self.start_left = 0
        self.controls = []
        self.slots = []
        self.width = 1000
        self.height = 500

    def move_on_top(self, card):
        """Moves draggable card to the top of the stack"""
        self.controls.remove(card)
        self.controls.append(card)
        self.update()

    def bounce_back(self, card):
        """return card to its original position"""
        card.top = self.start_top
        card.left = self.start_left
        

class Card(ft.GestureDetector):
    def __init__(self, solitaire, color, top, left):
        super().__init__()
        self.mouse_cursor=ft.MouseCursor.MOVE
        self.drag_interval=5
        self.on_pan_start=self.start_drag
        self.on_pan_update=self.drag
        self.on_pan_end=self.drop
        self.left=left
        self.top=top
        self.solitaire = solitaire
        self.color = color
        self.content=ft.Container(bgcolor=self.color, width=70, height=100)

    def place(self, slot):
        """place card to the slot"""
        self.top = slot.top
        self.left = slot.left

    def start_drag(self, e: ft.DragStartEvent):
        self.solitaire.move_on_top(e.control)
        self.solitaire.start_top = e.control.top
        self.solitaire.start_left = e.control.left
        self.update()

    
    def drag(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(self, e: ft.DragEndEvent):
        for slot in self.solitaire.slots:
            if (
                abs(e.control.top - slot.top) < 20
            and abs(e.control.left - slot.left) < 20
          ):
                self.place(slot)
                self.update()
                return
           
        self.solitaire.bounce_back(e.control)
        self.update()

class 


def main(page: ft.Page):

    slot1 = ft.Container(
        width=70, height=100, left=200, top=0, border=ft.border.all(1)
    )

    slot2 = ft.Container(
        width=70, height=100, left=300, top=0, border=ft.border.all(1)
    )

    slots = [slot1, slot2]

    solitaire = Solitaire()
    
    card1 = Card(solitaire, "GREEN", 0, 0)
    card2 = Card(solitaire, "YELLOW", 0, 100)
    cards = [card1, card2]
    
    solitaire.controls = slots + cards
    solitaire.slots = slots
    
    

    page.add(solitaire)


ft.app(target=main)
