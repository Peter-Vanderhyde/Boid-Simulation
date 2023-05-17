import pygame

class NoGoZone:
    """A circular zone that boids will avoid moving through."""

    def __init__(self, position, radius, screen):
        self.position = position
        self.radius = radius
        self.screen = screen
        self.placed = False # False when being placed with mouse
    
    def draw(self):
        """Draws its circular border."""
        
        pygame.draw.circle(self.screen, (84, 151, 167), self.position, self.radius, 2)