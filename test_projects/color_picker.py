import flet as ft
import colorsys

COLOR_MATRIX_WIDTH = 280
COLOR_MATRIX_HEIGHT = 160
COLOR_BLOCK_SIDE = 8

SLIDER_WIDTH = 180
NUMBER_OF_HUES = 20

CIRCLE_SIZE = 16


def rgb2hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0] * 255.0), int(rgb[1] * 255.0), int(rgb[2] * 255.0)
    )


def hex2rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


class HueSlider(ft.Stack):
    def __init__(self, on_change_hue):
        super().__init__()
        self.height = CIRCLE_SIZE
        self.width = SLIDER_WIDTH
        self.generate_hues()
        self.on_change_hue = on_change_hue

    def find_hue(self, x):
        for hue_block in self.controls[
            :-1
        ]:  # excluding the last element of the stack controls list which is the circle
            if x >= hue_block.left and x <= hue_block.left + self.hue_width:
                color = hue_block.bgcolor
                rgb_color = hex2rgb(color)
                hsv_color = colorsys.rgb_to_hsv(
                    round(rgb_color[0] / 255, 1),
                    round(rgb_color[1] / 255, 1),
                    round(rgb_color[2] / 255, 1),
                )
                return hsv_color[0]
        return 0

    def generate_hues(self):
        def pick_hue(e):
            rgb_color = hex2rgb(e.control.bgcolor)
            hsv_color = colorsys.rgb_to_hsv(
                round(rgb_color[0] / 255, 1),
                round(rgb_color[1] / 255, 1),
                round(rgb_color[2] / 255, 1),
            )
            self.on_change_hue(hsv_color[0])
            circle.left = e.control.left + self.hue_width / 2 - CIRCLE_SIZE / 2
            circle.content.bgcolor = e.control.bgcolor
            circle.update()

        self.hue_width = (self.width - CIRCLE_SIZE) / (NUMBER_OF_HUES + 1)
        for i in range(0, NUMBER_OF_HUES + 1):
            color = rgb2hex(colorsys.hsv_to_rgb(i / NUMBER_OF_HUES, 1, 1))
            if i == 0:
                border_radius = ft.border_radius.only(top_left=5, bottom_left=5)
            elif i == NUMBER_OF_HUES:
                border_radius = ft.border_radius.only(top_right=5, bottom_right=5)
            else:
                border_radius = None
            self.controls.append(
                ft.Container(
                    height=CIRCLE_SIZE / 2,
                    width=self.hue_width,
                    bgcolor=color,
                    border_radius=border_radius,
                    on_click=pick_hue,
                    top=CIRCLE_SIZE / 4,
                    left=i * self.hue_width + CIRCLE_SIZE / 2,
                )
            )

        def on_pan_update(e: ft.DragUpdateEvent):
            if e.control.left + e.delta_x < self.width - CIRCLE_SIZE:
                e.control.left = max(0, e.control.left + e.delta_x)

            hue = self.find_hue(x=e.control.left + CIRCLE_SIZE / 2)
            e.control.content.bgcolor = rgb2hex(colorsys.hsv_to_rgb(hue, 1, 1))
            self.on_change_hue(hue)
            e.control.update()

        circle = ft.GestureDetector(
            top=0,
            left=0,
            on_pan_update=on_pan_update,
            # on_pan_end=on_pan_end,
            content=ft.Container(
                width=CIRCLE_SIZE,
                height=CIRCLE_SIZE,
                bgcolor="#ff0000",
                border_radius=CIRCLE_SIZE,
                border=ft.border.all(width=2, color="white"),
            ),
        )

        self.controls.append(circle)


