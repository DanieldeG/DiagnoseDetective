import pygame
import random
import sys
from gamelogic import start_game 
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Diagnose Detective")

font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 22)

start_game(screen)