import pygame
from pygame.locals import *
from BoardAndPieces import Board

COLORS = {'white': (255, 255, 255), 'black': (0, 0, 0), 'porcelain': (255, 254, 253)}

BOARD_COLORS = {'light': COLORS['porcelain'], 'dark': (60, 179, 113) }

pygame.init()

screen = pygame.display.set_mode( [700, 700] )

board = Board((80, 80), 60)

def drawBoard():
    for square in board.squares:
        pygame.draw.rect( screen, BOARD_COLORS['dark'] if square.is_dark else BOARD_COLORS['light'], pygame.Rect( square.coordinates, (board.cellSize, board.cellSize) ) )

        if square.piece:
            screen.blit( square.piece.image )
            pass