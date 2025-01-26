import pygame
import pygame.font

class PopupWindow:
    def __init__(self, title, message, width = 300, height = 200):
        self.title = title
        self.message = message  # message is now expected to be a list of strings (lines)
        self.width = width
        self.height = height
        self.font = pygame.font.Font("PressStart2p.ttf", 9)
        self.close_button_rect = pygame.Rect(self.width - 30, 10, 20, 20)
        self.running = True

    def draw(self, screen):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((255, 255, 255))

        screen.blit(overlay, (screen.get_width() // 2 - self.width // 2,
                                  screen.get_height() // 2 - self.height // 2))

        # Title rendering
        title_surface = self.font.render(self.title, True, (0, 0, 0))
        screen.blit(title_surface, (screen.get_width() // 2 - self.width // 2 + 10,
                                         screen.get_height() // 2 - self.height // 2 + 10))

        # Render each line of the message array
        y_offset = screen.get_height() // 2 - self.height // 2 + 40  # Start below the title
        for line in self.message:
            message_surface = self.font.render(line, True, (0, 0, 0))
            screen.blit(message_surface, (screen.get_width() // 2 - self.width // 2 + 10, y_offset))
            y_offset += 20  