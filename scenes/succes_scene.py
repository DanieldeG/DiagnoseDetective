from scenes.base_scene import Scene
from ui.button import Button
from settings import *
import pygame

class SuccessScene(Scene):
    def __init__(self, game, score, total_cases):
        super().__init__(game, background_image=pygame.image.load('images/happy_ending.png'))
        self.score = score
        self.total_cases = total_cases
        self.button = Button("Back to Menu", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80, self.back_to_menu)

    def back_to_menu(self):
        from scenes.menu_scene import MenuScene
        self.game.change_scene(MenuScene)

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        super().render(screen)
        text_surface = self.font.render(f'You scores {self.score}/{self.total_cases}!', True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        screen.blit(text_surface, text_rect)
        self.button.draw(screen)
