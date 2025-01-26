import pygame

from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

def on_tray_click(icon, item):
    global running, minimized
    minimized = False
    pygame.display.set_mode((400, 400))
    icon.stop()

def quit_app(icon, item):
    global running
    running = False
    icon.stop()

def run_tray():
    tray_image = create_image()
    menu = Menu(
        MenuItem("Open", on_tray_click),
        MenuItem("Quit", quit_app)
    )
    tray_icon = Icon("Tamagotchi", tray_image, "Tamagotchi Anteater", menu)
    tray_icon.run()
    
def create_image():
    size = 64
    color = "blue"
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, size, size), fill=color)
    return image