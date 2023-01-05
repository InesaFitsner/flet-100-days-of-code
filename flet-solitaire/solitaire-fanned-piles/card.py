CARD_OFFSET = 20

import flet as ft

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
        self.slot = None
        self.color = color
        self.content=ft.Container(bgcolor=self.color, width=70, height=100)

    def place(self, slot):
        """Place card to the slot"""
        print(len(self.get_pile_to_move()))

        self.top = slot.top + len(slot.pile) * CARD_OFFSET
        self.left = slot.left

        # remove card from it's original slot, if exists
        if self.slot is not None:
            self.slot.pile.remove(self)
        
        # change card's slot to a new slot
        self.slot = slot

        # add card to the new slot's pile
        slot.pile.append(self)

    def get_pile_to_move(self):
        """returns list of cards that will be dragged together, starting with the current card"""
        if self.slot is not None:
            return self.slot.pile[self.slot.pile.index(self):]
        return [self]

    def start_drag(self, e: ft.DragStartEvent):
        self.solitaire.move_on_top(self)
        self.solitaire.start_top = self.top
        self.solitaire.start_left = self.left
        self.update()

    
    def drag(self, e: ft.DragUpdateEvent):
        self.top = max(0, self.top + e.delta_y)
        self.left = max(0, self.left + e.delta_x)
        self.update()

    def drop(self, e: ft.DragEndEvent):
        for slot in self.solitaire.slots:
            if (
                abs(self.top - slot.top) < 20
            and abs(self.left - slot.left) < 20
          ):
                self.place(slot)
                self.update()
                return
           
        self.solitaire.bounce_back(self)
        self.update()