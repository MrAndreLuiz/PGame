from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512

def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('PGame')
    pygame.display.update()
    FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()