import pygame
from vector import Vector

class Canvas:
    def __init__(self, screen, bg_color):
        self.screen = screen
        self.bg_color = bg_color
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def draw_background(self):
        self.screen.fill(self.bg_color)
    
    def draw_boids(self, boids):
        SIZE = 8
        for boid in boids:
            perpendicular = Vector(boid.velocity.y, -boid.velocity.x)
            perpendicular /= 2
            point_1 = boid.position + boid.velocity * SIZE
            point_2 = boid.position - boid.velocity * SIZE + perpendicular * SIZE
            point_3 = boid.position - boid.velocity * SIZE - perpendicular * SIZE
            boid_points = [point_1.values(),
                            point_2.values(),
                            (boid.position - boid.velocity * SIZE * 0.75).values(),
                            point_3.values()]
            pygame.draw.polygon(self.screen, (0, 0, 0), boid_points)
            # pygame.draw.line(self.screen, (255, 0, 0), boid.center, boid.center + boid.direction)
            # pygame.draw.line(self.screen, (0, 255, 0), boid.center, boid.center - boid.direction)
            # pygame.draw.line(self.screen, (0, 0, 0), boid.center + boid.direction, boid.center - boid.direction)
    
    def draw(self, boids):
        self.draw_background()
        self.draw_boids(boids)