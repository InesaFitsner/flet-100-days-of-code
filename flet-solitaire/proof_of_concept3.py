import flet as ft

# This prototype is to move card to any space with or without cards
# If there is card(s) and if close enough to the top card, drop it 20px lower
# if not close to any top card/space, return to original position


class Card:
    def __init__(self, control, space):
        self.control = control
        self.top = space.top
        self.left = space.left
        self.space = space


class Space:
    def __init__(self, space):
        self.space = space
        self.cards = []


def main(page: ft.Page):
    def move_on_top(item, list):
        """Brings draggable card to the top of the stack"""
        list.remove(item)
        list.append(item)
        # page.update()

    def find_close_space(item, spaces):
        """Returns closest top space or top card top and left; if no close spaces returns original top and left"""
        for space in spaces:
            if abs(item.top - space.top) < 20 and abs(item.left - space.left) < 20:
                item.space = None
                if space.data.cards == []:
                    space.data.cards.append(item)
                    return (space.top, space.left)
                else:
                    space.data.cards.append(item)
                    return (space.top + 20, space.left)

        return item.data.top, item.data.left

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, controls)
        page.update()

    def drop(e: ft.DragEndEvent):
        coordinates = find_close_space(e.control, spaces)
        e.control.top = coordinates[0]
        e.control.left = coordinates[1]
        e.control.data.top = e.control.top
        e.control.data.left = e.control.left
        page.update()

    def on_pan_update2(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    spaces = []

    # top spaces (final piles)
    x = 0
    for i in range(3):
        spaces.append(
            ft.Container(width=65, height=100, left=x, top=0, border=ft.border.all(1))
        )
        x += 100

    # bottom spaces (piles)
    y = 0
    for i in range(3):
        spaces.append(
            ft.Container(width=65, height=100, left=y, top=150, border=ft.border.all(1))
        )
        y += 100

    s = []
    for i in range(len(spaces)):
        space_object = Space(spaces[i])
        spaces[i].data = space_object
        s.append(space_object)

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=on_pan_update2,
        on_pan_start=start_drag,
        on_pan_end=drop,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=65, height=100),
    )

    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=on_pan_update2,
        on_pan_start=start_drag,
        on_pan_end=drop,
        content=ft.Container(bgcolor=ft.colors.AMBER, width=65, height=100),
    )

    # place card1 in spaces[4]
    c1 = Card(card1, spaces[4])
    card1.data = c1
    card1.top = c1.top
    card1.left = c1.left
    spaces[4].data.cards.append(c1)

    # place card2 in spaces[5]
    c2 = Card(card2, spaces[5])
    card2.data = c2
    card2.top = c2.top
    card2.left = c2.left
    spaces[5].data.cards.append(c2)

    cards = [card1, card2]
    controls = spaces + cards

    page.add(ft.Stack(controls, width=1000, height=500))


ft.app(target=main)
