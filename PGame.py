from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
# imagem dicts
IMAGES = {}

# tupla com as tres posicoes da barbatana
PLAYER_LIST = (
    'assets/images/redfish-upfin.png',
    'assets/images/redfish-midfin.png',
    'assets/images/redfish-downfin.png',
)

# fundo
BACKGROUND = 'assets/images/background.png'

def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('PGame')

    IMAGES['welcome'] = pygame.image.load('assets/images/welcome.png').convert_alpha()
    # imagem da base (terreno)
    IMAGES['base'] = pygame.image.load('assets/images/base.png').convert_alpha()

    IMAGES['background'] = pygame.image.load(BACKGROUND).convert()

    # seleciona imagens aleatorias do personagem
    randPlayer = random.randint(0, len(PLAYER_LIST) - 1)
    IMAGES['player'] = (
        pygame.image.load(PLAYER_LIST[randPlayer]).convert_alpha(),
        pygame.image.load(PLAYER_LIST[randPlayer]).convert_alpha(),
        pygame.image.load(PLAYER_LIST[randPlayer]).convert_alpha(),
    )

    pygame.display.update()
    FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()