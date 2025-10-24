# scenes/menu_scene.py
import pygame
import json
from scenes.base_scene import Scene
from ui.button import Button
from settings import *
from scenes.game_scene import GameScene

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game, background_image=pygame.image.load('images/main_menu_background.png'))
        self.title = self.font.render("Diagnose Detective", True, BLACK)
        self.title_rect = self.title.get_rect(center=(SCREEN_WIDTH//2, 30))
        self.mode = "main"
        self.level_buttons = [
            Button("Easy", SCREEN_WIDTH//4 * 3, SCREEN_HEIGHT//8 * 3, lambda: self.start_game("easy"), active=False),
            Button("Medium", SCREEN_WIDTH//4 * 3, SCREEN_HEIGHT//8 * 4, lambda: self.start_game("medium"), active=False),
            Button("Hard", SCREEN_WIDTH//4 * 3, SCREEN_HEIGHT//8 * 5, lambda: self.start_game("hard"), active=False)
        ]
        self.start_button = Button("Start Game", SCREEN_WIDTH//4 * 3, SCREEN_HEIGHT//8 * 3, self.show_levels)
        self.exit_button = Button("Exit", SCREEN_WIDTH//4 * 3, SCREEN_HEIGHT//8 * 4, self.exit_game, color=RED)

    def start_game(self, level):
        self.game.level = level
        self.game.change_scene(GameScene)
    
    def exit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def show_levels(self):
        self.start_button.active = False
        self.exit_button.active = False
        for btn in self.level_buttons:
            btn.active = True
        self.mode = "level_select"

    def handle_events(self, events):
        for event in events:
            if self.mode == "main":
                self.start_button.handle_event(event)
                self.exit_button.handle_event(event)
            elif self.mode == "level_select":
                for btn in self.level_buttons:
                    btn.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        super().render(screen)
        screen.blit(self.title, self.title_rect)
        if self.mode == "level_select":
            for btn in self.level_buttons:
                btn.draw(screen)
        elif self.mode == "main":
            self.start_button.draw(screen)
            self.exit_button.draw(screen)
