import flet as ft
import colorsys

WIDTH = 50
HEIGHT = 25
SQUARE_SIZE = 5
CIRCLE_SIZE = SQUARE_SIZE*5

class CustomColorPicker(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.content = ft.Column()
        self.generate_color_matrix(hue=0)
        self.on_dismiss=lambda e: print("Dialog dismissed!")
    
    def generate_color_matrix(self, hue):
        def rgb2hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255.0), int(rgb[1]*255.0), int(rgb[2]*255.0))
        
        selected_color = ft.Text()
        colors = ft.Stack(
            height=HEIGHT*SQUARE_SIZE+CIRCLE_SIZE, 
            width=WIDTH*SQUARE_SIZE+CIRCLE_SIZE
            )
        self.content.controls = []
        #colors.controls = []

        def pick_color(e):
            circle.top = e.control.top - CIRCLE_SIZE/2
            circle.left = e.control.left - CIRCLE_SIZE/2
            circle.bgcolor = e.control.bgcolor
            circle.update()
            selected_color.value = e.control.bgcolor
            selected_color.update()

        for j in range (0, HEIGHT):
            for i in range (0, WIDTH):
                #color = rgb2hex(colorsys.hsv_to_rgb(i/WIDTH,  1, 1 * (HEIGHT - j + 1) / HEIGHT))
                color = rgb2hex(colorsys.hsv_to_rgb(hue,  (i) /WIDTH, 1 * (HEIGHT - j) / HEIGHT))
                colors.controls.append(ft.Container(
                    height=SQUARE_SIZE, 
                    width=SQUARE_SIZE, 
                    bgcolor=color, 
                    on_click=pick_color,
                    top = j*SQUARE_SIZE+CIRCLE_SIZE/2,
                    left = i*SQUARE_SIZE+CIRCLE_SIZE/2  ))

        circle = ft.Container(
            top = 0,
            left = 0,
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            bgcolor='blue',
            border_radius=SQUARE_SIZE*5,
            border=ft.border.all(width=2, color='white'))

        colors.controls.append(circle)
        
        
        self.content.controls.append(colors)
        self.content.controls.append(selected_color)
        #self.update()


def main(page: ft.Page):
    
    color_picker = CustomColorPicker()
    page.dialog = color_picker

    def open_color_picker(e):
        color_picker.open = True
        page.update()
    
    page.add(ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker))
    
ft.app(target=main)