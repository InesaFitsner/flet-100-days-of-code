import flet as ft

class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()
        self.solitaire = solitaire
        self.suite = suite
        self.rank = rank
        self.face_up = False
        self.slot = None

        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_update = self.drag
        self.on_pan_start = self.start_drag
        self.on_pan_end = self.drop
        self.on_tap = self.click
        self.on_double_tap = self.doubleclick
        self.content = ft.Container(
            width=70,
            height=100,
            border_radius=ft.border_radius.all(6),
            #content=ft.Image(src=f"/images/card_back.svg"),
            content=ft.Image(src=self.solitaire.settings.card_back)
        )

    def turn_face_up(self):
        self.face_up = True
        self.content.content.src=f"/images/{self.rank.name}_{self.suite.name}.svg"
        self.update()

    
    def turn_face_down(self):
        self.face_up = False
        #self.content.content.src=f"/images/card_back.svg"
        self.content.content.src=self.solitaire.settings.card_back
        self.update()
    
    def can_be_moved(self):
        if self.face_up and self.slot.type != 'waste':
            return True
        if self.slot.type == 'waste' and len(self.solitaire.waste.pile)-1 == self.solitaire.waste.pile.index(self):
            return True
        return False

    def start_drag(self, e: ft.DragStartEvent):
        #if e.control.face_up:
        if self.can_be_moved():
            cards_to_drag = self.get_partial_pile()
            self.solitaire.move_on_top(cards_to_drag)
            # remember card original position to return it back if needed
            self.solitaire.current_top = e.control.top
            self.solitaire.current_left = e.control.left
            # self.page.update()

    def drag(self, e: ft.DragUpdateEvent):
        if self.can_be_moved():
            i = 0
            for card in self.get_partial_pile():
                card.top = max(0, self.top + e.delta_y)
                if card.slot.type == "tableau":
                    card.top += i * self.solitaire.card_offset
                card.left = max(0, self.left + e.delta_x)
                i += 1
                card.update()

    def drop(self, e: ft.DragEndEvent):
        if self.can_be_moved():
            cards_to_drag = self.get_partial_pile()
            slots = self.solitaire.tableau + self.solitaire.foundation
            # check if card is close to any of the tableau or foundation slots
            for slot in slots:
                # compare with top and left position of the top card in the slot pile
                if (
                    abs(self.top - slot.upper_card_top()) < 40
                    and abs(self.left - slot.left) < 40
                ):  
                    if (
                        slot.type == "tableau"
                        and self.solitaire.check_tableau_rules(
                            self, slot.get_top_card()
                        )
                    ) or (
                        slot.type == "foundation"
                        and len(cards_to_drag) == 1
                        and self.solitaire.check_foundation_rules(
                            self, slot.get_top_card()
                        )
                    ):

                        old_slot = self.slot
                        for card in cards_to_drag:
                            card.place(slot)
                        # reveal top card in old tableau slot if exists
                        #if len(old_slot.pile) > 0 and old_slot.type == "tableau":
                        #    old_slot.get_top_card().turn_face_up()
                        self.solitaire.display_waste()
                        self.page.update()

                        return

            # return card to original position
            self.solitaire.bounce_back(cards_to_drag)
            self.page.update()

    def doubleclick(self, e):
        if self.slot.type in ("waste", "tableau"):
            if self.face_up:
                #self.move_on_top(self.solitaire.controls, [self])
                self.solitaire.move_on_top([self])
                old_slot = self.slot
                for slot in self.solitaire.foundation:
                    if self.solitaire.check_foundation_rules(self, slot.get_top_card()):
                        # if True:
                        self.place(slot)
                        #if len(old_slot.pile) > 0:
                            #old_slot.get_top_card().turn_face_up()
                        self.solitaire.display_waste()
                        self.page.update()
                        return

    def click(self, e):
        if self.slot.type == "stock":
            print("Clicked on stock pile")
            for i in range(
                min(self.solitaire.settings.waste_size, len(self.solitaire.stock.pile))
            ):
                top_card = self.solitaire.stock.pile[-1]
                #self.move_on_top(self.solitaire.controls, [top_card])
                #self.solitaire.move_on_top([top_card])
                top_card.place(self.solitaire.waste)
                top_card.turn_face_up()
            self.solitaire.display_waste()
            self.page.update()

        if self.slot.type == "tableau":
            if self.face_up == False and len(self.slot.pile)-1 == self.slot.pile.index(self):
                self.turn_face_up()

    def place(self, slot):
        self.top = slot.top
        self.left = slot.left
        if slot.type == "tableau":
            self.top += self.solitaire.card_offset * len(slot.pile)

        # remove the card form the old slot's pile if exists

        if self.slot is not None:
            # if self.slot.type == 'waste':
            #    self.solitaire.update_waste()
            self.slot.pile.remove(self)

        # set card's slot as new slot
        self.slot = slot

        # add the card to the new slot's pile
        slot.pile.append(self)
        self.solitaire.move_on_top([self])
        self.update()

    def get_partial_pile(self):
        """returns list of cards that will be dragged together, starting with the current card"""
        partial_pile = []

        if self.slot is not None:
            card_index = self.slot.pile.index(self)

            for card in self.slot.pile:
                if self.slot.pile.index(card) >= card_index:
                    partial_pile.append(card)

        return partial_pile