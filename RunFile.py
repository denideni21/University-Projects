import pygame
from GameClass import Game

pygame.init()
init = pygame.font.init()

new_game = Game()
new_game.game_loop()
pygame.quit()
