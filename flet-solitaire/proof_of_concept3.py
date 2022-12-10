import flet as ft

# This prototype is to move card to any space with or without card
# If there is a card, drop it 20px lower


class GameData:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

    def bounce_back(self, card):
        card.top = self.start_top
        card.left = self.start_left


class Card:
    def __init__(self, control):
        self.control = control
        self.space = None
        self.set_control_data()

    def set_control_data(self):
        self.control.data = self

    def place_card(self, space):

        self.control.top = space.top + 20 * len(space.data.pile)
        self.control.left = space.left

        # remove the card form the old space's pile if exists
        if self.space is not None:
            self.space.data.pile.remove(self.control)

        # set card's space as new space
        self.space = space

        # add the card to the new space's pile
        space.data.pile.append(self.control)


class Space:
    def __init__(self, space):
        self.space = space
        self.pile = []
        self.set_control_data()

    def set_control_data(self):
        self.space.data = self

    def upper_card_top(self):
        return self.space.top + 20 * len(self.pile)


def main(page: ft.Page):
    def move_on_top(item, list):
        """Brings draggable card to the top of the stack"""
        list.remove(item)
        list.append(item)
        page.update()

    def start_drag(e: ft.DragStartEvent):
        print(e.control.data.space.data.pile.index(e.control))
        move_on_top(e.control, controls)
        # remember card original position to return it back if needed
        game_data.start_top = e.control.top
        game_data.start_left = e.control.left
        page.update()

    def drop(e: ft.DragEndEvent):
        # check if card is close to any of the spaces
        for space in spaces:
            new_top = space.data.upper_card_top()
            if (
                abs(e.control.top - new_top) < 20
                and abs(e.control.left - space.left) < 20
            ):

                e.control.data.place_card(space)
                page.update()
                return

        # return card to original position
        game_data.bounce_back(e.control)
        page.update()

    def move(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    spaces = []
    space_objects = []

    # top spaces (foundation piles)
    x = 0
    for i in range(4):
        spaces.append(
            ft.Container(width=65, height=100, left=x, top=0, border=ft.border.all(1))
        )
        space_objects.append(Space(spaces[-1]))
        x += 100

    # bottom spaces (plateau piles)
    y = 0
    for i in range(4):
        spaces.append(
            ft.Container(width=65, height=100, left=y, top=150, border=ft.border.all(1))
        )
        space_objects.append(Space(spaces[-1]))
        y += 100

    colors = ["BLUE", "YELLOW", "GREEN", "RED"]

    cards = []
    card_objects = []

    for color in colors:

        cards.append(
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                drag_interval=10,
                on_pan_update=move,
                on_pan_start=start_drag,
                on_pan_end=drop,
                content=ft.Container(width=65, height=100),
            )
        )
        cards[-1].content.bgcolor = color
        card_objects.append(Card(cards[-1]))

    game_data = GameData()

    for i in range(4):
        card_objects[i].place_card(spaces[4 + i])

    controls = spaces + cards

    page.add(ft.Stack(controls, width=1000, height=500))


ft.app(target=main)