class HueSlider1(ft.GestureDetector):
    def __init__(self, on_change_hue):
        super().__init__()
        self.content = ft.Stack(height=CIRCLE_SIZE, width=SLIDER_WIDTH)
        self.generate_hues()
        self.on_change_hue = on_change_hue
        self.on_pan_start = self.start_drag

    def find_hue(self, x):
        for hue_block in self.content.controls[
            :-1
        ]:  # excluding the last element of the stack controls list which is the circle
            if x >= hue_block.left and x <= hue_block.left + self.hue_width:
                color = hue_block.bgcolor
                rgb_color = hex2rgb(color)
                hsv_color = colorsys.rgb_to_hsv(
                    round(rgb_color[0] / 255, 1),
                    round(rgb_color[1] / 255, 1),
                    round(rgb_color[2] / 255, 1),
                )
                return hsv_color[0]
        return 0

    def start_drag(self, e: ft.DragStartEvent):
        hue = self.find_hue(e.local_x)

        color = rgb2hex(colorsys.hsv_to_rgb(hue, 1, 1))
        self.circle.left = e.local_x - CIRCLE_SIZE / 2

        # self.circle.bgcolor = color
        self.circle.update()
        self.on_change_hue(hue)

    # def on_pan_start(self, e: ft.DragStartEvent):
    #     print("Start drag!")

    def generate_hues(self):
        # def pick_hue(e):
        #     rgb_color = hex2rgb(e.control.bgcolor)
        #     hsv_color = colorsys.rgb_to_hsv(
        #         round(rgb_color[0] / 255, 1),
        #         round(rgb_color[1] / 255, 1),
        #         round(rgb_color[2] / 255, 1),
        #     )
        #     self.on_change_hue(hsv_color[0])
        #     circle.left = e.control.left + self.hue_width / 2 - CIRCLE_SIZE / 2
        #     circle.content.bgcolor = e.control.bgcolor
        #     circle.update()

        self.hue_width = (self.content.width - CIRCLE_SIZE) / (NUMBER_OF_HUES + 1)
        for i in range(0, NUMBER_OF_HUES + 1):
            color = rgb2hex(colorsys.hsv_to_rgb(i / NUMBER_OF_HUES, 1, 1))
            if i == 0:
                border_radius = ft.border_radius.only(top_left=5, bottom_left=5)
            elif i == NUMBER_OF_HUES:
                border_radius = ft.border_radius.only(top_right=5, bottom_right=5)
            else:
                border_radius = None
            self.content.controls.append(
                ft.Container(
                    height=CIRCLE_SIZE / 2,
                    width=self.hue_width,
                    bgcolor=color,
                    border_radius=border_radius,
                    # on_click=pick_hue,
                    top=CIRCLE_SIZE / 4,
                    left=i * self.hue_width + CIRCLE_SIZE / 2,
                )
            )

        # def on_pan_update(e: ft.DragUpdateEvent):
        #     if e.control.left + e.delta_x < self.width - CIRCLE_SIZE:
        #         e.control.left = max(0, e.control.left + e.delta_x)

        #     hue = self.find_hue(x=e.control.left + CIRCLE_SIZE / 2)
        #     e.control.content.bgcolor = rgb2hex(colorsys.hsv_to_rgb(hue, 1, 1))
        #     self.on_change_hue(hue)
        #     e.control.update()

        # circle = ft.GestureDetector(
        #     top=0,
        #     left=0,
        #     on_pan_update=on_pan_update,
        #     # on_pan_end=on_pan_end,
        #     content=ft.Container(
        #         width=CIRCLE_SIZE,
        #         height=CIRCLE_SIZE,
        #         bgcolor="#ff0000",
        #         border_radius=CIRCLE_SIZE,
        #         border=ft.border.all(width=2, color="white"),
        #     ),
        # )
        self.circle = ft.Container(
            top=0,
            left=0,
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            bgcolor="#ff0000",
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.content.controls.append(self.circle)


class CustomColorPicker(ft.Column):
    def __init__(self, color="#000000"):
        super().__init__()
        self.color = color
        # self.content = ft.Column()
        self.hue_slider = HueSlider1(
            on_change_hue=self.update_color_matrix,
        )
        self.generate_color_matrix(hue=0)
        self.generate_selected_color_view(color=self.color)
        # self.on_dismiss = lambda e: print("Dialog dismissed!")

    def change_hue(self, e: ft.DragStartEvent):
        print("Start drag on hue slider!")

    def find_color(self, x, y):
        for color_square in self.color_matrix.content.controls[
            :-1
        ]:  # excluding the last element of the controls list which is the circle
            if (
                y >= color_square.top
                and y <= color_square.top + self.square_side
                and x >= color_square.left
                and x <= color_square.left + self.square_side
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
        # self.content.controls.append(self.selected_color_view)
        self.controls.append(self.selected_color_view)

    def update_selected_color_view(self, color):
        rgb = hex2rgb(color)
        self.selected_color_view.content.controls[0].controls[
            0
        ].bgcolor = color  # Colored circle
        self.selected_color_view.content.controls[1].controls[0].value = color  # Hex
        self.selected_color_view.content.controls[1].controls[1].value = rgb[0]  # R
        self.selected_color_view.content.controls[1].controls[2].value = rgb[1]  # G
        self.selected_color_view.content.controls[1].controls[3].value = rgb[2]  # B
        self.color_matrix.content.controls[-1].bgcolor = color  # Color matrix circle
        self.update()

    def generate_color_matrix(self, hue):
        self.square_side = COLOR_BLOCK_SIDE
        self.colors_x = int(COLOR_MATRIX_WIDTH / self.square_side)
        self.colors_y = int(COLOR_MATRIX_HEIGHT / self.square_side)

        def on_pan_start(e: ft.DragStartEvent):
            circle.top = max(
                0,
                min(
                    e.local_y - CIRCLE_SIZE / 2,
                    self.color_matrix.content.height - CIRCLE_SIZE,
                ),
            )
            circle.left = max(
                0,
                min(
                    e.local_x - CIRCLE_SIZE / 2,
                    self.color_matrix.content.width - CIRCLE_SIZE,
                ),
            )
            circle.update()
            self.color = self.find_color(
                x=circle.left + CIRCLE_SIZE / 2, y=circle.top + CIRCLE_SIZE / 2
            )
            self.update_selected_color_view(self.color)

        def on_pan_update(e: ft.DragUpdateEvent):
            circle.top = max(
                0,
                min(
                    e.local_y - CIRCLE_SIZE / 2,
                    self.color_matrix.content.height - CIRCLE_SIZE,
                ),
            )
            circle.left = max(
                0,
                min(
                    e.local_x - CIRCLE_SIZE / 2,
                    self.color_matrix.content.width - CIRCLE_SIZE,
                ),
            )
            self.color = self.find_color(
                x=circle.left + CIRCLE_SIZE / 2, y=circle.top + CIRCLE_SIZE / 2
            )
            self.update_selected_color_view(self.color)

        self.color_matrix = ft.GestureDetector(
            content=ft.Stack(
                height=(self.colors_y + 1) * COLOR_BLOCK_SIDE + CIRCLE_SIZE,
                width=(self.colors_x + 1) * COLOR_BLOCK_SIDE + CIRCLE_SIZE,
            ),
            on_pan_start=on_pan_start,
            on_pan_update=on_pan_update,
        )

        self.color_matrix = ft.GestureDetector(
            content=ft.Stack(
                height=(self.colors_y + 1) * COLOR_BLOCK_SIDE + CIRCLE_SIZE,
                width=(self.colors_x + 1) * COLOR_BLOCK_SIDE + CIRCLE_SIZE,
            ),
            on_pan_start=on_pan_start,
            on_pan_update=on_pan_update,
        )
        # self.content.controls = []

        for j in range(0, self.colors_y + 1):
            for i in range(0, self.colors_x + 1):
                color = rgb2hex(
                    colorsys.hsv_to_rgb(
                        hue,
                        (i) / self.colors_x,
                        1 * (self.colors_y - j) / self.colors_y,
                    )
                )
                if i == 0 and j == 0:
                    border_radius = ft.border_radius.only(top_left=5)
                elif i == 0 and j == self.colors_y:
                    border_radius = ft.border_radius.only(bottom_left=5)
                elif i == self.colors_x and j == 0:
                    border_radius = ft.border_radius.only(top_right=5)
                elif i == self.colors_x and j == self.colors_y:
                    border_radius = ft.border_radius.only(bottom_right=5)
                else:
                    border_radius = None
                self.color_matrix.content.controls.append(
                    ft.Container(
                        height=self.square_side,
                        width=self.square_side,
                        border_radius=border_radius,
                        bgcolor=color,
                        # on_click=pick_color,
                        top=j * self.square_side + CIRCLE_SIZE / 2,
                        left=i * self.square_side + CIRCLE_SIZE / 2,
                    )
                )

        circle = ft.Container(
            top=(self.colors_y + 1) * self.square_side,
            left=0,
            # on_pan_update=on_pan_update,
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            bgcolor=self.color,
            border_radius=CIRCLE_SIZE,
            border=ft.border.all(width=2, color="white"),
        )

        self.color_matrix.content.controls.append(circle)
        # self.content.controls.append(self.color_matrix)
        self.controls.append(self.color_matrix)

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
                # self.content.controls[0].content.controls[n].bgcolor = color
                self.controls[0].content.controls[n].bgcolor = color
                n += 1
        self.color = self.find_color(
            x=self.color_matrix.content.controls[-1].top + CIRCLE_SIZE / 2,
            y=self.color_matrix.content.controls[-1].left + CIRCLE_SIZE / 2,
        )
        self.update_selected_color_view(self.color)
        # self.content.update()
        self.update()


def main(page: ft.Page):
    color_picker = CustomColorPicker()
    # page.dialog = color_picker
    d = ft.AlertDialog(content=color_picker)
    page.dialog = d

    def open_color_picker(e):
        d.open = True
        page.update()

    page.add(ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker))


ft.app(target=main)
