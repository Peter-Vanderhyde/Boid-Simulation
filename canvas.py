import pygame
import sys
from pygame.math import Vector2 as Vector
import gui
import repel

class Canvas:
    """This class takes care of drawing the window, drawing the boids, and handling window events."""

    def __init__(self, width, height, bg_color, settings, default_settings):
        pygame.display.set_caption("Boid Simulation")
        self.screen = pygame.display.set_mode((width, height)) # Create window
        self.bg_color = bg_color
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.sidebar = None

        margin = 100 # The margin around the active simulation area where the boids will turn around

        # Create rectangle area the boids will try to stay within
        # ((corner_x, corner_y), (width, height))
        self.active_area = ((margin, margin),
                    (self.width - margin * 2, self.height - margin * 2))

        self.settings = settings
        self.default_settings = default_settings
        self.zones = []
        self.tree = None
        self.show_circles = False
        self.show_grid = False
        self.show_zones = True
        self.placing_zone = False
        # Info that is displayed in the top left of the screen
        self.infos = self.create_info(["Tab - Toggle vision and separation visibility",
                                       "G - Toggle quad tree visibility",
                                       "Z - Toggle zone creation",
                                       "  > Click to place and scroll to resize",
                                       "Delete - Delete all placed zones",
                                       "Ctrl Z - Toggle zone visibility"],
                                     "calibri",
                                     15,
                                     (255, 255, 255))
    
    def create_sidebar(self, width, margins=(0, 0), bg_color=(100, 100, 100), text_color=(0, 0, 0), slider_color=(150, 150, 150)):
        """This function creates the sidebar based on the passed in properties."""

        def create_accent(color):
            # Returns a darkened color that is valid
            return [max(rgb - 30, 0) for rgb in color]
        
        self.sidebar = gui.Sidebar(self.screen, width, margins, self.settings, self.default_settings,
                                   bg_color=bg_color,
                                   scrollbar_shade=(create_accent(bg_color)),
                                   text_color=text_color,
                                   slider_color=slider_color)
        margin = self.active_area[0][0]
        # Remake the simulation zone to account for sidebar taking up space
        self.active_area = ((margin, margin),
                    (self.width - width - margin * 2, self.height - margin * 2))
    
    def create_info(self, info_texts, font_name, size, color):
        """This creates and positions text in the top left of the window."""

        infos = []
        for index, text in enumerate(info_texts):
            # Stacks the text
            infos.append(gui.Text(text, font_name, size, color, Vector(5, 5 + size * index)))
        
        return infos
    
    def draw(self, boids):
        """This draws each element of the window in order."""

        self.draw_background()
        if self.show_zones:
            for zone in self.zones:
                zone.draw()
        elif self.placing_zone:
            self.zones[-1].draw()
        
        self.draw_boids(boids)
        if self.sidebar:
            self.sidebar.draw()
        
        self.draw_info()
    
    def draw_background(self):
        """Fills the screen with the background color and draws a square for the active area.
        It also draws the grid of the quad tree if toggled to visible."""

        self.screen.fill(self.bg_color)
        if self.show_grid:
            self.tree.draw_grid(self.screen)
            pygame.draw.rect(self.screen, (200, 0, 0), pygame.Rect(self.active_area[0], self.active_area[1]), 1)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.active_area[0], self.active_area[1]), 1)
    
    def draw_boids(self, boids):
        """Draws the boid polygons."""

        size = self.settings["boid size"]["value"]
        for boid in boids:
            if boid.velocity.length() == 0: # It has no direction to point
                direction = Vector(0, 1)
            else:
                direction = boid.velocity.normalize()
            
            perpendicular = Vector(direction.y, -direction.x)
            perpendicular /= 2
            # Calculate polygon positions
            point_1 = boid.position + direction * size
            point_2 = boid.position - direction * size + perpendicular * size
            point_3 = boid.position - direction * size - perpendicular * size
            boid_points = [list(point_1),
                            list(point_2),
                            list(point_3)]
            pygame.draw.polygon(self.screen, boid.color, boid_points)

            if self.show_circles:
                # Show view range circles around the boids
                pygame.draw.circle(self.screen, (150, 255, 150), list(boid.position), self.settings["view distance"]["value"], 1)
                pygame.draw.circle(self.screen, (255, 150, 150), list(boid.position), self.settings["separation distance"]["value"], 1)
    
    def draw_info(self):
        """Draws the text in the top left of the screen."""

        for info in self.infos:
            info.draw(self.screen)
    
    def get_events(self):
        """Check every window event."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEMOTION:
                if self.placing_zone:
                    self.zones[-1].position = Vector(pygame.mouse.get_pos())
            
            elif event.type == pygame.MOUSEWHEEL:
                    if self.placing_zone and not self.sidebar.rect.collidepoint(pygame.mouse.get_pos()):
                        self.zones[-1].radius = max(self.zones[-1].radius - event.y, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Make sure they are trying to place a zone and not clicking a UI element
                if pygame.mouse.get_pressed()[0] == 1 and self.placing_zone and not self.sidebar.rect.collidepoint(pygame.mouse.get_pos()):
                    self.zones[-1].placed = True
                    self.placing_zone = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_TAB:
                    # Show view circles around boids
                    self.show_circles = not self.show_circles
                elif event.key == pygame.K_g:
                    # Display the nodes of the quad tree
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_z and pygame.key.get_mods() and pygame.KMOD_CTRL:
                    self.show_zones = not self.show_zones
                elif event.key == pygame.K_z:
                    if not self.placing_zone:
                        self.placing_zone = True
                        zone = repel.NoGoZone(Vector(pygame.mouse.get_pos()), 50, self.screen)
                        self.zones.append(zone)
                    else:
                        self.placing_zone = False
                        self.zones.pop()
                elif event.key == pygame.K_DELETE:
                    if self.placing_zone:
                        self.zones = [self.zones[-1]]
                    else:
                        self.zones = []
            
            # Check for events that apply to the UI elements
            self.sidebar.check_event(event)