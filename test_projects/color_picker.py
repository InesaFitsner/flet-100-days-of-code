import flet as ft
import colorsys

WIDTH = 35
HEIGHT = 20
SQUARE_SIZE = 8
CIRCLE_SIZE = SQUARE_SIZE * 2


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0)
    )


def hex2rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


class HueSlider(ft.Container):
    def __init__(self, on_change_hue):
        super().__init__()
        self.height = SQUARE_SIZE
        self.width = SQUARE_SIZE * WIDTH / 2
        self.border_radius = 5
        self.content = ft.Stack(controls=[ft.Container(bgcolor="green")])
        self.generate_hues()
        self.on_change_hue = on_change_hue

    def generate_hues(self):
        def pick_hue(e):
            rgb_color = hex2rgb(e.control.bgcolor)
            hsv_color = colorsys.rgb_to_hsv(
                round(rgb_color[0] / 255, 1),
                round(rgb_color[1] / 255, 1),
                round(rgb_color[2] / 255, 1),
            )
            self.on_change_hue(hsv_color[0])

        for i in range(0, WIDTH):
            # color = rgb2hex(colorsys.hsv_to_rgb(i/WIDTH,  1, 1 * (HEIGHT - j + 1) / HEIGHT))
            color = rgb2hex(colorsys.hsv_to_rgb(i * 2 / WIDTH, 1, 1))
            # c color = rgb2hex(colorsys.hls_to_rgb(i / WIDTH, 1, 1))
            self.content.controls.append(
                ft.Container(
                    height=SQUARE_SIZE,
                    width=SQUARE_SIZE,
                    bgcolor=color,
                    on_click=pick_hue,
                    top=0,
                    left=i * SQUARE_SIZE,
                )
            )


class CustomColorPicker(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.color = "#0a0a0a"
        self.content = ft.Column()

        self.hue_slider = HueSlider(on_change_hue=self.update_color_matrix)
        self.generate_color_matrix(hue=0)
        self.generate_selected_color(color=self.color)
        self.on_dismiss = lambda e: print("Dialog dismissed!")

    def generate_selected_color(self, color):
        self.selected_color = ft.Container(
            padding=CIRCLE_SIZE / 2,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(width=20, height=20, border_radius=20, bgcolor=color),
                    ft.Text(color),
                    self.hue_slider,
                ],
            ),
        )
        self.content.controls.append(self.selected_color)

    def update_selected_color(self, color):
        self.selected_color.content.controls[0].bgcolor = color
        self.selected_color.content.controls[1].value = color
        self.selected_color.update()

    def update_color_matrix(self, hue):
        n = 0
        for j in range(0, HEIGHT):
            for i in range(0, WIDTH):
                color = rgb2hex(
                    colorsys.hsv_to_rgb(hue, (i) / WIDTH, 1 * (HEIGHT - j) / HEIGHT)
                )
                self.content.controls[0].controls[n].bgcolor = color
                n += 1
        # print(self.content.controls[0][1].bgcolor)
        self.content.update()

    def generate_color_matrix(self, hue):
        color_matrix = ft.Stack(
            height=HEIGHT * SQUARE_SIZE + CIRCLE_SIZE,
            width=WIDTH * SQUARE_SIZE + CIRCLE_SIZE,
        )
        self.content.controls = []

        def pick_color(e):
            circle.top = e.control.top + SQUARE_SIZE / 2 - CIRCLE_SIZE / 2
            circle.left = e.control.left + SQUARE_SIZE / 2 - CIRCLE_SIZE / 2
            circle.content.bgcolor = e.control.bgcolor
            circle.update()
            self.color = e.control.bgcolor
            self.update_selected_color(self.color)

        for j in range(0, HEIGHT):
            for i in range(0, WIDTH):
                # color = rgb2hex(colorsys.hsv_to_rgb(i/WIDTH,  1, 1 * (HEIGHT - j + 1) / HEIGHT))
                color = rgb2hex(
                    colorsys.hsv_to_rgb(hue, (i) / WIDTH, 1 * (HEIGHT - j) / HEIGHT)
                )
                color_matrix.controls.append(
                    ft.Container(
                        height=SQUARE_SIZE,
                        width=SQUARE_SIZE,
                        bgcolor=color,
                        on_click=pick_color,
                        top=j * SQUARE_SIZE + CIRCLE_SIZE / 2,
                        left=i * SQUARE_SIZE + CIRCLE_SIZE / 2,
                    )
                )

        def find_color(x, y):
            for color_square in color_matrix.controls[
                :-1
            ]:  # excluding the last element of the controls list which is the circle
                if (
                    x >= color_square.top
                    and x <= color_square.top + SQUARE_SIZE
                    and y >= color_square.left
                    and y <= color_square.left + SQUARE_SIZE
                ):
                    return color_square.bgcolor
            return "blue"

        def on_pan_end(e: ft.DragEndEvent):
            e.control.content.bgcolor = find_color(
                x=e.control.top + CIRCLE_SIZE / 2, y=e.control.left + CIRCLE_SIZE / 2
            )
            e.control.update()
            self.color = e.control.content.bgcolor
            self.update_selected_color(self.color)

        def on_pan_update(e: ft.DragUpdateEvent):
            if e.control.top + e.delta_y < color_matrix.height - CIRCLE_SIZE:
                e.control.top = max(0, e.control.top + e.delta_y)
            if e.control.left + e.delta_x < color_matrix.width - CIRCLE_SIZE:
                e.control.left = max(0, e.control.left + e.delta_x)

            e.control.content.bgcolor = find_color(
                x=e.control.top + CIRCLE_SIZE / 2, y=e.control.left + CIRCLE_SIZE / 2
            )
            e.control.update()
            self.color = e.control.content.bgcolor
            self.update_selected_color(self.color)

        circle = ft.GestureDetector(
            top=HEIGHT * SQUARE_SIZE,
            left=0,
            on_pan_update=on_pan_update,
            on_pan_end=on_pan_end,
            content=ft.Container(
                width=CIRCLE_SIZE,
                height=CIRCLE_SIZE,
                bgcolor="#0a0a0a",
                border_radius=SQUARE_SIZE * 5,
                border=ft.border.all(width=2, color="white"),
            ),
        )

        color_matrix.controls.append(circle)
        self.content.controls.append(color_matrix)


def main(page: ft.Page):
    color_picker = CustomColorPicker()
    page.dialog = color_picker

    def open_color_picker(e):
        color_picker.open = True
        page.update()

    page.add(ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker))


ft.app(target=main)
