from pygame.math import Vector2

class Boid:
    def __init__(self, center, angle, size):
        self.center = center
        self.angle = angle
        self.size = size
        