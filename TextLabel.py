import pygame

from Canvas import *

class TextLabel:
    def __init__(self, text, font, color, position):
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.surface = None
        self.rect = None
        self.update_text(text)

    def update_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=self.position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
