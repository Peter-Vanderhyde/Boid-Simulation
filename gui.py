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
    def __init__(self, font_name, size, color, anchor=Anchor("top left", (0, 0))):
        self.font_name = font_name
        self.size = size
        self.color = color
        self.text = ""
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.surf = None
        self.rect = None
        self.anchor = anchor
        self.create_surf()
    
    def create_surf(self):
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect()
        self.anchor.move_rect(self.rect)
    
    def render(self, screen):
        screen.blit(self.surf, self.rect)
    
    def set_text(self, text):
        self.text = text
        self.create_surf()


class Property:
    def __init__(self, name, value, min_value, max_value):
        self.name = name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.text = None


class Sidebar:
    def __init__(self, screen, width):
        self.screen = screen
        self.s_width = screen.get_width()
        self.s_height = screen.get_height()
        self.width = width
        self.properties = []
    
    def draw(self):
        width, height = self.screen.get_size()
        pygame.draw.rect(self.screen, (200, 200, 200), (width - self.width, 0, self.width, height))
