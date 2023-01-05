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
        self.color = color
        self.content=ft.Container(bgcolor=self.color, width=70, height=100)

    def place(self, slot):
        """Place card to the slot"""
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