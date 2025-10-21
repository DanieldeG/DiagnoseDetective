# scenes/menu_scene.py
import pygame
from scenes.base_scene import Scene
from ui.button import Button
from settings import *

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.start_button = Button("Start Game", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, self.start_game)

    def start_game(self):
        from scenes.game_scene import GameScene
        self.game.change_scene(GameScene)

    def handle_events(self, events):
        for event in events:
            self.start_button.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill(WHITE)
        self.start_button.draw(screen)
