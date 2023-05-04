from pygame.math import Vector2 as Vector

class Boid:
    def __init__(self, settings, position, velocity=Vector(0), color=(0, 0, 0)):
        self.settings = settings
        self.position = position
        self.velocity = velocity
        self.color = color