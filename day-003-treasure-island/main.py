import flet as ft


def main(page: ft.Page):
    page.title = "Flet Treasure Island Story"
    # page.vertical_alignment = "center"

    def start_adventure(e):
        question1.visible = True
        left_button.visible = True
        right_button.visible = True
        welcome.visible = False
        directions.visible = False
        image.src = f"https://media.gettyimages.com/id/707544639/photo/t-intersection-sign-on-grassy-field-by-dirt-road-against-blue-sky.jpg?s=1024x1024&w=gi&k=20&c=uxrPO1TKBuOdCbbZ1q_eEXbym0LqBfHFhUiaMyw3eNA="

        start_adventure.visible = False
        page.update()

    def button_clicked(e):
        if e.data == "left":
            end_message.visible = True

        page.update()

    image = ft.Image(
        src=f"https://cdn.pixabay.com/photo/2015/02/01/17/06/treasure-chest-619868_1280.jpg",
        height=300,
        fit="fitWidth",
    )

    welcome = ft.Text(
        "Welcome to Treasure Island.",
        style="displayMedium",
    )
    directions = ft.Text("Your mission is to find the treasure.", style="titleMedium")
    start_adventure = ft.OutlinedButton(
        text="Start your adventure", on_click=start_adventure
    )

    left_button = ft.OutlinedButton(
        text="Left", on_click=button_clicked, data="left", visible=False
    )
    right_button = ft.OutlinedButton(
        text="Right", on_click=button_clicked, data="right", visible=False
    )
    question1 = ft.Text(
        "You came accross a T-intersection in a rural area. Where would you go, left or right?",
        style="titleMedium",
        visible=False,
    )
    end_message = ft.Text("You died.", visible=False)
    page.add(
        image,
        welcome,
        directions,
        start_adventure,
        question1,
        left_button,
        right_button,
        end_message,
    )


ft.app(target=main)
