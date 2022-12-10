import flet as ft

# This prototype is to move card to any space with or without card
# If there is a card, drop it 20px lower


class GameData:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

    def place_card(self, card, space):
        card.top = space.top
        card.left = space.left

        # remove the card form the old space's pile if exists
        if card.data.space is not None:
            card.data.space.data.cards.remove(card)

        # set card's space as new space
        card.data.space = space

        # add the card to the new space's pile
        space.data.pile.append(card)

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


class Space:
    def __init__(self, space):
        self.space = space
        self.pile = []


def main(page: ft.Page):
    def move_on_top(item, list):
        """Brings draggable card to the top of the stack"""
        list.remove(item)
        list.append(item)
        page.update()

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, controls)
        # remember card original position to return it back if needed
        game_data.start_top = e.control.top
        game_data.start_left = e.control.left
        page.update()

    def drop(e: ft.DragEndEvent):
        # check if card is close to any of the spaces
        for space in spaces:
            if (
                abs(e.control.top - space.top) < 20
                and abs(e.control.left - space.left) < 20
            ):
                game_data.place_card(e.control, space)
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

    # top spaces (foundation piles)
    x = 0
    for i in range(4):
        spaces.append(
            ft.Container(width=65, height=100, left=x, top=0, border=ft.border.all(1))
        )
        x += 100

    # bottom spaces (plateau piles)
    y = 0
    for i in range(4):
        spaces.append(
            ft.Container(width=65, height=100, left=y, top=150, border=ft.border.all(1))
        )
        y += 100

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=move,
        on_pan_start=start_drag,
        on_pan_end=drop,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=65, height=100),
    )

    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=move,
        on_pan_start=start_drag,
        on_pan_end=drop,
        content=ft.Container(bgcolor=ft.colors.AMBER, width=65, height=100),
    )

    cards = [card1, card2]
    game_data = GameData()

    game_data.place_card(card1, spaces[4])
    game_data.place_card(card2, spaces[5])

    controls = spaces + cards

    page.add(ft.Stack(controls, width=1000, height=500))


ft.app(target=main)
