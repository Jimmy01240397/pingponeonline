import pygame

import conf

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (x,y)
        self.color = color
        

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)