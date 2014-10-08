"""Dr. Python Game module"""

import sys
import pygame
from pygame.locals import *

from colors import *

FPS = 15
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class Game(object):

    def __init__(self):
        pygame.init()

        self.fpsClock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        pygame.display.set_caption('Dr. Python')

    def run(self):
        while True:
            for event in pygame.event.get():
                self.process_event(event)

            self.display.fill(DARKGRAY)

            pygame.display.update()
            self.fpsClock.tick(FPS)

    def process_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

