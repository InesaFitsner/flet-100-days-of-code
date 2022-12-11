import flet as ft

# This prototype is move space and card creating and dealing to a class


class GameData:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0
        self.offset = 20

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            if card.data.space.type == "tableau":
                card.top = self.start_top + i * self.offset
            elif card.data.space.type == "foundation":
                card.top = self.start_top
            card.left = self.start_left
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
            self.control.top = space.control.top + 20 * len(space.pile)
        elif space.type == "foundation":
            self.control.top = space.control.top
        self.control.left = space.control.left

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


class Space:
    def __init__(self, space, space_type):
        self.control = space
        self.pile = []
        self.type = space_type
        self.set_control_data()

    def set_control_data(self):
        self.control.data = self

    def upper_card_top(self):
        if self.type == "tableau":
            if len(self.pile) > 1:
                return self.control.top + 20 * (len(self.pile) - 1)
        return self.control.top


def main(page: ft.Page):
    def move_on_top(list, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            list.remove(card)
            list.append(card)
        page.update()

    def start_drag(e: ft.DragStartEvent):

        cards_to_drag = e.control.data.cards_to_drag()
        move_on_top(controls, cards_to_drag)

        # remember card original position to return it back if needed
        game_data.start_top = e.control.top
        game_data.start_left = e.control.left
        page.update()

    def drag(e: ft.DragUpdateEvent):
        i = 0
        for card in e.control.data.cards_to_drag():
            if e.control.data.space.type == "tableau":
                card.top = max(0, e.control.top + e.delta_y) + i * game_data.offset
            elif e.control.data.space.type == "foundation":
                card.top = max(0, e.control.top + e.delta_y)
            card.left = max(0, e.control.left + e.delta_x)
            i += 1
            card.update()

    def drop(e: ft.DragEndEvent):
        # check if card is close to any of the spaces
        cards_to_drag = e.control.data.cards_to_drag()
        for space in spaces:
            # top position of the upper card in the pile
            if (
                abs(e.control.top - space.upper_card_top()) < 20
                and abs(e.control.left - space.control.left) < 20
            ):
                # place cards_to_drag to the space in proximity
                for card in cards_to_drag:
                    card.data.place(space)
                page.update()
                return

        # return card to original position
        game_data.bounce_back(cards_to_drag)
        page.update()

    game_data = GameData()
    space_controls = []
    spaces = []

    # top spaces (foundation piles)
    x = 0
    for i in range(4):
        space_controls.append(
            ft.Container(width=65, height=100, left=x, top=0, border=ft.border.all(1))
        )
        spaces.append(Space(space_controls[-1], "foundation"))
        x += 100

    # bottom spaces (plateau piles)
    y = 0
    for i in range(4):
        space_controls.append(
            ft.Container(width=65, height=100, left=y, top=150, border=ft.border.all(1))
        )
        spaces.append(Space(space_controls[-1], "tableau"))
        y += 100

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
        cards[i].place(spaces[4 + i])

    controls = space_controls + card_controls

    page.add(ft.Stack(controls, width=1000, height=500))


ft.app(target=main)
