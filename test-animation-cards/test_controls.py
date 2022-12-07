import flet as ft


class GameData:
    """
    To store user_choice and computer_choice
    """

    pass


def main(page: ft.Page):

    page.horizontal_alignment = "start"
    page.vertical_alignment = "start"

    game_data = GameData()

    user_choice_text = ft.Text("Choose your weapon:", style="titleLarge")
    computer_choice_text = ft.Text("Computer choice:", style="titleLarge")

    def user_chose(e):
        """
        Will save control data as game_data.user_choice (0 for rock, 1 for paper, 2 for scissors) and show animation
        """
        print(f"user chose {e.control.data}")
        game_data.user_choice = int(e.control.data)

        c2.top = 50
        c2.left = 50
        c3.top = 50
        c3.left = 50
        page.update()

    c1 = ft.Container(
        content=ft.Image(src=f"/images/rock_user.png"),
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        # ink=True,
        data="0",
        width=150,
        height=150,
        bgcolor=ft.colors.WHITE,
        left=50,
        top=50,
        on_click=user_chose,
        animate_position=1000,
    )

    c2 = ft.Container(
        width=150,
        height=150,
        data="1",
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        left=300,
        top=50,
        on_click=user_chose,
        animate_position=1000,
        content=ft.Image(src=f"/images/paper_user.png"),
    )

    c3 = ft.Container(
        width=150,
        height=150,
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        left=550,
        top=50,
        animate_position=1000,
        data="2",
        on_click=user_chose,
        content=ft.Image(src=f"/images/scissors_user.png"),
    )

    page.add(
        ft.Row(
            width=800,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[user_choice_text, computer_choice_text],
        ),
        ft.Container(
            bgcolor=ft.colors.BLUE_GREY_100,
            width=800,
            height=250,
            content=ft.Stack(
                controls=[
                    c1,
                    c2,
                    c3,
                ],
            ),
        ),
    )


ft.app(target=main, assets_dir="images")
