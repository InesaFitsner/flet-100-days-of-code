import flet as ft

# This prototype is move space and card creating and dealing to a class


class GameController:
    def __init__(self):
        self.current_top = 0
        self.current_left = 0
        self.offset = 20
        self.space_layout()

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

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            if card.data.space.type == "tableau":
                card.top = self.current_top + i * self.offset
            elif card.data.space.type == "foundation":
                card.top = self.current_top
            card.left = self.current_left
            i += 1


class Card:
    def __init__(self, control):
        self.control = control
        self.space = None
        self.set_control_data()

    def set_control_data(self):
        self.control.data = self

    def place(self, space):
        if space.type == "tableau":
            self.control.top = space.top + 20 * len(space.pile)
        elif space.type == "foundation":
            self.control.top = space.top
        self.control.left = space.left

        # remove the card form the old space's pile if exists
        if self.space is not None:
            self.space.pile.remove(self.control)

        # set card's space as new space
        self.space = space

        # add the card to the new space's pile
        space.pile.append(self.control)

    def cards_to_drag(self):
        # number if cards in the space
        top_pile = []
        if self.space is not None:
            card_index = self.space.pile.index(self.control)

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
    def move_on_top(controls, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            controls.remove(card)
            controls.append(card)
        page.update()

    def start_drag(e: ft.DragStartEvent):

        cards_to_drag = e.control.data.cards_to_drag()
        move_on_top(controls, cards_to_drag)

        # remember card original position to return it back if needed
        solitaire.current_top = e.control.top
        solitaire.current_left = e.control.left
        page.update()

    def drag(e: ft.DragUpdateEvent):
        i = 0
        for card in e.control.data.cards_to_drag():
            if e.control.data.space.type == "tableau":
                card.top = max(0, e.control.top + e.delta_y) + i * solitaire.offset
            elif e.control.data.space.type == "foundation":
                card.top = max(0, e.control.top + e.delta_y)
            card.left = max(0, e.control.left + e.delta_x)
            i += 1
            card.update()

    def drop(e: ft.DragEndEvent):
        # check if card is close to any of the spaces
        cards_to_drag = e.control.data.cards_to_drag()
        for space in solitaire.spaces:
            # top position of the upper card in the pile
            if (
                abs(e.control.top - space.upper_card_top()) < 20
                and abs(e.control.left - space.left) < 20
            ):
                # place cards_to_drag to the space in proximity
                for card in cards_to_drag:
                    card.data.place(space)
                page.update()
                return

        # return card to original position
        solitaire.bounce_back(cards_to_drag)
        page.update()

    solitaire = GameController()

    colors = ["BLUE", "YELLOW", "GREEN", "RED"]

    card_controls = []
    cards = []

    for color in colors:

        card_controls.append(
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                drag_interval=10,
                on_pan_update=drag,
                on_pan_start=start_drag,
                on_pan_end=drop,
                content=ft.Container(width=65, height=100),
            )
        )
        card_controls[-1].content.bgcolor = color
        cards.append(Card(card_controls[-1]))

    for i in range(4):
        cards[i].place(solitaire.spaces[4 + i])

    controls = solitaire.spaces + card_controls

    page.add(ft.Stack(controls, width=1000, height=500))


ft.app(target=main)
