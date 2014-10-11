"""Dr. Python Game module"""

import sys
import pygame
from pygame.locals import *

import drpython.board
from drpython.colors import *
from drpython.board import Board
from drpython.exceptions import *

FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

BOARD_OFFSET_X = (WINDOW_WIDTH - drpython.board.WIDTH_PIXELS) / 2
BOARD_OFFSET_Y = (WINDOW_HEIGHT - drpython.board.HEIGHT_PIXELS) / 2
BOARD_BORDER = 1

BLOCK_FALL_INTERVAL = 100

class Game(object):

    def __init__(self):
        self._board = Board()
        pygame.init()

        self._fpsClock = pygame.time.Clock()
        self._display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption('Dr. Python')

        self._block_fall_timer = BLOCK_FALL_INTERVAL

        self._speed = False

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
            try:
                self.board.move_brick('down')
            except (BottomReached, PositionOccupied):
                self.handle_collision()

            self._block_fall_timer = BLOCK_FALL_INTERVAL
        else:
            if self._speed:
                delta *= 100.0

            print delta
            self._block_fall_timer -= delta

    def handle_collision(self):
        self.board.spawn_brick()

    def process_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_RIGHT:
                direction = 'left' if event.key == K_LEFT else 'right'
                self.move_brick(direction)
            elif event.key == K_DOWN:
                self._speed = True
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self._speed = False

    def move_brick(self, direction):
        try:
            self.board.move_brick(direction)
        except (OutOfBoard, PositionOccupied):
            # Simply ignore those, the brick will not move at all
            pass

    @property
    def board(self):
        return self._board

    @property
    def display(self):
        return self._display

    @property
    def fpsClock(self):
        return self._fpsClock

