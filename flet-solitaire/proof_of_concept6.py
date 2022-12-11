import flet as ft

# This prototype is move space and card creating and dealing to a class


class GameController:
    def __init__(self, controls):
        self.current_top = 0
        self.current_left = 0
        self.offset = 20
        self.space_layout()
        self.card_deck(controls=controls)

    def space_layout(self):
        self.spaces = []

        # top spaces (foundation piles)
        x = 0
        for i in range(4):
            self.spaces.append(Space(space_type="foundation", top=0, left=x))
            x += 100

        # bottom spaces (plateau piles)
        x = 0
        for i in range(4):
            self.spaces.append(Space(space_type="tableau", top=150, left=x))
            x += 100

    def card_deck(self, controls):
        colors = ["BLUE", "YELLOW", "GREEN", "RED"]

        self.cards = []
        # controls = []

        for color in colors:
            self.cards.append(Card(solitaire=self, controls=controls, bgcolor=color))

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            if card.space.type == "tableau":
                card.top = self.current_top + i * self.offset
            elif card.space.type == "foundation":
                card.top = self.current_top
            card.left = self.current_left
            i += 1


class Card(ft.GestureDetector):
    def __init__(self, solitaire, controls, bgcolor):
        super().__init__()
        self.solitaire = solitaire
        self.controls = controls
        self.space = None

        self.mouse_cursor = ft.MouseCursor.MOVE
        # self.drag_interval = 10
        self.on_pan_update = self.drag
        self.on_pan_start = self.start_drag
        self.on_pan_end = self.drop
        self.content = ft.Container(width=65, height=100, bgcolor=bgcolor)

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
            if self.space.type == "tableau":
                card.top = max(0, self.top + e.delta_y) + i * self.solitaire.offset
            elif self.space.type == "foundation":
                card.top = max(0, self.top + e.delta_y)
            card.left = max(0, self.left + e.delta_x)
            i += 1
            card.update()

    def drop(self, e: ft.DragEndEvent):
        # check if card is close to any of the spaces
        cards_to_drag = self.cards_to_drag()
        for space in self.solitaire.spaces:
            # top position of the upper card in the pile
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

    def place(self, space):
        if space.type == "tableau":
            self.top = space.top + 20 * len(space.pile)
        elif space.type == "foundation":
            self.top = space.top
        self.left = space.left

        # remove the card form the old space's pile if exists
        if self.space is not None:
            self.space.pile.remove(self)

        # set card's space as new space
        self.space = space

        # add the card to the new space's pile
        space.pile.append(self)

    def cards_to_drag(self):
        # number if cards in the space
        top_pile = []
        if self.space is not None:
            card_index = self.space.pile.index(self)

            for card in self.space.pile:
                if self.space.pile.index(card) >= card_index:
                    top_pile.append(card)

        return top_pile


class Space(ft.Container):
    def __init__(self, space_type, top, left):
        super().__init__()
        self.pile = []
        self.type = space_type
        self.width = 65
        self.height = 100
        self.left = left
        self.top = top
        self.border = ft.border.all(1)

    def upper_card_top(self):
        if self.type == "tableau":
            if len(self.pile) > 1:
                return self.top + 20 * (len(self.pile) - 1)
        return self.top


def main(page: ft.Page):
    controls = []
    solitaire = GameController(controls)

    # colors = ["BLUE", "YELLOW", "GREEN", "RED"]

    # cards = []

    # for color in colors:
    #     cards.append(Card(solitaire=solitaire, controls=controls, bgcolor=color))

    for i in range(4):
        solitaire.cards[i].place(solitaire.spaces[4 + i])

    controls.extend(solitaire.spaces)
    controls.extend(solitaire.cards)

    page.add(ft.Stack(controls, width=1000, height=500))


ft.app(target=main)
