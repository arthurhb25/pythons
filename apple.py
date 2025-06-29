import pygame
import random
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, RED

class Apple:
    def __init__(self):
        self.color = RED
        self.rect = pygame.Rect(0, 0, GRID_SIZE, GRID_SIZE)

    def randomize(self, pythons):
        while True:
            self.rect.topleft = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            collision = False
            for python in pythons:
                if self.rect.collidelist(python.body) != -1:
                    collision = True
                    break
            if not collision:
                break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
