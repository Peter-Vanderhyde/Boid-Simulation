import pygame

class NoGoZone:
    def __init__(self, position, radius, screen):
        self.position = position
        self.radius = radius
        self.screen = screen
        self.placed = False
    
    def draw(self):
        pygame.draw.circle(self.screen, (84, 151, 167), self.position, self.radius, 2)