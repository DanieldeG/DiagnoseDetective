import pygame

def start_game(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # Scherm wit maken
        pygame.display.flip()  # Update het scherm
