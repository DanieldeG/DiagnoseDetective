from scenes.base_scene import Scene
from ui.button import Button
from settings import *
import pygame

class FailScene(Scene):
    def __init__(self, game, score, total_cases):
        super().__init__(game, background_image=pygame.image.load('images/sad_ending.png'))
        self.score = score
        self.total_cases = total_cases  
        self.retry_button = Button("Retry", SCREEN_WIDTH//8 * 5, SCREEN_HEIGHT//2 + 40, self.retry_game)
        self.menu_button = Button("Back to Menu", SCREEN_WIDTH//8 * 5, SCREEN_HEIGHT//2 + 100, self.back_to_menu)

    def back_to_menu(self):
        from scenes.menu_scene import MenuScene
        self.game.change_scene(MenuScene)
    
    def retry_game(self):
        from scenes.game_scene import GameScene
        self.game.change_scene(GameScene)

    def handle_events(self, events):
        for event in events:
            self.menu_button.handle_event(event)
            self.retry_button.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        super().render(screen)
        text_surface = self.font.render(f'You scored: {self.score}/{self.total_cases}!', True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//8 * 5, SCREEN_HEIGHT//2 - 40))
        screen.blit(text_surface, text_rect)
        self.menu_button.draw(screen)
        self.retry_button.draw(screen)
