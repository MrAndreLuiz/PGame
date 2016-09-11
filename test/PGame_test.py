#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *


FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
# montante do desvio maximo da base para a esquerda
TRUNKGAPSIZE  = 100 # espaco entre a parte superior e inferior do tronco
BASEY = SCREENHEIGHT * 0.79
# imagem, sons e hitmasks dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

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
        'assets/images/yellowfish-upfin.png',
        'assets/images/yellowfish-midfin.png',
        'assets/images/yellowfish-downfin.png',
    ),
)

# lista de fundos
BACKGROUNDS_LIST = (
    'assets/images/background-day.png',
    'assets/images/background-night.png',
)

# tronco
TRUNK = 'assets/images/trunk.png'


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Os Peixinhos - 1.0')

    # imagens dos numeros de pontuacao
    IMAGES['numbers'] = (
        pygame.image.load('assets/images/0.png').convert_alpha(),
        pygame.image.load('assets/images/1.png').convert_alpha(),
        pygame.image.load('assets/images/2.png').convert_alpha(),
        pygame.image.load('assets/images/3.png').convert_alpha(),
        pygame.image.load('assets/images/4.png').convert_alpha(),
        pygame.image.load('assets/images/5.png').convert_alpha(),
        pygame.image.load('assets/images/6.png').convert_alpha(),
        pygame.image.load('assets/images/7.png').convert_alpha(),
        pygame.image.load('assets/images/8.png').convert_alpha(),
        pygame.image.load('assets/images/9.png').convert_alpha()
    )

    # imagem de fim de jogo
    IMAGES['gameover'] = pygame.image.load('assets/images/gameover.png').convert_alpha()
    # imagem de boas vindas
    IMAGES['welcome'] = pygame.image.load('assets/images/welcome.png').convert_alpha()
    # imagem da base (terreno)
    IMAGES['base'] = pygame.image.load('assets/images/base.png').convert_alpha()

    # sons
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die'] = ('assets/audio/die' + soundExt)
    SOUNDS['hit'] = ('assets/audio/hit' + soundExt)
    SOUNDS['point'] = ('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = ('assets/audio/swoosh' + soundExt)
    SOUNDS['wing'] = ('assets/audio/wing' + soundExt)

    while True:
        # seleciona imagens aleatorias dos fundos
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # seleciona imagens aleatorias dos personagens
        randPlayer = random.randint(0, len(PLAYER_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYER_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYER_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYER_LIST[randPlayer][2]).convert_alpha(),
        )

        # seleciona imagens aleatorias dos troncos
        IMAGES['trunk'] = (
            pygame.transform.rotate(
                pygame.image.load(TRUNK).convert_alpha(), 180),
            pygame.image.load(TRUNK).convert_alpha(),
        )

        # histmask do tronco
        HITMASKS['trunk'] = (
            getHitmask(IMAGES['trunk'][0]),
            getHitmask(IMAGES['trunk'][1]),
        )

        # hitmask dos personagens
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        movementInfo = initialAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


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
    getIn = True

    while True:
        if getIn == True:
            SOUNDS['wing']
            return {
                'playery': playery + playerShmVals['val'],
                 'basex': basex,
                'playerIndexGen': playerIndexGen,
            }

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


def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # pega 2 novos troncos para adicionar para as listas de upperTrunks lowerTrunks
    newTrunk1 = getRandomTrunk()
    newTrunk2 = getRandomTrunk()

    # lista de troncos superiores
    upperTrunks = [
        {'x': SCREENWIDTH + 200, 'y': newTrunk1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newTrunk2[0]['y']},
    ]

    # lista de troncos inferiores
    lowerTrunks = [
        {'x': SCREENWIDTH + 200, 'y': newTrunk1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newTrunk2[1]['y']},
    ]

    trunkVelX = -4

    # velocidade do personagem, velocidade maxima, aceleracao de queda, aceleracao da nadadeira
    playerVelY    =  -9   # velocidade do personagem em Y, o mesmo padrao de playerFinped
    playerMaxVelY =  10   # max velocidade em Y, maxima velocidade de descida
    playerMinVelY =  -8   # min velocidade em Y, maxima velocidade de subida
    playerAccY    =   1   # velocidade de aceleracao de queda do personagem
    playerFinAcc =  -9   # velocidade de agitacao da nadadeira
    playerFinped = False # True quando as nadadeiras


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFinAcc
                    playerFinped = True
                    SOUNDS['wing']

        # verifica acidentes
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperTrunks, lowerTrunks)
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperTrunks': upperTrunks,
                'lowerTrunks': lowerTrunks,
                'score': score,
                'playerVelY': playerVelY,
            }

        # verifica a existencia de pontuacao
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for trunk in upperTrunks:
            trunkMidPos = trunk['x'] + IMAGES['trunk'][0].get_width() / 2
            if trunkMidPos <= playerMidPos < trunkMidPos + 4:
                score += 1
                SOUNDS['point']

        # mudancas em playerIndex basex
        if (loopIter + 1) % 3 == 0:
            playerIndex = playerIndexGen.next()
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # movimento do personagem
        if playerVelY < playerMaxVelY and not playerFinped:
            playerVelY += playerAccY
        if playerFinped:
            playerFinped = False
        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move os troncos para a esquerda
        for uTrunk, lTrunk in zip(upperTrunks, lowerTrunks):
            uTrunk['x'] += trunkVelX
            lTrunk['x'] += trunkVelX

        # adiciona novo tronco quando o primeiro tronco esta prestes a tocar a esquerda da tela
        if 0 < upperTrunks[0]['x'] < 5:
            newTrunk = getRandomTrunk()
            upperTrunks.append(newTrunk[0])
            lowerTrunks.append(newTrunk[1])

        # remove o primeiro tronco se ele esta fora da tela
        if upperTrunks[0]['x'] < -IMAGES['trunk'][0].get_width():
            upperTrunks.pop(0)
            lowerTrunks.pop(0)

        # desenha as imagens
        SCREEN.blit(IMAGES['background'], (0,0))

        for uTrunk, lTrunk in zip(upperTrunks, lowerTrunks):
            SCREEN.blit(IMAGES['trunk'][0], (uTrunk['x'], uTrunk['y']))
            SCREEN.blit(IMAGES['trunk'][1], (lTrunk['x'], lTrunk['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # exibe a pontuacao de forma que o personagem se sobrepoe a pontuacao
        showScore(score)
        SCREEN.blit(IMAGES['player'][playerIndex], (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """trava o personagem caido e mostra a imagem de fim de jogo"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2

    gameoverx = int((SCREENWIDTH - IMAGES['gameover'].get_width()) / 2)
    gameovery = int(SCREENHEIGHT * 0.35)

    basex = crashInfo['basex']

    upperTrunks, lowerTrunks = crashInfo['upperTrunks'], crashInfo['lowerTrunks']

    # executa sons de bater e morrer
    SOUNDS['hit']
    if not crashInfo['groundCrash']:
        SOUNDS['die']

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # mudanca do personagem em y
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # mudanca de velocidade do personagem
        if playerVelY < 15:
            playerVelY += playerAccY

        # desenha as imagens
        SCREEN.blit(IMAGES['background'], (0,0))

        for uTrunk, lTrunk in zip(upperTrunks, lowerTrunks):
            SCREEN.blit(IMAGES['trunk'][0], (uTrunk['x'], uTrunk['y']))
            SCREEN.blit(IMAGES['trunk'][1], (lTrunk['x'], lTrunk['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)
        SCREEN.blit(IMAGES['gameover'], (gameoverx, gameovery))
        SCREEN.blit(IMAGES['player'][1], (playerx,playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()

        print "modulos ok"
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


def getRandomTrunk():
    """retorna um tronco gerado aleatoriamente"""
    # espaco em y entre o tronco superior e inferior
    gapY = random.randrange(0, int(BASEY * 0.6 - TRUNKGAPSIZE))
    gapY += int(BASEY * 0.2)
    trunkHeight = IMAGES['trunk'][0].get_height()
    trunkX = SCREENWIDTH + 10

    return [
        {'x': trunkX, 'y': gapY - trunkHeight},  # tronco superior
        {'x': trunkX, 'y': gapY + TRUNKGAPSIZE}, # tronco inferior
    ]


def showScore(score):
    """exibe pontuacao na tela"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # largura total de todos os numeros a serem exibidos

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperTrunks, lowerTrunks):
    """retorna True se o personagem colide com a base ou os troncos"""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # se o personagem bater no chao
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        trunkW = IMAGES['trunk'][0].get_width()
        trunkH = IMAGES['trunk'][0].get_height()

        for uTrunk, lTrunk in zip(upperTrunks, lowerTrunks):
            # rects superiores e inferiores dos troncos
            uTrunkRect = pygame.Rect(uTrunk['x'], uTrunk['y'], trunkW, trunkH)
            lTrunkRect = pygame.Rect(lTrunk['x'], lTrunk['y'], trunkW, trunkH)

            # hitmasks dos personagens e tronco superior/inferior
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['trunk'][0]
            lHitmask = HITMASKS['trunk'][1]

            # se o personagem colidiu com utrunk ou ltrunk
            uCollide = pixelCollision(playerRect, uTrunkRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lTrunkRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Verifica se dois objetos colidem e nao apenas os seus rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False


def getHitmask(image):
    """retorna a hitmask usando o alfa de uma imagem"""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask

if __name__ == '__main__':
    main()