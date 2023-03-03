import pygame
from vector import Vector

class Canvas:
    def __init__(self, screen, bg_color):
        self.screen = screen
        self.bg_color = bg_color
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def draw_background(self, active_area):
        self.screen.fill(self.bg_color)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(active_area[0], (active_area[1], active_area[2])), 1)
    
    def draw_boids(self, boids, show_circles):
        SIZE = 8
        for boid in boids:
            perpendicular = Vector(boid.velocity.y, -boid.velocity.x).normalize()
            perpendicular /= 2
            point_1 = boid.position + boid.velocity.normalize() * SIZE
            point_2 = boid.position - boid.velocity.normalize() * SIZE + perpendicular * SIZE
            point_3 = boid.position - boid.velocity.normalize() * SIZE - perpendicular * SIZE
            boid_points = [point_1.values(),
                            point_2.values(),
                            point_3.values()]
            pygame.draw.polygon(self.screen, (0, 0, 0), boid_points)
            if show_circles:
                pygame.draw.circle(self.screen, (150, 255, 150), boid.position.values(), boid.view_distance, 1)
                pygame.draw.circle(self.screen, (255, 150, 150), boid.position.values(), boid.separation_distance, 1)
            # pygame.draw.line(self.screen, (255, 0, 0), boid.center, boid.center + boid.direction)
            # pygame.draw.line(self.screen, (0, 255, 0), boid.center, boid.center - boid.direction)
            # pygame.draw.line(self.screen, (0, 0, 0), boid.center + boid.direction, boid.center - boid.direction)
    
    def draw(self, boids):
        self.draw_background()
        self.draw_boids(boids)