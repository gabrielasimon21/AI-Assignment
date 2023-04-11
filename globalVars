import time
from copy import deepcopy
from sys import exit
from pygame.locals import *
import sys 
import pygame

PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')

NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G',
            'G': '2', '2': 'A'}  # para onde as peças vão em ordem anti horaria

OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D',
                'K': 'E', 'L': 'F'}  # casa paralela do oponente, usada para regra de pegar as pedras do oponente

PIT_LABELS = 'ABCDEF1LKJIHG2'

pygame.init()

largura = 1400
altura = 788

tela = pygame.display.set_mode((largura, altura))
tela.fill((255, 255, 255))

cor_texto = (0, 0, 0)
tamanho_da_fonte1 = 75
fonte1 = pygame.font.Font(None, tamanho_da_fonte1)

tamanho_da_fonte2 = 40
fonte2 = pygame.font.Font(None, tamanho_da_fonte2)
