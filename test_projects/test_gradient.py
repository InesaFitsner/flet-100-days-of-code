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


def generate_s(number_of_s):
    colors = []
    for i in range(0, number_of_s + 1):
        color = rgb2hex(colorsys.hsv_to_rgb(0.5, i / number_of_s, 1))
        colors.append(color)
    return colors


def generate_v(number_of_v):
    colors = []
    for i in range(0, number_of_v + 1):
        color = rgb2hex(colorsys.hsv_to_rgb(1, 0, (number_of_v - i) / number_of_v))
        colors.append(color)
    return colors


def main(page: ft.Page):
    c_h = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=generate_hues(10),
        ),
        width=150,
        height=30,
        border_radius=5,
    )

    c_s = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=generate_s(2),
        ),
        width=300,
        height=150,
        border_radius=5,
    )

    c_v = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#00ffffff", "#ff000000"],
        ),
        width=300,
        height=150,
        border_radius=5,
    )

    stack = ft.Stack(controls=[c_s, c_v])

    shader_mask_on_s = ft.ShaderMask(
        content=c_s,
        blend_mode=ft.BlendMode.MULTIPLY,
        shader=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.WHITE, ft.colors.BLACK],
            # stops=[0.5, 1.0],
        ),
        border_radius=10,
    )

    shader_mask_on_v = ft.ShaderMask(
        content=c_v,
        blend_mode=ft.BlendMode.SATURATION,
        shader=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=generate_s,
            stops=[0.5, 1.0],
        ),
        border_radius=10,
    )

    page.add(stack, shader_mask_on_s)


ft.app(target=main)
