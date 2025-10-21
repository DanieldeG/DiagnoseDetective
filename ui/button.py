# ui/button.py
import pygame
from settings import *

class Button:
    def __init__(self, text, x, y, callback, width=200, height=50):
        self.text = text
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.callback = callback
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.color = BLUE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()
