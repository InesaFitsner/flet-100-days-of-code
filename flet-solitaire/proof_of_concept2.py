import flet as ft

# This prototype is to move card to any space or card and if close enough drop it there;
# For spaces, drop on the space. For cards, place it some 20-40px lower
# Once card is dropped to a new place, change top and left for Card object (make it original position)
# if not close to any card/space, return to original position


class Card:
    def __init__(self, control, space):
        self.control = control
        self.top = space.top
        self.left = space.left


class Space:
    def __init__(self, space):
        self.space = space


def main(page: ft.Page):
    def move_on_top(item, list):
        """Brings draggable card to the top of the stack"""
        list.remove(item)
        list.append(item)

    def find_close_space(item, spaces):
        """Returns closest space's top and left; if no close spaces returns original top and left"""
        coordinates = (item.data.top, item.data.left)
        for space in spaces:
            if abs(item.top - space.top) < 20 and abs(item.left - space.left) < 20:
                return (space.top, space.left)

        return coordinates

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, cards)
        page.update()

    def check_proximity(e: ft.DragEndEvent):

        e.control.top = find_close_space(e.control, spaces)[0]
        e.control.left = find_close_space(e.control, spaces)[1]
        e.control.data.top = e.control.top
        e.control.data.left = e.control.left
        page.update()

    def on_pan_update2(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    # top spaces (final piles)
    space1 = ft.Container(width=65, height=100, left=0, top=0, border=ft.border.all(1))

    space2 = ft.Container(
        width=65, height=100, left=100, top=0, border=ft.border.all(1)
    )

    space3 = ft.Container(
        width=65, height=100, left=200, top=0, border=ft.border.all(1)
    )
    # bottom spaces (piles)
    space4 = ft.Container(
        width=65, height=100, left=0, top=150, border=ft.border.all(1)
    )

    space5 = ft.Container(
        width=65, height=100, left=100, top=150, border=ft.border.all(1)
    )

    space6 = ft.Container(
        width=65, height=100, left=200, top=150, border=ft.border.all(1)
    )

    s1 = Space(space1)
    s2 = Space(space2)
    s3 = Space(space3)
    s4 = Space(space4)
    s5 = Space(space5)
    s6 = Space(space6)
    space1.data = s1
    space2.data = s2
    space3.data = s3
    space4.data = s4
    space5.data = s5
    space6.data = s6

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=on_pan_update2,
        on_pan_start=start_drag,
        on_pan_end=check_proximity,
        # left=0,
        # top=0,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=65, height=100),
    )

    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=on_pan_update2,
        on_pan_start=start_drag,
        on_pan_end=check_proximity,
        # left=100,
        # top=100,
        content=ft.Container(bgcolor=ft.colors.AMBER, width=65, height=100),
    )
    c1 = Card(card1, space4)
    card1.data = c1
    card1.top = c1.top
    card1.left = c1.left

    c2 = Card(card2, space5)
    card2.data = c2
    card2.top = c2.top
    card2.left = c2.left

    spaces = [space1, space2, space3, space4, space5, space6]
    cards = [card1, card2]

    # page.add(ft.Stack(cards, width=1000, height=500))
    page.add(ft.Stack(spaces + cards, width=1000, height=500))


ft.app(target=main)
