import flet as ft


def main(page: ft.Page):
    page.title = "Flet Band Name Generator"
    # page.vertical_alignment = "center"
    def reset_textfields():
        city.error_text = ""
        pet.error_text = ""

    def button_clicked(e):
        reset_textfields()
        valid_form = True

        if city.value == "":
            city.error_text = "City cannot be blank."
            valid_form = False
        if pet.value == "":
            pet.error_text = "Pet name connot be blank."
            valid_form = False

        if valid_form:
            band_name.value = f"Your band name could be {city.value} {pet.value}."
        page.update()

    city = ft.TextField(label="Name of the city you grew up in")
    pet = ft.TextField(label="Name of your pet")
    band_name = ft.Text("Your band name could be [wait for it].")

    page.add(
        city,
        pet,
        ft.ElevatedButton(text="Generate your band name", on_click=button_clicked),
        band_name,
    )


ft.app(target=main)
