import pygame
import sys
from vector import Vector

class Canvas:
    def __init__(self, screen, bg_color, show_circles=False):
        self.screen = screen
        self.bg_color = bg_color
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.show_circles = show_circles
    
    def draw_background(self, active_area):
        self.screen.fill(self.bg_color)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(active_area[0], active_area[1]), 1)
    
    def draw_boids(self, boids, size):
        for boid in boids:
            perpendicular = Vector(boid.velocity.y, -boid.velocity.x).normalize()
            perpendicular /= 2
            point_1 = boid.position + boid.velocity.normalize() * size
            point_2 = boid.position - boid.velocity.normalize() * size + perpendicular * size
            point_3 = boid.position - boid.velocity.normalize() * size - perpendicular * size
            boid_points = [point_1.values(),
                            point_2.values(),
                            point_3.values()]
            pygame.draw.polygon(self.screen, (0, 0, 0), boid_points)
            if self.show_circles:
                pygame.draw.circle(self.screen, (150, 255, 150), boid.position.values(), boid.view_distance, 1)
                pygame.draw.circle(self.screen, (255, 150, 150), boid.position.values(), boid.separation_distance, 1)
    
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    self.show_circles = not self.show_circles