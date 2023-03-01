from vector import Vector
import math

class Boid:
    def __init__(self, position, velocity, max_speed, view_distance, separation_distance):
        self.position = position
        self.velocity = velocity
        self.max_speed = max_speed
        self.view_distance = view_distance
        self.separation_distance = separation_distance
    
    def rotate_ip(self, angle):
        rad = math.radians(angle)
        cos = math.cos(rad)
        sin = math.sin(rad)
        self.velocity.x = self.velocity.x * cos - self.velocity.y * sin
        self.velocity.y = self.velocity.x * sin + self.velocity.y * cos
        self.velocity = self.velocity.normalize()

    def move(self, dt):
        self.position += self.velocity * self.max_speed * dt