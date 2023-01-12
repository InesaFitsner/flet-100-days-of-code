CARD_WIDTH = 70
CARD_HEIGTH = 100
DROP_PROXIMITY = 20

import flet as ft

class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank, top, left):
        super().__init__()
        self.mouse_cursor=ft.MouseCursor.MOVE
        self.drag_interval=5
        self.on_pan_start=self.start_drag
        self.on_pan_update=self.drag
        self.on_pan_end=self.drop
        self.suite=suite
        self.rank=rank
        self.face_up=False
        self.top=top
        self.left=left
        self.solitaire = solitaire
        self.slot = None
        self.content=ft.Container(
            width=CARD_WIDTH, 
            height=CARD_HEIGTH, 
            border_radius = ft.border_radius.all(6), 
            content=ft.Image(src="card_back.png"))

    def turn_face_up(self):
        self.face_up = True
        self.content.content.src=f"/images/{self.rank.name}_{self.suite.name}.svg"
        self.update()

    def place(self, slot):
        """Place draggable pile to the slot"""

        if slot in self.solitaire.tableau:
            self.top = slot.top + len(slot.pile) * self.solitaire.card_offset
        else:
            self.top = slot.top
        
        self.left = slot.left

        # remove card from it's original slot, if exists
        if self.slot is not None:
            self.slot.pile.remove(self)
        
        # change card's slot to a new slot
        self.slot = slot

        # add card to the new slot's pile
        slot.pile.append(self)

    def get_draggable_pile(self):
        """returns list of cards that will be dragged together, starting with the current card"""
        if self.slot is not None:
            return self.slot.pile[self.slot.pile.index(self):]
        return [self]

    def start_drag(self, e: ft.DragStartEvent):
        self.solitaire.move_on_top(self.get_draggable_pile())
        self.solitaire.start_top = self.top
        self.solitaire.start_left = self.left
        self.update()

    
    def drag(self, e: ft.DragUpdateEvent):
        draggable_pile = self.get_draggable_pile()
        for card in draggable_pile:
            card.top = max(0, self.top + e.delta_y) + draggable_pile.index(card) * self.solitaire.card_offset
            card.left = max(0, self.left + e.delta_x)
            card.update()


    def drop(self, e: ft.DragEndEvent):
        for slot in self.solitaire.slots:
            if (
                abs(self.top - slot.top) < DROP_PROXIMITY
            and abs(self.left - slot.left) < DROP_PROXIMITY
          ):
                for card in self.get_draggable_pile():
                    card.place(slot)
                    card.update()
                return
           
        self.solitaire.bounce_back(self.get_draggable_pile())
        self.update()