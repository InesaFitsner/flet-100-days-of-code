import flet as ft

# This prototype is to move card that is not upper card. The card shouldn't be moved on top,
# and the rest of the pile should move together with it
# if not close to any space the pile should bounce back
# if close, all the cards in pile should be placed to this space


class GameData:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0
        self.offset = 20

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.start_top + i * self.offset
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

        self.control.top = space.control.top + 20 * len(space.pile)
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
    def __init__(self, space):
        self.control = space
        self.pile = []
        self.set_control_data()

    def set_control_data(self):
        self.control.data = self

    def upper_card_top(self):
        return self.control.top + 20 * len(self.pile)


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
            card.top = max(0, e.control.top + e.delta_y) + i * game_data.offset
            card.left = max(0, e.control.left + e.delta_x)
            i += 1
            card.update()

    def drop(e: ft.DragEndEvent):
        # check if card is close to any of the spaces
        cards_to_drag = e.control.data.cards_to_drag()
        for space in spaces:
            # top position of the upper card in the pile
            new_top = space.upper_card_top()
            if (
                abs(e.control.top - new_top) < 20
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
        spaces.append(Space(space_controls[-1]))
        x += 100

    # bottom spaces (plateau piles)
    y = 0
    for i in range(4):
        space_controls.append(
            ft.Container(width=65, height=100, left=y, top=150, border=ft.border.all(1))
        )
        spaces.append(Space(space_controls[-1]))
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
