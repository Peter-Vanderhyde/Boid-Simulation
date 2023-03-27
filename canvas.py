import pygame
import sys
from vector import Vector
import gui

class Canvas:
    """This class takes care of drawing the window, drawing the boids, and handling window events."""

    def __init__(self, width, height, bg_color, settings):
        self.screen = pygame.display.set_mode((width, height)) # Create window
        self.bg_color = bg_color
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.sidebar = None

        margin = settings["margin"]["value"]
        # Create rectangle area the boids will try to stay within
        # ((corner_x, corner_y), (width, height))
        self.active_area = ((margin, margin),
                    (self.width - margin * 2, self.height - margin * 2))

        self.settings = settings
        self.show_circles = False
        self.last_scroll_pos = None
        self.selected_textbox = None
    
    def create_sidebar(self, width, margins=(0, 0)):
        self.sidebar = gui.Sidebar(self.screen, width, margins, self.settings)
        margin = self.active_area[0][0]
        self.active_area = ((margin, margin),
                    (self.width - width - margin * 2, self.height - margin * 2))
    
    def draw(self, boids):
        self.draw_background()
        self.draw_boids(boids)
        if self.sidebar:
            mouse_pos = pygame.mouse.get_pos()
            self.sidebar.draw(mouse_pos, self.last_scroll_pos)
            if self.last_scroll_pos != None:
                self.last_scroll_pos = mouse_pos
    
    def draw_background(self):
        """Fills the screen with the background color and draws a square for the active area."""

        self.screen.fill(self.bg_color)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.active_area[0], self.active_area[1]), 1)
    
    def draw_boids(self, boids):
        """Draws the boid polygons."""

        size = self.settings["boid size"]["value"]
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
                pygame.draw.circle(self.screen, (150, 255, 150), boid.position.values(), self.settings["view distance"]["value"], 1)
                pygame.draw.circle(self.screen, (255, 150, 150), boid.position.values(), self.settings["separation distance"]["value"], 1)
    
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
            
            elif event.type == pygame.MOUSEWHEEL:
                if self.sidebar.rect.collidepoint(pygame.mouse.get_pos()):
                    self.sidebar.scroll(event.y * 10)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.sidebar.get_scrollbar_pos().collidepoint(mouse_pos):
                    self.last_scroll_pos = mouse_pos
                else:
                    self.last_scroll_pos = None
                
                self.selected_textbox = None
                for prop in self.sidebar.properties:
                    if prop.textbox.rect.collidepoint(mouse_pos):
                        self.selected_textbox = prop
                        prop.textbox.selected = True
                
                for prop in self.sidebar.properties:
                    if prop is not self.selected_textbox:
                        prop.textbox.selected = False
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.last_scroll_pos = None