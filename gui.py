import pygame
import math
from vector import Vector

class Anchor:
    def __init__(self, anchor_point_string, pos):
        self.anchor_point_string = anchor_point_string
        self.pos = pos
    
    def anchor_rect(self, rect):
        if self.anchor_point_string == "center":
            rect.center = self.pos
        elif self.anchor_point_string == "left top":
            rect.topleft = self.pos
        elif self.anchor_point_string == "right top":
            rect.topright = self.pos
        elif self.anchor_point_string == "left bottom":
            rect.botleft = self.pos
        elif self.anchor_point_string == "right bottom":
            rect.botright = self.pos
        elif self.anchor_point_string == "center top":
            rect.midtop = self.pos
        elif self.anchor_point_string == "center bottom":
            rect.midbottom = self.pos

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
        self.anchor.anchor_rect(self.rect)
    
    def get_offset_rect(self, offset_amount):
        return pygame.Rect(self.rect.left + offset_amount[0], self.rect.top + offset_amount[1],
                           self.rect.width, self.rect.height)
    
    def render(self, screen, offset=(0, 0)):
        if not self.text:
            raise RuntimeError("Text object has no text to display.")
        
        if offset == (0, 0):
            screen.blit(self.surf, self.rect)
        else:
            screen.blit(self.surf, self.get_offset_rect(offset))
    
    def set_text(self, text):
        self.text = text
        if self.text:
            self.create_surf()


class Property:
    def __init__(self, name, font_name, value, min_value, max_value, place_top, margin):
        self.name = name
        self.font_name = font_name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.margin = margin
        self.title = None
        self.create_title(place_top + Vector(0, margin))
        self.height = margin * 2 + self.title.rect.height
    
    def create_title(self, place_top):
        title = Text(self.name, self.font_name, 15, (0, 0, 0), Anchor("center top", place_top.values()))
        self.title = title
    
    def draw(self, screen, offset_y):
        self.title.render(screen, (0, offset_y))


class Sidebar:
    def __init__(self, screen, width, prop_margin, settings):
        self.screen = screen
        self.s_width = screen.get_width()
        self.s_height = screen.get_height()
        self.width = width
        self.rect = pygame.Rect(self.s_width - width, 0, width, self.s_height)
        self.prop_margin = prop_margin
        self.settings = settings
        self.font_name = "calibri"
        self.properties = []
        self.scroll_y = 0
        self.max_scroll = 0
    
    def add_property(self, property_name):
        value, min_value, max_value = self.settings[property_name].values()

        bot_of_last_prop = 0
        for prop in self.properties:
            bot_of_last_prop += prop.height
        
        prop = Property(property_name, self.font_name, value, min_value, max_value,
                        Vector(self.rect.centerx, bot_of_last_prop), self.prop_margin)
        self.properties.append(prop)
        self.max_scroll -= prop.height
    
    def scroll(self, amount):
        self.scroll_y += amount
        self.scroll_y = max(self.max_scroll, min(0, self.scroll_y))
    
    def draw_scrollbar(self):
        full_height = self.rect.height
        scroll_percent = -self.max_scroll / full_height
        if scroll_percent > 0.99:
            bar_height = 30
            scroll_speed = (full_height - bar_height) / -self.max_scroll 
        else:
            bar_height = math.ceil(full_height - -self.max_scroll)
            scroll_speed = 1
        
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.rect.right - 10, self.rect.top, 10, self.rect.height), border_radius=20)
        pygame.draw.rect(self.screen, (150, 150, 150),
                         (self.rect.right - 10, self.rect.top + -self.scroll_y * scroll_speed, 10, bar_height), border_radius=20)
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.rect.right - 10, self.rect.top + -self.scroll_y * scroll_speed, 10, bar_height), 1, border_radius=20)
    
    def draw(self):
        width, height = self.screen.get_size()
        pygame.draw.rect(self.screen, (200, 200, 200), (width - self.width, 0, self.width, height),
                         border_top_left_radius=15, border_bottom_left_radius=15)

        for prop in self.properties:
            prop.draw(self.screen, self.scroll_y)
        
        self.draw_scrollbar()
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1, border_top_left_radius=15, border_bottom_left_radius=15)
