import pygame
import math
from vector import Vector

    
def get_offset_rect(rect, offset_amount):
    return pygame.Rect(rect.left + offset_amount[0], rect.top + offset_amount[1],
                        rect.width, rect.height)

class Text:
    def __init__(self, text, font_name, size, color, top_left):
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.size, True)
        self.surf = None
        self.top_left = top_left
        self.rect = None
        self.create_surf()
    
    def create_surf(self):
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect()
        self.rect.topleft = self.top_left.values()
    
    def draw(self, screen, offset=(0, 0)):
        if not self.text:
            return
            #raise RuntimeError("Text object has no text to display.")
        
        if offset == (0, 0):
            screen.blit(self.surf, self.rect)
        else:
            screen.blit(self.surf, get_offset_rect(self.rect, offset))
    
    def set_text(self, text):
        self.text = text
        if self.text:
            self.create_surf()


class TextBox:
    def __init__(self, value, font_name, width, height, top_left):
        self.value = value
        self.text = Text(str(value), font_name, height, (0, 0, 0), top_left)
        self.width = width
        self.height = height
        self.top_left = top_left
        self.selected = False
        self.rect = pygame.Rect(top_left.values(), (width, height))
    
    def set_value(self, value):
        self.value = value
        self.text.set_text(str(value))
    
    def draw(self, screen, offset=(0, 0)):
        rect = get_offset_rect(self.rect, offset)
        pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=5)
        if not self.selected:
            pygame.draw.rect(screen, (150, 150, 150), rect, 1, border_radius=5)
        else:
            pygame.draw.rect(screen, (50, 50, 50), rect, 1, border_radius=5)
        
        self.text.draw(screen, (offset[0] + 3, offset[1]))


class Property:
    def __init__(self, name, font_name, value, min_value, max_value, top_left):
        self.name = name
        self.font_name = font_name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.top_left = top_left
        self.title = None
        self.textbox = None
        self.create_title(top_left)
        self.create_textbox(top_left + Vector(0, self.title.rect.height))
        prop_y_margins = 15
        self.height = prop_y_margins * 2 + self.title.rect.height + self.textbox.rect.height
    
    def create_title(self, top_left):
        title = Text(self.name, self.font_name, 15, (0, 0, 0), top_left)
        self.title = title
    
    def create_textbox(self, top_left):
        textbox = TextBox(self.value, self.font_name, 150, 15, top_left)
        self.textbox = textbox
    
    def draw(self, screen, offset_y):
        self.title.draw(screen, (0, offset_y))
        self.textbox.draw(screen, (0, offset_y))


class Sidebar:
    def __init__(self, screen, width, margins, settings):
        self.screen = screen
        self.s_width = screen.get_width()
        self.s_height = screen.get_height()
        self.width = width
        self.rect = pygame.Rect(self.s_width - width, 0, width, self.s_height)
        self.margins = margins
        self.settings = settings
        self.font_name = "calibri"
        self.properties = []
        self.scroll_y = 0
        self.max_scroll = 0
        self.bar_height = self.s_height
        self.scroll_speed = 1
        self.bar_rect = pygame.Rect(self.s_width - 10, 0, 10, self.bar_height)
        self.last_scroll_pos = None
        self.selected_textbox = None
    
    def calculate_scrollbar_props(self):
        full_height = self.rect.height
        scroll_percent = -self.max_scroll / full_height
        if scroll_percent > 0.99:
            self.bar_height = 30
            self.scroll_speed = (full_height - self.bar_height) / -self.max_scroll 
        else:
            self.bar_height = math.ceil(full_height - -self.max_scroll)
            self.scroll_speed = 1
    
    def get_scrollbar_pos(self):
        return pygame.Rect(self.rect.right - 10, self.rect.top + -self.scroll_y * self.scroll_speed, 10, self.bar_height)
    
    def add_property(self, property_name):
        value, min_value, max_value = self.settings[property_name].values()

        bot_of_last_prop = self.margins[1]
        for prop in self.properties:
            bot_of_last_prop += prop.height
        
        prop = Property(property_name, self.font_name, value, min_value, max_value,
                        Vector(self.s_width - self.width + self.margins[0], bot_of_last_prop))
        self.properties.append(prop)
        self.max_scroll -= prop.height
        self.calculate_scrollbar_props()
    
    def scroll(self, amount):
        self.scroll_y += amount
        self.scroll_y = max(self.max_scroll, min(0, self.scroll_y))
    
    def draw_scrollbar(self):
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (self.rect.right - 10, self.rect.top, 10, self.rect.height), border_radius=20)
        pygame.draw.rect(self.screen, (150, 150, 150),
                         self.get_scrollbar_pos(), border_radius=20)
        pygame.draw.rect(self.screen, (100, 100, 100),
                         self.get_scrollbar_pos(), 1, border_radius=20)
    
    def draw(self):
        if self.last_scroll_pos != None:
            mouse_pos = pygame.mouse.get_pos()
            self.scroll(self.last_scroll_pos[1] - mouse_pos[1])
            self.last_scroll_pos = mouse_pos
        
        width, height = self.screen.get_size()
        pygame.draw.rect(self.screen, (200, 200, 200), (width - self.width, 0, self.width, height),
                         border_top_left_radius=15, border_bottom_left_radius=15)

        for prop in self.properties:
            prop.draw(self.screen, self.scroll_y)
        
        self.draw_scrollbar()
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1, border_top_left_radius=15, border_bottom_left_radius=15)

    def check_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll(event.y * 10)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.get_scrollbar_pos().collidepoint(mouse_pos):
                    self.last_scroll_pos = mouse_pos
                else:
                    self.last_scroll_pos = None
                
                self.selected_textbox = None
                for prop in self.properties:
                    if get_offset_rect(prop.textbox.rect, (0, self.scroll_y)).collidepoint(mouse_pos):
                        self.selected_textbox = prop
                        prop.textbox.selected = True
                    else:
                        prop.textbox.selected = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.last_scroll_pos = None