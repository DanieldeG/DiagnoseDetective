# scenes/menu_scene.py
import pygame
from scenes.base_scene import Scene
from ui.button import Button
from settings import *

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game, background_image=pygame.image.load('images/main_menu_background.png'))
        self.start_button = Button("Start Game", SCREEN_WIDTH//4 * 3, SCREEN_HEIGHT//4 * 3, self.start_game)
        self.exit_button = Button("Exit", SCREEN_WIDTH//4 * 3, SCREEN_HEIGHT//4 * 2, self.exit_game)

    def start_game(self):
        from scenes.game_scene import GameScene
        self.game.change_scene(GameScene)
    
    def exit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def handle_events(self, events):
        for event in events:
            self.start_button.handle_event(event)
            self.exit_button.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        super().render(screen)
        self.start_button.draw(screen)
        self.exit_button.draw(screen)
