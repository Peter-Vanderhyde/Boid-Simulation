import pygame


class Anchor:
    def __init__(self, anchor_point_string, pos):
        self.anchor_point_string = anchor_point_string
        self.pos = pos
    
    def move_rect(self, rect):
        if self.anchor_point_string == "center":
            rect.center = self.pos
        elif self.anchor_point_string == "top left":
            rect.topleft = self.pos
        elif self.anchor_point_string == "top right":
            rect.topright = self.pos
        elif self.anchor_point_string == "bottom left":
            rect.botleft = self.pos
        elif self.anchor_point_string == "bottom right":
            rect.botright = self.pos

class Text:
    def __init__(self, text, font_name, size, color, anchor=Anchor("top left", (0, 0))):
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.size, True)
        self.surf = None
        self.rect = None
        self.anchor = anchor
        if self.text:
            self.create_surf()
    
    def create_surf(self):
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect()
        self.anchor.move_rect(self.rect)
    
    def render(self, screen):
        if not self.text:
            raise RuntimeError("Text object has no text to display.")
        screen.blit(self.surf, self.rect)
    
    def set_text(self, text):
        self.text = text
        if self.text:
            self.create_surf()


class Property:
    def __init__(self, name, font_name, value, min_value, max_value, sidebar_rect):
        self.name = name
        self.font_name = font_name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.title = None
        self.create_title(sidebar_rect)
    
    def create_title(self, sidebar_rect):
        title = Text(self.name, self.font_name, 15, (0, 0, 0), Anchor("center", (sidebar_rect.center[0], 10)))
        self.title = title
    
    def draw(self, screen):
        self.title.render(screen)


class Sidebar:
    def __init__(self, screen, width, settings):
        self.screen = screen
        self.s_width = screen.get_width()
        self.s_height = screen.get_height()
        self.width = width
        self.rect = pygame.Rect(self.s_width - width, 0, width, self.s_height)
        self.settings = settings
        self.font_name = "calibri"
        self.properties = []
    
    def add_property(self, property_name):
        value, min_value, max_value = self.settings[property_name].values()
        prop = Property(property_name, self.font_name, value, min_value, max_value, sidebar_rect=self.rect)
        self.properties.append(prop)
    
    def draw(self):
        width, height = self.screen.get_size()
        pygame.draw.rect(self.screen, (200, 200, 200), (width - self.width, 0, self.width, height), border_top_left_radius=15, border_bottom_left_radius=15)
        for prop in self.properties:
            prop.draw(self.screen)
        
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2, border_top_left_radius=15, border_bottom_left_radius=15)
