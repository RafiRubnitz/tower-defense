import pygame

from game import Game


if __name__ == '__main__':
    # Window size: map is 40x30 grid (800x600) + UI panel (180px on right)
    win = pygame.display.set_mode((980, 600))
    pygame.display.set_caption("Tower Defense")
    game = Game(win)
    game.run()