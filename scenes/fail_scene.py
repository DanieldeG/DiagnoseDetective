# scenes/fail_scene.py
import pygame
from scenes.base_scene import Scene
from ui.button import Button
from settings import *

class FailScene(Scene):
    def __init__(self, game, message="Incorrect! Try again."):
        super().__init__(game)
        self.message = message
        self.button = Button("Back to Menu", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80, self.back_to_menu)
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE + 10)

    def back_to_menu(self):
        from scenes.menu_scene import MenuScene
        self.game.change_scene(MenuScene)

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(RED)
        text_surface = self.font.render(self.message, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        screen.blit(text_surface, text_rect)
        self.button.draw(screen)
