import flet as ft
import colorsys

WIDTH = 50
HEIGHT = 50

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
        #colors = ft.Column(spacing=0)
        colors = ft.Stack(height=50*5, width=50*5)
        self.content.controls = []
        #colors.controls = []

        def pick_color(e):
            circle.top = e.control.top
            circle.left = e.control.left
            circle.bgcolor = e.control.bgcolor
            circle.update()
            selected_color.value = e.control.bgcolor
            selected_color.update()

        for j in range (0, HEIGHT):
            #colors.controls.append(ft.Row(spacing=0))
            for i in range (0, WIDTH):
                #color = rgb2hex(colorsys.hsv_to_rgb(i/WIDTH,  1, 1 * (HEIGHT - j + 1) / HEIGHT))
                color = rgb2hex(colorsys.hsv_to_rgb(hue,  (i) /WIDTH, 1 * (HEIGHT - j) / HEIGHT))
                # colors.controls[-1].controls.append(ft.Container(
                #     height=5, 
                #     width=5, 
                #     bgcolor=color,
                #     on_click=pick_color
                #     ))
                colors.controls.append(ft.Container(
                    height=5, 
                    width=5, 
                    bgcolor=color, 
                    on_click=pick_color,
                    top = j*5,
                    left = i*5  ))

        circle = ft.Container(
            top = 0,
            left = 0,
            width=30,
            height=30,
            bgcolor='blue',
            border_radius=30,
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