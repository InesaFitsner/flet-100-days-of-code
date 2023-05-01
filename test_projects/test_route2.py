import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))

    def route_change(e):
        page.add(ft.Text(f"New route: {e.route}"))
        print(len(page.views))

    def go_store(e):
        page.route = "/store"
        page.update()

    page.on_route_change = route_change
    page.add(ft.ElevatedButton("Go to Store", on_click=go_store))
    print(len(page.views))

ft.app(target=main, view=ft.WEB_BROWSER)