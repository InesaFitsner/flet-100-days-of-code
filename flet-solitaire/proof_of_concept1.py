import flet as ft

# This prototype is to move card to a space and if close enough drop it there;
# if not return to original position


class Card:
    def __init__(self, control):
        self.control = control
        self.top = control.top
        self.left = control.left


def main(page: ft.Page):
    def move_on_top(item, list):
        list.remove(item)
        list.append(item)

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, cards)
        page.update()

    def check_proximity(e: ft.DragEndEvent):
        if (
            abs(e.control.top - space.top) < 20
            and abs(e.control.left - space.left) < 20
        ):
            e.control.top = space.top
            e.control.left = space.left
        else:
            e.control.top = e.control.data.top
            e.control.left = e.control.data.left

        page.update()

    def on_pan_update2(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    space = ft.Container(
        width=50, height=50, left=200, top=200, border=ft.border.all(5)
    )

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=on_pan_update2,
        on_pan_start=start_drag,
        on_pan_end=check_proximity,
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=50, height=50),
    )
    c1 = Card(card1)
    card1.data = c1

    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=on_pan_update2,
        on_pan_start=start_drag,
        on_pan_end=check_proximity,
        left=100,
        top=100,
        content=ft.Container(bgcolor=ft.colors.AMBER, width=50, height=50),
    )

    c2 = Card(card2)
    card2.data = c2

    cards = [card1, card2, space]

    page.add(ft.Stack(cards, width=1000, height=500))


ft.app(target=main)
