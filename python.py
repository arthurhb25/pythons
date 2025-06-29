import pygame
from config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

class Python:
    def __init__(self, x, y, color, keys):
        self.color = color
        self.keys = keys
        self.body = [pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)]
        self.direction = (1, 0)
        self.alive = True
        self.score = 0

    def handle_input(self, event):
        if not self.alive:
            return

        if event.type == pygame.KEYDOWN and event.key in self.keys:
            new_direction = self.keys[event.key]
            if (new_direction[0] != -self.direction[0] or
                new_direction[1] != -self.direction[1]):
                self.direction = new_direction

    def move(self):
        if not self.alive:
            return

        head = self.body[0].copy()
        head.move_ip(self.direction[0] * GRID_SIZE, self.direction[1] * GRID_SIZE)

        if head.left < 0:
            head.left = (GRID_WIDTH - 1) * GRID_SIZE
        elif head.right > GRID_WIDTH * GRID_SIZE:
            head.left = 0
        if head.top < 0:
            head.top = (GRID_HEIGHT - 1) * GRID_SIZE
        elif head.bottom > GRID_HEIGHT * GRID_SIZE:
            head.top = 0

        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        if not self.alive:
            return
        tail = self.body[-1].copy()
        self.body.append(tail)
        self.score += 1

    def check_collision(self):
        if not self.alive:
            return
        head = self.body[0]
        for segment in self.body[1:]:
            if head.colliderect(segment):
                self.alive = False
                break

    def draw(self, surface):
        if not self.alive:
            return
        for segment in self.body:
            pygame.draw.rect(surface, self.color, segment)