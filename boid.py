from pygame.math import Vector2
import math

class Boid:
    def __init__(self, position, velocity, max_speed):
        self.position = position
        self.velocity = velocity
        self.max_speed = max_speed
    
    def rotate_ip(self, angle):
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        self.velocity.x = self.velocity.x * cos - self.velocity.y * sin
        self.velocity.y = self.velocity.x * sin + self.velocity.y * cos
        self.velocity = self.velocity.normalize()

    def move(self):
        self.position += self.velocity * self.max_speed
    
    def separation(self, boids):
        pass

    def alignment(self, boids):
        pass

    def cohesion(self, boids):
        pass

