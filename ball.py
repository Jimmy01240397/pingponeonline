import pygame

import conf

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, radius*2, radius*2)
        self.rect.center = (x,y)
        self.radius = radius
        self.color = color
        

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)