import pygame
from settings import *

class Scene:
    def __init__(self, game, background_color=WHITE, background_image=None):
        self.game = game
        self.background_color = background_color
        self.background_image = background_image
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) if background_image else None
        self.small_font = pygame.font.Font(FONT_NAME, SMALL_FONT_SIZE)
        self.font = pygame.font.Font(FONT_NAME, STANDARD_FONT_SIZE)
        self.large_font = pygame.font.Font(FONT_NAME, LARGE_FONT_SIZE)

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(self.background_color)
