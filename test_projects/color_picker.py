import flet as ft
import colorsys

COLOR_MATRIX_WIDTH = 280
COLOR_MATRIX_HEIGHT = 160
COLOR_BLOCK_SIDE = 8

SLIDER_WIDTH = 180
NUMBER_OF_HUES = 100

CIRCLE_SIZE = 16


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0)
    )


def hex2rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


# class HueSlider(ft.Container):
class HueSlider(ft.Stack):
    def __init__(self, on_change_hue):
        super().__init__()
        self.height = CIRCLE_SIZE
        self.width = SLIDER_WIDTH
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

        hue_width = (self.width - CIRCLE_SIZE) / NUMBER_OF_HUES
        for i in range(0, NUMBER_OF_HUES):
            color = rgb2hex(colorsys.hsv_to_rgb(i / NUMBER_OF_HUES, 1, 1))
            self.controls.append(
                ft.Container(
                    height=CIRCLE_SIZE / 2,
                    width=hue_width,
                    bgcolor=color,
                    on_click=pick_hue,
                    top=(CIRCLE_SIZE) / 4,
                    left=i * hue_width + CIRCLE_SIZE / 2,
                )
            )

        def on_pan_update(e: ft.DragUpdateEvent):
            if e.control.left + e.delta_x < self.width - CIRCLE_SIZE:
                e.control.left = max(0, e.control.left + e.delta_x)
            e.control.update()

        circle = ft.GestureDetector(
            top=0,
            left=0,
            on_pan_update=on_pan_update,
            # on_pan_end=on_pan_end,
            content=ft.Container(
                width=CIRCLE_SIZE,
                height=CIRCLE_SIZE,
                bgcolor="#000000",
                border_radius=CIRCLE_SIZE,
                border=ft.border.all(width=2, color="white"),
            ),
        )

        self.controls.append(circle)


