import pygame
import sys
from settings import *
from scenes.menu_scene import MenuScene
from scenes.game_scene import GameScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Diagnose Detective")
        self.clock = pygame.time.Clock()
        self.active_scene = MenuScene(self)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000  # Delta time for frame-independent movement
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.active_scene.handle_events(events)
            self.active_scene.update(dt)
            self.active_scene.render(self.screen)

            pygame.display.flip()

    def change_scene(self, new_scene_class):
        """Switch to a different scene."""
        self.active_scene = new_scene_class(self)

if __name__ == "__main__":
    game = Game()
    game.run()
