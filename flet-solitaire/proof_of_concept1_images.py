import flet as ft

# This prototype is to move card to a space and if close enough drop it there;
# if not return to original position

class GameData:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0

def main(page: ft.Page):
    def move_on_top(item, list):
        list.remove(item)
        list.append(item)

    def start_drag(e: ft.DragStartEvent):
        move_on_top(e.control, controls)
        game_data.start_top = e.control.top
        game_data.start_left = e.control.left
        page.update()

    def check_proximity(e: ft.DragEndEvent):
        if (
            abs(e.control.top - space.top) < 20
            and abs(e.control.left - space.left) < 20
        ):
            e.control.top = space.top
            e.control.left = space.left
        else:
            e.control.top = game_data.start_top
            e.control.left = game_data.start_left

        page.update()

    def move(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    space = ft.Container(
        width=50, height=50, left=200, top=200, border=ft.border.all(1)
    )

    card1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=move,
        on_pan_start=start_drag,
        on_pan_end=check_proximity,
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.colors.GREEN, width=50, height=50),
    )

    card2 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=move,
        on_pan_start=start_drag,
        on_pan_end=check_proximity,
        left=100,
        top=100,
        content=ft.Container(
            content=ft.Image(src=f"/images/Ace_spades.svg"),
        #visible=False,
        #margin=10,
        #padding=10,
        #alignment=ft.alignment.center,
        # bgcolor=ft.colors.GREEN_200,
            width=70,
            height=100,
            border_radius=10,
        #border=ft.border.all(3, ft.colors.BLACK),
    )
    )

    controls = [card1, card2, space]
    game_data = GameData()
    
    page.add(ft.Stack(controls, width=1000, height=500))


ft.app(target=main, assets_dir="images")
