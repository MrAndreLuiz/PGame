from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *


FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
# montante do desvio maximo da base para a esquerda
BASEY = SCREENHEIGHT + (SCREENWIDTH * 0.69 - SCREENWIDTH)
# imagem dicts
IMAGES = {}

# tupla com as tres posicoes da barbatana
PLAYER_LIST = (
    # peixe vermelho
    (
        'assets/images/redfish-upfin.png',
        'assets/images/redfish-midfin.png',
        'assets/images/redfish-downfin.png',
    ),
    # peixe azul
    (
        'assets/images/bluefish-upfin.png',
        'assets/images/bluefish-midfin.png',
        'assets/images/bluefish-downfin.png',
    ),
    # peixe amarelo
    (
        'assets/images/bluefish-upfin.png',
        'assets/images/bluefish-midfin.png',
        'assets/images/bluefish-downfin.png',
    ),
)

# fundo
BACKGROUND = 'assets/images/background.png'

# tronco
TRUNK = 'assets/images/trunk.png'


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('PGame - Alfa')

    # imagem de boas vindas
    IMAGES['welcome'] = pygame.image.load('assets/images/welcome.png').convert_alpha()
    # imagem da base (terreno)
    IMAGES['base'] = pygame.image.load('assets/images/base.png').convert_alpha()

    while True:
        IMAGES['background'] = pygame.image.load(BACKGROUND).convert()

        # seleciona imagens aleatorias dos personagens
        randPlayer = random.randint(0, len(PLAYER_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYER_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYER_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYER_LIST[randPlayer][2]).convert_alpha(),
        )

        initialAnimation()


def initialAnimation():
    """Mostra a animacao inicial"""
    # indice do personagem no blit da tela
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator usado para mudar playerIndex apos a quinta interacao
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['welcome'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # montante do desvio maximo da base para a esquerda
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # shm do personagem para o movimento de cima para baixo na tela inicial
    playerShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # ajusta playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = playerIndexGen.next()
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # desenha as imagens
        SCREEN.blit(IMAGES['background'], (0, 0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['welcome'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # testes de desempenho
        printFPS()

        # estrutura de teste
        pygame.quit()
        sys.exit()


def playerShm(playerShm):
    """Shm do personagem"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
        playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def printFPS():
    """Imprime o frame rate para testes de desempenho"""
    print "fps:", FPSCLOCK.get_fps()

if __name__ == '__main__':
    main()