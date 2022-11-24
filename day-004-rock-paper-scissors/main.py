import flet as ft


def main(page: ft.Page):
    page.title = "Rock, Paper, Scissors"
    # page.vertical_alignment = "center"

    def user_chose(e):
        print(e.control.data)
        page.update()

    def start_over(e):

        page.update()

    directions = ft.Text("Choose your weapon:", style="titleLarge")

    rock = ft.Container(
        content=ft.Image(src=f"/images/rock_user.png"),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="rock",
        on_click=user_chose,
    )
    paper = ft.Container(
        content=ft.Image(src=f"/images/paper_user.png"),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="paper",
        on_click=user_chose,
    )
    scissors = ft.Container(
        content=ft.Image(src=f"/images/scissors_user.png"),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        # bgcolor=ft.colors.GREEN_200,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="scissors",
        on_click=user_chose,
    )

    choices = ft.Row(controls=[rock, paper, scissors])

    end_message = ft.Text("", visible=False)
    start_over_button = ft.OutlinedButton(
        text="Start over", on_click=start_over, visible=False
    )
    page.add(directions, choices, end_message, start_over_button)


ft.app(target=main, assets_dir="images")
