import random

import flet as ft

# This prototype is move space and card creating and dealing to a class


class Solitaire:
    def __init__(self):
        self.current_top = 0
        self.current_left = 0
        self.offset = 20
        self.controls = []
        self.create_spaces()
        self.create_card_deck()
        self.deal_cards()

    def create_spaces(self):
        self.spaces = []

        # stock space index 0
        self.spaces.append(Space(solitaire=self, space_type="stock", top=0, left=0))

        # waste spaces index 1-3
        x = 100
        for i in range(3):
            self.spaces.append(Space(solitaire=self, space_type="waste", top=0, left=x))
            x += 20

        # top spaces (foundation piles) index 4-7
        x = 300
        for i in range(4):
            self.spaces.append(
                Space(solitaire=self, space_type="foundation", top=0, left=x)
            )
            x += 100

        # bottom spaces (plateau piles) index 8-14
        x = 0
        for i in range(7):
            self.spaces.append(
                Space(solitaire=self, space_type="tableau", top=150, left=x)
            )
            x += 100
        self.controls.extend(self.spaces)

    def create_card_deck(self):
        suites = ["Hearts", "Diamonds", "Clubs", "Spades"]
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
        self.controls.extend(self.cards)

    def deal_cards(self):
        i = 8
        for card in self.cards:
            if i > len(self.spaces) - 1:
                i = 8
            card.place(self.spaces[i])
            i += 1
        # card = random.choice(self.stock)
        # print(len(self.spaces))
        # print(len(self.cards))
        # i = 4
        # n = 0
        # while i < 11:
        #     for number in range(i, 11):
        #         card = random.choice(self.stock)
        #         print(self.stock.index(card))
        #         # self.cards[n].place(self.spaces[number])
        #         card.place(self.spaces[number])
        #         self.stock.remove(card)
        #         # n += 1
        #         # print(n)
        #     i += 1
        #     # self.stock.remove(card)

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.space.type == "tableau":
                card.top += i * self.offset
            card.left = self.current_left
            i += 1


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, value):
        super().__init__()
        self.solitaire = solitaire
        self.controls = solitaire.controls
        self.suite = suite
        self.value = value
        self.space = None

        self.mouse_cursor = ft.MouseCursor.MOVE
        # self.drag_interval = 10
        self.on_pan_update = self.drag
        self.on_pan_start = self.start_drag
        self.on_pan_end = self.drop
        self.on_double_tap = self.doubleclick
        self.content = ft.Container(
            width=65,
            height=100,
            border_radius=ft.border_radius.all(6),
            border=ft.border.all(2),
            bgcolor="WHITE",
            content=ft.Text(f"{value} of {suite}", size=8),
        )

    def move_on_top(self, controls, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            controls.remove(card)
            controls.append(card)
        self.page.update()

    def start_drag(self, e: ft.DragStartEvent):

        cards_to_drag = self.cards_to_drag()
        self.move_on_top(self.controls, cards_to_drag)
        # remember card original position to return it back if needed
        self.solitaire.current_top = e.control.top
        self.solitaire.current_left = e.control.left
        self.page.update()

    def drag(self, e: ft.DragUpdateEvent):
        i = 0
        for card in self.cards_to_drag():
            card.top = max(0, self.top + e.delta_y)
            if card.space.type == "tableau":
                card.top += i * self.solitaire.offset
            card.left = max(0, self.left + e.delta_x)
            i += 1
            card.update()

    def drop(self, e: ft.DragEndEvent):
        # check if card is close to any of the spaces
        cards_to_drag = self.cards_to_drag()
        for space in self.solitaire.spaces:
            # compare with top and left position of the upper card in the space pile
            if (
                abs(self.top - space.upper_card_top()) < 20
                and abs(self.left - space.left) < 20
            ):
                # place cards_to_drag to the space in proximity
                for card in cards_to_drag:
                    card.place(space)
                self.page.update()
                return

        # return card to original position
        self.solitaire.bounce_back(cards_to_drag)
        self.page.update()

    def doubleclick(self, e):
        self.move_on_top(self.solitaire.controls, [self])
        self.place(self.solitaire.spaces[0])
        self.page.update()

    def place(self, space):
        self.top = space.top
        if space.type == "tableau":
            self.top += self.solitaire.offset * len(space.pile)
        self.left = space.left

        # remove the card form the old space's pile if exists
        if self.space is not None:
            self.space.pile.remove(self)

        # set card's space as new space
        self.space = space

        # add the card to the new space's pile
        space.pile.append(self)

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
    def __init__(self, solitaire, space_type, top, left):
        super().__init__()
        self.solitaire = solitaire
        self.pile = []
        self.type = space_type
        self.width = 65
        self.height = 100
        self.left = left
        self.top = top
        self.border_radius = ft.border_radius.all(6)
        self.border = ft.border.all(1)

    def upper_card_top(self):
        if self.type == "tableau":
            if len(self.pile) > 1:
                return self.top + self.solitaire.offset * (len(self.pile) - 1)
        return self.top


def main(page: ft.Page):

    solitaire = Solitaire()

    page.add(ft.Stack(solitaire.controls, width=1000, height=500))


ft.app(target=main)
