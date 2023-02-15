from pygame.math import Vector2
import pygame

class Canvas:
    def __init__(self, screen, bg_color):
        self.screen = screen
        self.bg_color = bg_color
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def draw_background(self):
        self.screen.fill(self.bg_color)
    
    def draw_boids(self, boids):
        for boid in boids:
            perpendicular = Vector2(boid.direction.y, -boid.direction.x)
            perpendicular /= 2
            boid_points = [boid.center + boid.direction, boid.center - boid.direction + perpendicular, boid.center - boid.direction - perpendicular]
            pygame.draw.polygon(self.screen, (0, 0, 0), boid_points)
            # pygame.draw.line(self.screen, (255, 0, 0), boid.center, boid.center + boid.direction)
            # pygame.draw.line(self.screen, (0, 255, 0), boid.center, boid.center - boid.direction)
            # pygame.draw.line(self.screen, (0, 0, 0), boid.center + boid.direction, boid.center - boid.direction)
    
    def draw(self, boids):
        self.draw_background()
        self.draw_boids(boids)