class CustomColorPicker(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.color = "#000000"
        self.content = ft.Column()
        self.hue_slider = HueSlider(on_change_hue=self.update_color_matrix)
        self.generate_color_matrix(hue=0)
        self.generate_selected_color_view(color=self.color)
        self.on_dismiss = lambda e: print("Dialog dismissed!")

    def find_color(self, x, y):
        for color_square in self.color_matrix.controls[
            :-1
        ]:  # excluding the last element of the controls list which is the circle
            if (
                x >= color_square.top
                and x <= color_square.top + self.square_side
                and y >= color_square.left
                and y <= color_square.left + self.square_side
            ):
                return color_square.bgcolor
        return "blue"

    def generate_selected_color_view(self, color):
        rgb = hex2rgb(color)

        self.selected_color_view = ft.Container(
            # padding=CIRCLE_SIZE / 2,
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Container(
                                width=30, height=30, border_radius=30, bgcolor=color
                            ),
                            # ft.Text(color),
                            self.hue_slider,
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.TextField(
                                label="Hex",
                                text_size=12,
                                value=color,
                                height=40,
                                width=90,
                            ),
                            ft.TextField(
                                label="R",
                                height=40,
                                width=55,
                                value=rgb[0],
                                text_size=12,
                            ),
                            ft.TextField(
                                label="G",
                                height=40,
                                width=55,
                                value=rgb[1],
                                text_size=12,
                            ),
                            ft.TextField(
                                label="B",
                                height=40,
                                width=55,
                                value=rgb[2],
                                text_size=12,
                            ),
                        ],
                    ),
                ],
            ),
        )
        self.content.controls.append(self.selected_color_view)

    def update_selected_color_view(self, color):
        rgb = hex2rgb(color)
        self.selected_color_view.content.controls[0].controls[
            0
        ].bgcolor = color  # Colored circle
        self.selected_color_view.content.controls[1].controls[0].value = color  # Hex
        self.selected_color_view.content.controls[1].controls[1].value = rgb[0]  # R
        self.selected_color_view.content.controls[1].controls[2].value = rgb[1]  # G
        self.selected_color_view.content.controls[1].controls[3].value = rgb[2]  # B
        self.color_matrix.controls[-1].content.bgcolor = color  # Color matrix circle
        self.update()

    def generate_color_matrix(self, hue):
        self.square_side = COLOR_BLOCK_SIDE
        self.colors_x = int(COLOR_MATRIX_WIDTH / self.square_side)
        self.colors_y = int(COLOR_MATRIX_HEIGHT / self.square_side)
        self.color_matrix = ft.Stack(
            # height=COLOR_MATRIX_HEIGHT + CIRCLE_SIZE,
            # width=COLOR_MATRIX_WIDTH + CIRCLE_SIZE,
            height=(self.colors_y + 1) * COLOR_BLOCK_SIDE + CIRCLE_SIZE,
            width=(self.colors_x + 1) * COLOR_BLOCK_SIDE + CIRCLE_SIZE,
        )
        self.content.controls = []

        def pick_color(e):
            # circle.top = e.control.top + self.square_side / 2 - CIRCLE_SIZE / 2
            # circle.left = e.control.left + self.square_side / 2 - CIRCLE_SIZE / 2
            circle.top = e.control.top + self.square_side / 2 - CIRCLE_SIZE / 2
            circle.left = e.control.left + self.square_side / 2 - CIRCLE_SIZE / 2
            circle.update()
            self.color = e.control.bgcolor
            self.update_selected_color_view(self.color)

        for j in range(0, self.colors_y + 1):
            for i in range(0, self.colors_x + 1):
                color = rgb2hex(
                    colorsys.hsv_to_rgb(
                        hue,
                        (i) / self.colors_x,
                        1 * (self.colors_y - j) / self.colors_y,
                    )
                )
                self.color_matrix.controls.append(
                    ft.Container(
                        height=self.square_side,
                        width=self.square_side,
                        bgcolor=color,
                        on_click=pick_color,
                        top=j * self.square_side + CIRCLE_SIZE / 2,
                        left=i * self.square_side + CIRCLE_SIZE / 2,
                    )
                )
                print(
                    self.color_matrix.controls[-1].top,
                    self.color_matrix.controls[-1].left,
                )

        def on_pan_end(e: ft.DragEndEvent):
            self.color = self.find_color(
                x=e.control.top + CIRCLE_SIZE / 2, y=e.control.left + CIRCLE_SIZE / 2
            )
            self.update_selected_color_view(self.color)

        def on_pan_update(e: ft.DragUpdateEvent):
            if e.control.top + e.delta_y < self.color_matrix.height - CIRCLE_SIZE:
                e.control.top = max(0, e.control.top + e.delta_y)
            if e.control.left + e.delta_x < self.color_matrix.width - CIRCLE_SIZE:
                e.control.left = max(0, e.control.left + e.delta_x)

            e.control.update()
            self.color = self.find_color(
                x=e.control.top + CIRCLE_SIZE / 2, y=e.control.left + CIRCLE_SIZE / 2
            )
            self.update_selected_color_view(self.color)

        circle = ft.GestureDetector(
            top=(self.colors_y + 1) * self.square_side,
            left=0,
            on_pan_update=on_pan_update,
            on_pan_end=on_pan_end,
            content=ft.Container(
                width=CIRCLE_SIZE,
                height=CIRCLE_SIZE,
                bgcolor=self.color,
                border_radius=CIRCLE_SIZE,
                border=ft.border.all(width=2, color="white"),
            ),
        )

        self.color_matrix.controls.append(circle)
        self.content.controls.append(self.color_matrix)

    def update_color_matrix(self, hue):
        n = 0
        for j in range(0, self.colors_y + 1):
            for i in range(0, self.colors_x + 1):
                color = rgb2hex(
                    colorsys.hsv_to_rgb(
                        hue,
                        (i) / self.colors_x,
                        1 * (self.colors_y - j) / self.colors_y,
                    )
                )
                self.content.controls[0].controls[n].bgcolor = color
                n += 1
        self.color = self.find_color(
            x=self.color_matrix.controls[-1].top + CIRCLE_SIZE / 2,
            y=self.color_matrix.controls[-1].left + CIRCLE_SIZE / 2,
        )
        self.update_selected_color_view(self.color)
        self.content.update()


def main(page: ft.Page):
    color_picker = CustomColorPicker()
    page.dialog = color_picker

    def open_color_picker(e):
        color_picker.open = True
        page.update()

    page.add(ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker))


ft.app(target=main)
