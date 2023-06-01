import flet as ft
import colorsys


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0)
    )


def generate_hues(number_of_hues):
    colors = []
    for i in range(0, number_of_hues + 1):
        color = rgb2hex(colorsys.hsv_to_rgb(i / number_of_hues, 1, 1))
        colors.append(color)
    return colors


def main(page: ft.Page):
    c = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=generate_hues(10),
        ),
        width=150,
        height=30,
        border_radius=5,
    )

    page.add(c)


ft.app(target=main)
