from colorthief import ColorThief
color_thief = ColorThief('images/shirt.jpg')
# dominant color
print(color_thief.get_color(quality=1))