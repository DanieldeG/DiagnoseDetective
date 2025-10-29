import pygame
from settings import *

class Button:
    def __init__(self, text, x, y, callback, width=200, height=50, color=BLUE, active=True):
        """Initialize a button instance."""
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.callback = callback
        self.font = pygame.font.Font(FONT_NAME, STANDARD_FONT_SIZE)
        self.color = color
        self.active = active

    def draw(self, screen):
        """Draw the button on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse click events."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.active:
            self.callback()
