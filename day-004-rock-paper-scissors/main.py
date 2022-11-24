import random
from time import sleep

import flet as ft


def main(page: ft.Page):
    page.title = "Rock, Paper, Scissors"
    # page.vertical_alignment = "center"

    def user_chose(e):
        e.control.border = ft.border.all(10, ft.colors.BLACK)
        user_choice_index = int(e.control.data)
        print(f"User choice is {user_choice_index}")
        computer_choice_text.visible = True
        computer_choice_index = 0
        for i in range(0, 10):
            # pr.value = i * 0.1
            # choice = random.randint(0, 2)
            computer_choices.controls[computer_choice_index].visible = True
            page.update()
            sleep(0.5)
            computer_choices.controls[computer_choice_index].visible = False
            if computer_choice_index < 2:
                computer_choice_index += 1
            else:
                computer_choice_index = 0
            page.update()

        computer_choice_index = random.randint(0, 2)
        print(f"Computer choice is {computer_choice_index}")
        computer_choice_text.value = "The computer has chosen:"
        computer_choices.controls[computer_choice_index].border = ft.border.all(
            10, ft.colors.BLACK
        )
        computer_choices.controls[computer_choice_index].visible = True

        page.update()

    def start_over(e):

        page.update()

    directions = ft.Text("Choose your weapon:", style="titleLarge")

    rock_user = ft.Container(
        content=ft.Image(src=f"/images/rock_user.png"),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="0",
        on_click=user_chose,
    )
    paper_user = ft.Container(
        content=ft.Image(src=f"/images/paper_user.png"),
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="1",
        on_click=user_chose,
    )
    scissors_user = ft.Container(
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
        data="2",
        on_click=user_chose,
    )

    rock_computer = ft.Container(
        content=ft.Image(src=f"/images/rock_computer.png"),
        margin=10,
        padding=10,
        visible=False,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="0",
        on_click=user_chose,
    )
    paper_computer = ft.Container(
        content=ft.Image(src=f"/images/paper_computer.png"),
        visible=False,
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="1",
        on_click=user_chose,
    )
    scissors_computer = ft.Container(
        content=ft.Image(src=f"/images/scissors_computer.png"),
        visible=False,
        margin=10,
        padding=10,
        alignment=ft.alignment.center,
        # bgcolor=ft.colors.GREEN_200,
        width=150,
        height=150,
        border_radius=10,
        border=ft.border.all(3, ft.colors.BLACK),
        ink=True,
        data="2",
        on_click=user_chose,
    )

    user_choices = ft.Row(controls=[rock_user, paper_user, scissors_user])

    computer_choices = ft.Stack(
        controls=[rock_computer, paper_computer, scissors_computer]
    )

    computer_choice_text = ft.Text(
        visible=False, value="Wait for the computer to choose...", style="titleLarge"
    )

    end_message = ft.Text("", visible=False)
    start_over_button = ft.OutlinedButton(
        text="Start over", on_click=start_over, visible=False
    )
    page.add(
        directions,
        user_choices,
        computer_choice_text,
        computer_choices,
        end_message,
        start_over_button,
    )


ft.app(target=main, assets_dir="images")
