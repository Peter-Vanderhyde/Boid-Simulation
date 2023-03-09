import pygame
import sys
from vector import Vector

class Canvas:
    """This class takes care of drawing the window, drawing the boids, and handling window events."""

    def __init__(self, width, height, bg_color, show_circles=False):
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN) # Create window
        self.bg_color = bg_color
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.show_circles = show_circles
    
    def draw_background(self, active_area):
        """Fills the screen with the background color and draws a square for the active area."""

        self.screen.fill(self.bg_color)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(active_area[0], active_area[1]), 1)
    
    def draw_boids(self, boids, size):
        """Draws the boid polygons."""

        for boid in boids:
            if boid.velocity.length() == 0:
                direction = Vector(0, 1)
            else:
                direction = boid.velocity.normalize()
            
            perpendicular = Vector(direction.y, -direction.x)
            perpendicular /= 2
            point_1 = boid.position + direction * size
            point_2 = boid.position - direction * size + perpendicular * size
            point_3 = boid.position - direction * size - perpendicular * size
            boid_points = [point_1.values(),
                            point_2.values(),
                            point_3.values()]
            pygame.draw.polygon(self.screen, boid.color, boid_points)

            if self.show_circles:
                # Show view range circles around the boids
                pygame.draw.circle(self.screen, (150, 255, 150), boid.position.values(), boid.view_distance, 1)
                pygame.draw.circle(self.screen, (255, 150, 150), boid.position.values(), boid.separation_distance, 1)
    
    def get_events(self):
        """Check every window event."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    self.show_circles = not self.show_circles # Show view circles around boids