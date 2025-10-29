from scenes.base_scene import Scene
from ui.button import Button
from settings import *
import pygame

class SuccessScene(Scene):
    def __init__(self, game, score, total_cases):
        """Initialize the success scene."""
        super().__init__(game, background_image=pygame.image.load('images/happy_ending.png'))
        self.score = score
        self.total_cases = total_cases
        self.menu_button = Button("Back to Menu", SCREEN_WIDTH//8 * 5, SCREEN_HEIGHT//2 + 100, self.back_to_menu)
        self.retry_button = Button("Retry", SCREEN_WIDTH//8 * 5, SCREEN_HEIGHT//2 + 40, self.retry_game)

        # Add "Next Level" button only if not on hardest level
        if self.game.level != "hard":
            self.next_level_button = Button("Next Level", SCREEN_WIDTH//8 * 5, SCREEN_HEIGHT//2 + 160, self.next_level)

    def back_to_menu(self):
        """Navigate back to the main menu."""
        from scenes.menu_scene import MenuScene
        self.game.change_scene(MenuScene)
    
    def retry_game(self):
        """Restart the current game level."""
        from scenes.game_scene import GameScene
        self.game.change_scene(GameScene)
    
    def next_level(self):
        """Advance to the next game level."""
        from scenes.game_scene import GameScene
        if self.game.level == "easy":
            self.game.level = "medium"
        elif self.game.level == "medium":
            self.game.level = "hard"
        self.game.change_scene(GameScene)

    def handle_events(self, events):
        """Handle input events for the success scene."""
        for event in events:
            self.menu_button.handle_event(event)
            self.retry_button.handle_event(event)

            # Handle next level button only if it exists
            if self.game.level != "hard":
                self.next_level_button.handle_event(event)

    def update(self, dt):
        pass

    def render(self, screen):
        """Render all objects in the success scene."""
        super().render(screen)
        text_surface = self.font.render(f'You scored: {self.score}/{self.total_cases}!', True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//8 * 5, SCREEN_HEIGHT//2 - 40))
        screen.blit(text_surface, text_rect)
        self.menu_button.draw(screen)
        self.retry_button.draw(screen)
        if self.game.level != "hard":
            self.next_level_button.draw(screen)
