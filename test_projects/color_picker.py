import flet as ft
import colorsys

WIDTH = 50
HEIGHT = 50

class CustomColorPicker(ft.AlertDialog):
    def __init__(self):
        pass

def main(page: ft.Page):
    
    def rgb2hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255.0), int(rgb[1]*255.0), int(rgb[2]*255.0))
    
    grey_colors = ft.Row(spacing=0)
    grey_colors.controls = []

    # grey colors
    # for i in range(0, WIDTH):
    #     color = rgb2hex(colorsys.hsv_to_rgb(0, 0, i/WIDTH))
    #     grey_colors.controls.append(ft.Container(height=20, width=20, bgcolor = color))
    # color matrix
    #color = 'red'
    colors = ft.Column(spacing=0)
    colors.controls = []
    hue = 0.1
    for j in range (0, HEIGHT):
        colors.controls.append(ft.Row(spacing=0))
        for i in range (0, WIDTH):
            #color = rgb2hex(colorsys.hsv_to_rgb(i/WIDTH,  1, 1 * (HEIGHT - j + 1) / HEIGHT))
            color = rgb2hex(colorsys.hsv_to_rgb(hue,  (i) /WIDTH, 1 * (HEIGHT - j) / HEIGHT))
            colors.controls[-1].controls.append(ft.Container(height=5, width=5, bgcolor = color))

        

    #print(colors)
    #page.add(ft.Text("ColorPicker"), grey_colors, colors)
    page.add(ft.Text("ColorPicker"), colors)
ft.app(target=main)


# void loadColors()
# {
#     colors = new Color[width, height];

#     // load greys
#     for (int i = 0; i < width; i++ ) colors[i, 0] = HsvToRgb(0f, 0f, 1f * i / width);
#     // load bright stripe:
#     for (int i = 0; i < width; i++) colors[i, 1] = HsvToRgb(i* 360f / width, 0.33f, 1f);
#     // load matrix:
#     for (int j = 2; j < height; j++)
#         for (int i = 0; i < width; i++) 
#              colors[i, j] = HsvToRgb(i * 360f / width, 1f, 1f * (height - j + 2) / height);
# }