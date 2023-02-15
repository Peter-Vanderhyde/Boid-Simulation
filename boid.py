from pygame.math import Vector2

class Boid:
    def __init__(self, center, angle, size):
        self.center = center
        self.angle = angle
        self.length = size
        self.direction = Vector2(1, 0)
        self.direction.scale_to_length(size)
        self.direction.rotate_ip(angle)