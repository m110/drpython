"""Dr. Python Game module"""

import sys
import pygame
from pygame.locals import *

import drpython.board
from drpython.colors import *
from drpython.board import Board

FPS = 15
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

BOARD_OFFSET_X = (WINDOW_WIDTH - drpython.board.WIDTH_PIXELS) / 2
BOARD_OFFSET_Y = (WINDOW_HEIGHT - drpython.board.HEIGHT_PIXELS) / 2
BOARD_BORDER = 1

BLOCK_FALL_INTERVAL = 500

class Game(object):

    def __init__(self):
        self._board = Board()
        pygame.init()

        self._fpsClock = pygame.time.Clock()
        self._display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption('Dr. Python')

        self._block_fall_timer = BLOCK_FALL_INTERVAL

    def run(self):
        self.board.spawn_brick()

        while True:
            for event in pygame.event.get():
                self.process_event(event)

            self.update(self.fpsClock.get_time())

            self.display.fill(DARKGRAY)

            pygame.draw.rect(self.display, DARKBLUE,
                    (BOARD_OFFSET_X-BOARD_BORDER, BOARD_OFFSET_Y-BOARD_BORDER,
                     drpython.board.WIDTH_PIXELS+BOARD_BORDER*2, drpython.board.HEIGHT_PIXELS+BOARD_BORDER*2))
            board_display = self.board.render()
            self.display.blit(board_display, (BOARD_OFFSET_X, BOARD_OFFSET_Y))

            pygame.display.update()
            self.fpsClock.tick(FPS)

    def update(self, delta):

        if self._block_fall_timer <= 0:
            self.board.move_brick('down')
            self._block_fall_timer = BLOCK_FALL_INTERVAL
        else:
            self._block_fall_timer -= delta

    def process_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.board.move_brick('left')
            elif event.key == K_RIGHT:
                self.board.move_brick('right')

    @property
    def board(self):
        return self._board

    @property
    def display(self):
        return self._display

    @property
    def fpsClock(self):
        return self._fpsClock

