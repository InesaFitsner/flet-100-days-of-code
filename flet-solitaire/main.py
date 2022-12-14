import logging
import random

import flet as ft

# This prototype is move slot and card creating and dealing to a class

# logging.basicConfig(level=logging.DEBUG)


class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color

class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value


class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 500
        self.current_top = 0
        self.current_left = 0
        self.card_offset = 20
        self.controls = []

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()
        self.deal_cards()

    def create_slots(self):
        # self.slots = []
        
        
    
        self.stock = slot(
            solitaire=self, slot_type="stock", top=0, left=0, border=None
        )

        self.waste = slot(
            solitaire=self, slot_type="waste", top=0, left=100, border=None
        )
     
        self.foundation = []
        x = 300
        for i in range(4):
            self.foundation.append(
                slot(
                    solitaire=self,
                    slot_type="foundation",
                    top=0,
                    left=x,
                    border=ft.border.all(1),
                )
            )
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(
                slot(
                    solitaire=self,
                    slot_type="tableau",
                    top=150,
                    left=x,
                    border=ft.border.all(1),
                )
            )
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundation)
        self.controls.extend(self.tableau)
        self.update()

    def create_card_deck(self):
        suites = [
            Suite("Hearts", "RED"),
            Suite("Diamonds", "RED"),
            Suite("Clubs", "BLACK"),
            Suite("Spades", "BLACK"),
        ]
        # colors = ["BLUE", "YELLOW", "GREEN", "RED"]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13)
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))
        # self.stock = self.cards
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        self.update()

    def deal_cards(self):
        # Tableau
        card_index = 0
        first_slot = 0
        while card_index <= 27:
            for slot_index in range(first_slot, len(self.tableau)):
                self.cards[card_index].place(self.tableau[slot_index])
                card_index += 1
            first_slot += 1

        # Reveal top cards in slot piles:
        for number in range(len(self.tableau)):
            self.tableau[number].pile[-1].flip()

        # Stock pile
        for i in range(28, len(self.cards)):
            self.cards[i].place(self.stock)

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.slot.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()
        self.solitaire = solitaire
        self.controls = solitaire.controls
        self.suite = suite
        self.rank = rank
        self.face_up = False
        self.slot = None

        self.mouse_cursor = ft.MouseCursor.MOVE
        # self.visible = False
        self.drag_interval = 5
        self.on_pan_update = self.drag
        self.on_pan_start = self.start_drag
        self.on_pan_end = self.drop
        self.on_double_tap = self.doubleclick
        self.content = ft.Container(
            width=65,
            height=100,
            border_radius=ft.border_radius.all(6),
            border=ft.border.all(2),
            bgcolor="GREEN",
            content=ft.Text(f"{rank.name} of {suite.name}", size=8, color=suite.color),
        )

    def flip(self):
        self.face_up = True
        self.content.bgcolor = "WHITE"
        self.update()

    def move_on_top(self, controls, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            controls.remove(card)
            controls.append(card)
        self.page.update()

    def start_drag(self, e: ft.DragStartEvent):
        if e.control.face_up:
            cards_to_drag = self.cards_to_drag()
            self.move_on_top(self.controls, cards_to_drag)
            # remember card original position to return it back if needed
            self.solitaire.current_top = e.control.top
            self.solitaire.current_left = e.control.left
            # self.page.update()

    def drag(self, e: ft.DragUpdateEvent):
        if e.control.face_up:
            i = 0
            for card in self.cards_to_drag():
                card.top = max(0, self.top + e.delta_y)
                if card.slot.type == "tableau":
                    card.top += i * self.solitaire.card_offset
                card.left = max(0, self.left + e.delta_x)
                i += 1
                card.update()

    def drop(self, e: ft.DragEndEvent):
        if e.control.face_up:
            cards_to_drag = self.cards_to_drag()
            slots = self.solitaire.tableau + self.solitaire.foundation
            # check if card is close to any of the tableau slots
            for slot in slots:
                # compare with top and left position of the upper card in the slot pile
                if (
                    abs(self.top - slot.upper_card_top()) < 40
                    and abs(self.left - slot.left) < 40
                ):
                    # tableau slot
                    # place cards_to_drag to the slot in proximity, if:
                    # *** For tableau slots: if cards' color is different or slot is empty
                    # *** For foundation slots: [TBD]
                    if (
                        slot.type == "tableau"
                        and (
                            len(slot.pile) == 0
                            or (
                                len(slot.pile) != 0
                                and self.suite.color != slot.pile[-1].suite.color
                            )
                        )
                    ) or (
                        slot.type == "foundation"
                        and len(cards_to_drag) == 1
                        and (
                            (len(slot.pile) == 0 and e.control.rank.name == "Ace")
                            or (
                                len(slot.pile) != 0
                                and self.suite.name == slot.pile[-1].suite.name and self.rank.value - slot.pile[-1].rank.value == 1
                            )
                        )
                    ):

                        old_slot = self.slot
                        for card in cards_to_drag:
                            card.place(slot)
                        # reveal top card in old slot if exists
                        if len(old_slot.pile) > 0:
                            old_slot.pile[-1].flip()
                        self.page.update()
                        return

            # return card to original position
            self.solitaire.bounce_back(cards_to_drag)
            self.page.update()

    def doubleclick(self, e):
        if self.slot.type in ('waste', 'tableau'):
            if self.face_up:
                self.move_on_top(self.solitaire.controls, [self])
                old_slot = self.slot
                self.place(self.solitaire.foundation[0])
                if len(old_slot.pile) > 0:
                            old_slot.pile[-1].flip()
                self.page.update()

    def place(self, slot):
        self.top = slot.top
        self.left = slot.left
        if slot.type == "tableau":
            self.top += self.solitaire.card_offset * len(slot.pile)
        if slot.type == "waste":
            self.left += self.solitaire.card_offset * len(slot.pile)

        # remove the card form the old slot's pile if exists
        if self.slot is not None:
            self.slot.pile.remove(self)

        # set card's slot as new slot
        self.slot = slot

        # add the card to the new slot's pile
        slot.pile.append(self)
        self.update()


    def cards_to_drag(self):
        """returns list of cards that will be dragged together, starting with current card"""
        top_pile = []

        if self.slot is not None:
            card_index = self.slot.pile.index(self)

            for card in self.slot.pile:
                if self.slot.pile.index(card) >= card_index:
                    top_pile.append(card)

        return top_pile


class slot(ft.Container):
    def __init__(self, solitaire, slot_type, top, left, border):
        super().__init__()
        self.solitaire = solitaire
        self.pile = []
        self.type = slot_type
        self.width = 65
        self.height = 100
        self.left = left
        self.top = top
        self.border_radius = ft.border_radius.all(6)
        self.border = border

    def upper_card_top(self):
        if self.type == "tableau":
            if len(self.pile) > 1:
                return self.top + self.solitaire.card_offset * (len(self.pile) - 1)
        return self.top


def main(page: ft.Page):

    solitaire = Solitaire()

    page.add(solitaire)


ft.app(target=main)
