import logging
import random

import flet as ft

# This prototype is move space and card creating and dealing to a class

# logging.basicConfig(level=logging.DEBUG)


class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


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
        self.create_spaces()
        self.create_card_deck()
        self.deal_cards()

    def create_spaces(self):
        # self.spaces = []
        self.foundation = []
        self.tableau = []
        # stock space index 0
        self.stock = Space(
            solitaire=self, space_type="stock", top=0, left=0, border=None
        )

        # waste spaces index 1-3
        # x = 100
        # for i in range(3):
        self.waste = Space(
            solitaire=self, space_type="waste", top=0, left=100, border=None
        )
        #    x += 20

        x = 300
        for i in range(4):
            self.foundation.append(
                Space(
                    solitaire=self,
                    space_type="foundation",
                    top=0,
                    left=x,
                    border=ft.border.all(1),
                )
            )
            x += 100

        # bottom spaces (plateau piles)
        x = 0
        for i in range(7):
            self.tableau.append(
                Space(
                    solitaire=self,
                    space_type="tableau",
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
        values = [
            "Ace",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "Jack",
            "Queen",
            "King",
        ]

        self.cards = []

        for suite in suites:
            for value in values:
                self.cards.append(Card(solitaire=self, suite=suite, value=value))
        # self.stock = self.cards
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        self.update()

    def deal_cards(self):
        # Tableau
        card_index = 0
        first_space = 0
        while card_index <= 27:
            for space_index in range(first_space, len(self.tableau)):
                self.cards[card_index].place(self.tableau[space_index])
                card_index += 1
            first_space += 1

        # Reveal top cards in space piles:
        for number in range(len(self.tableau)):
            self.tableau[number].pile[-1].reveal()

        # Stock pile
        for i in range(28, len(self.cards)):
            self.cards[i].place(self.stock)
            # print(f"Card index: {i}, space index 0")

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.space.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, value):
        super().__init__()
        self.solitaire = solitaire
        self.controls = solitaire.controls
        self.suite = suite
        self.value = value
        self.face_up = False
        self.space = None

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
            content=ft.Text(f"{value} of {suite.name}", size=8, color=suite.color),
        )

    def reveal(self):
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
        print("start_drag:", e.control)
        cards_to_drag = self.cards_to_drag()
        self.move_on_top(self.controls, cards_to_drag)
        # remember card original position to return it back if needed
        self.solitaire.current_top = e.control.top
        self.solitaire.current_left = e.control.left
        # self.page.update()

    def drag(self, e: ft.DragUpdateEvent):
        i = 0
        # print(len(self.cards_to_drag()))
        print("drag:", e.control)
        for card in self.cards_to_drag():
            card.top = max(0, self.top + e.delta_y)
            if card.space.type == "tableau":
                card.top += i * self.solitaire.card_offset
            card.left = max(0, self.left + e.delta_x)
            i += 1
            card.update()

    def drop(self, e: ft.DragEndEvent):
        cards_to_drag = self.cards_to_drag()
        spaces = self.solitaire.tableau + self.solitaire.foundation
        # check if card is close to any of the tableau spaces
        for space in spaces:
            # compare with top and left position of the upper card in the space pile
            if (
                abs(self.top - space.upper_card_top()) < 20
                and abs(self.left - space.left) < 20
            ):
                # tableau slot
                # place cards_to_drag to the space in proximity, if
                # *** For tableau slots: if cards' color is different or space is empty
                # *** For foundation slots: [TBD]
                if (
                    space.type == "tableau"
                    and (
                        len(space.pile) == 0
                        or (
                            len(space.pile) != 0
                            and self.suite.color != space.pile[-1].suite.color
                        )
                    )
                ) or (
                    space.type == "foundation"
                    and len(cards_to_drag) == 1
                    and (
                        len(space.pile) == 0
                        or (
                            len(space.pile) != 0
                            and self.suite.color == space.pile[-1].suite.color
                        )
                    )
                ):

                    old_space = self.space
                    for card in cards_to_drag:
                        card.place(space)
                    # reveal top card in old space if exists
                    if len(old_space.pile) > 0:
                        old_space.pile[-1].reveal()
                    self.page.update()
                    return

        # return card to original position
        self.solitaire.bounce_back(cards_to_drag)
        self.page.update()

    def doubleclick(self, e):
        self.move_on_top(self.solitaire.controls, [self])
        self.place(self.solitaire.foundation[0])
        self.page.update()

    def place(self, space):
        self.top = space.top
        self.left = space.left
        if space.type == "tableau":
            self.top += self.solitaire.card_offset * len(space.pile)
        if space.type == "waste":
            self.left += self.solitaire.card_offset * len(space.pile)

        # remove the card form the old space's pile if exists
        if self.space is not None:
            self.space.pile.remove(self)

        # set card's space as new space
        self.space = space

        # add the card to the new space's pile
        space.pile.append(self)
        self.update()

    def cards_to_drag(self):
        """returns list of cards that will be dragged together, starting with current card"""
        top_pile = []

        if self.space is not None:
            card_index = self.space.pile.index(self)

            for card in self.space.pile:
                if self.space.pile.index(card) >= card_index:
                    top_pile.append(card)

        return top_pile


class Space(ft.Container):
    def __init__(self, solitaire, space_type, top, left, border):
        super().__init__()
        self.solitaire = solitaire
        self.pile = []
        self.type = space_type
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
