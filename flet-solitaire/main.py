import flet as ft

def main(page: ft.Page):
    def on_pan_update1(e: ft.DragUpdateEvent):
        c.top = max(0, c.top + e.delta_y)
        c.left = max(0, c.left + e.delta_x)
        #print(f"ctop1 {c.top} cleft1 {c.left}")
        # if c.top > 100:
        #     print ("Too low")
        c.update()
    
    def check_top(e: ft.DragEndEvent):
        if c.top > c3.top:
            print ("Too low")
        c.update()

    def on_pan_update2(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    gd = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=50,
        on_pan_update=on_pan_update1,
        on_pan_end=check_top
    )

    c = ft.Container(gd, bgcolor=ft.colors.AMBER, width=50, height=50, left=0, top=0)

    c3 = ft.Container(bgcolor=ft.colors.BLACK, width=50, height=50, left=200, top=200)

    gd1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_pan_update=on_pan_update2,
        left=100,
        top=100,
        content=ft.Container(bgcolor=ft.colors.BLUE, width=50, height=50),
    )

    page.add( ft.Stack([c, gd1, c3], width=1000, height=500))

ft.app(target=main)
