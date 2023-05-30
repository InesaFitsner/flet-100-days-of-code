import flet as ft


def main(page: ft.Page):
    def dropdown_changed(e):
        dd.value = ""
        dd.update()

    dd = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
        ],
        on_change=dropdown_changed,
    )
    page.add(dd)


ft.app(target=main)
