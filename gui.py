import pygame
from pygame.locals import *
import math
from pygame.math import Vector2 as Vector

    
def get_offset_rect(rect, offset):
    """This returns a rect that is offset from the original rect.
    It's useful for scrolling items up and down."""

    return pygame.Rect(rect.left + offset.x, rect.top + offset.y,
                        rect.width, rect.height)


class Sidebar:
    """This is the entire bar on the side that contains all of the gui elements."""

    def __init__(self, screen, width, margins, settings, default_setting, bg_color=(100, 100, 100),
                 scrollbar_shade=(150, 150, 150), text_color=(0, 0, 0), slider_color=(150, 150, 150)):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.width = width # The width of the sidebar
        self.rect = pygame.Rect(self.screen_width - width, 0, width, self.screen_height)
        self.margins = margins # Margins to pad the sidebar elements
        self.settings = settings
        self.default_settings = default_setting
        self.bg_color = bg_color
        self.scrollbar_shade_color = scrollbar_shade
        self.text_color = text_color
        self.slider_color = slider_color
        self.font_name = "calibri"
        self.setting_list = []
        self.scroll_y = 0
        self.max_scroll = 0
        self.bar_height = self.screen_height
        self.scroll_speed = 1
        self.bar_rect = pygame.Rect(self.screen_width - 10, 0, 10, self.bar_height)
        self.last_scroll_pos = None
        self.selected_textbox = None
        self.selected_slider = None
        self.last_slider_pos = None
    
    def calculate_scrollbar_props(self):
        """Calculates the height of the bar and how fast the sidebar scrolls as you move it."""

        full_height = self.rect.height
        scroll_percent = -self.max_scroll / full_height
        # If the bar contents are more than the height of the window
        # itself, we can't shrink the scrollbar any more.
        # Instead, change the speed that the scrollbar moves
        if scroll_percent > 0.99: # Change speed
            self.bar_height = 30
            self.scroll_speed = (full_height - self.bar_height) / -self.max_scroll 
        else:
            self.bar_height = math.ceil(full_height - -self.max_scroll)
            self.scroll_speed = 1
    
    def get_scrollbar_pos(self):
        """Returns the rect of the scrollbar at the correct scroll position."""

        return pygame.Rect(self.rect.right - 10, self.rect.top + -self.scroll_y * self.scroll_speed, 10, self.bar_height)
    
    def add_setting(self, setting_name):
        """Add a setting to the sidebar."""

        value, min_value, max_value = self.settings[setting_name].values()

        # Find the y position to place the setting
        bot_of_last_setting = self.margins[1]
        for setting in self.setting_list:
            bot_of_last_setting += setting.height
        
        setting = Setting(setting_name, self.settings, self.default_settings, self.font_name, value, min_value, max_value,
                        Vector(self.screen_width - self.width + self.margins[0], bot_of_last_setting),
                        text_color=self.text_color, slider_color=self.slider_color,
                        shade_color=self.scrollbar_shade_color)
        self.setting_list.append(setting)
        self.max_scroll -= setting.height
        self.calculate_scrollbar_props() # Adjust the scrollbar
    
    def scroll(self, amount):
        """Called when scrolling the mouse."""
        
        self.scroll_y += amount
        # Prevent scrolling beyond bounds
        self.scroll_y = max(self.max_scroll, min(0, self.scroll_y))
    
    def draw_scrollbar(self):
        """Draws the scrollbar and the scrollbar groove."""

        pygame.draw.rect(self.screen, self.scrollbar_shade_color,
                         (self.rect.right - 10, self.rect.top, 10, self.rect.height), border_radius=20)
        pygame.draw.rect(self.screen, self.bg_color,
                         self.get_scrollbar_pos(), border_radius=20)
        pygame.draw.rect(self.screen, self.scrollbar_shade_color,
                         self.get_scrollbar_pos(), 1, border_radius=20)
    
    def draw(self):
        """Draws the sidebar and all its setting elements on the right."""

        if self.last_scroll_pos != None: # Scrollbar is currently being dragged
            mouse_pos = pygame.mouse.get_pos()
            self.scroll(self.last_scroll_pos[1] - mouse_pos[1]) # Move scrollbar to new position
            self.last_scroll_pos = mouse_pos
        
        # Sidebar background
        width, height = self.screen.get_size()
        pygame.draw.rect(self.screen, self.bg_color, (width - self.width, 0, self.width, height),
                         border_top_left_radius=15, border_bottom_left_radius=15)

        # Draw settings
        for setting in self.setting_list:
            setting.draw(self.screen, self.scroll_y)
        
        self.draw_scrollbar()
        # Black outline
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1, border_top_left_radius=15, border_bottom_left_radius=15)
    
    def overlaps(self, rect, mouse_pos):
        """Used for checking if mouse events overlap UI elements."""

        # Move the element rect by the scroll amount
        offset_rect = get_offset_rect(rect, Vector(0, self.scroll_y))
        return offset_rect.collidepoint(mouse_pos)

    def check_event(self, event):
        """Handle any mouse events that occured within the sidebar."""

        if event.type == MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()): # Overlaps sidebar, so allow it to scroll
                self.scroll(event.y * 10)

        elif event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]: # Left button pressed
                mouse_pos = pygame.mouse.get_pos()
                if self.get_scrollbar_pos().collidepoint(mouse_pos): # Clicked the scrollbar
                    self.last_scroll_pos = mouse_pos # Begin tracking dragged scrollbar
                else:
                    self.last_scroll_pos = None # De-select scrollbar
                
                self.selected_textbox = None
                self.selected_slider = None
                for setting in self.setting_list:
                    if self.overlaps(setting.textbox.rect, mouse_pos):
                        self.selected_textbox = setting.textbox # Selected a textbox
                        if setting.textbox.selected:
                             # Second time clicking the textbox, so remove highlight of text
                             setting.textbox.highlighted = False
                        else:
                            # First click, so select and highlight
                            setting.textbox.selected = True
                            setting.textbox.highlighted = True
                    elif self.overlaps(Rect(setting.slider.rect.left - 5,
                                              setting.slider.rect.top,
                                              setting.slider.rect.width + 10,
                                              setting.slider.rect.height),
                                        mouse_pos):
                        setting.textbox.selected = False
                        setting.textbox.highlighted = False
                        self.selected_slider = setting.slider # Selected a slider
                        self.last_slider_pos = mouse_pos
                    elif self.overlaps(setting.button.rect, mouse_pos):
                        button = setting.button
                        if button.active:
                            # Set the current setting value to the default
                            self.settings[setting.name]["value"] = self.default_settings[setting.name]["value"]
                            setting.textbox.set_value(str(self.settings[setting.name]["value"]))
                            setting.textbox.apply_value(self.settings)
                            button.active = False
                    else:
                        if setting.textbox.selected:
                            # User clicked outside textbox, so apply the input value
                            setting.textbox.apply_value(self.settings)
                        
                        setting.textbox.selected = False
                        setting.textbox.highlighted = False
        
        elif event.type == MOUSEBUTTONUP:
            # Release the slider/scrollbar
            self.last_scroll_pos = None
            self.selected_slider = None

        elif event.type == MOUSEMOTION:
            if self.selected_slider:
                # Update the value in real time
                self.selected_slider.update_pos(pygame.mouse.get_pos())
                self.selected_slider.apply_value(self.settings) # Apply settings in real time
        
        elif event.type == KEYDOWN:
            if self.selected_textbox != None:
                # Textbox selected, so check for user inputing values
                if event.key == K_RETURN:
                    self.selected_textbox.apply_value(self.settings)
                    self.selected_textbox.highlighted = False
                    self.selected_textbox.selected = False
                    self.selected_textbox = None
                elif event.key == K_RIGHT:
                    self.selected_textbox.highlighted = False
                else:
                    self.selected_textbox.check_typing_event(event) # Check it's a valid key


class Setting:
    """A sidebar element consisting of a title, textbox, and slider."""

    def __init__(self, name, settings, default_settings, font_name, value, min_value, max_value, top_left, text_color, slider_color, shade_color):
        self.name = name
        self.settings = settings
        self.default_settings = default_settings
        self.font_name = font_name
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.top_left = top_left
        self.text_color = text_color
        self.slider_color = slider_color
        self.shade_color = shade_color
        self.title = None
        self.textbox = None
        self.slider = None
        self.button = None
        self.create_title(top_left)
        self.create_textbox(top_left + Vector(0, self.title.rect.height + 2))
        self.create_slider(top_left + Vector(0, self.title.rect.height + self.textbox.rect.height + 4))
        self.create_button()
        setting_y_margins = 15 # Spacing between each setting
        self.height = setting_y_margins * 2 + self.title.rect.height + self.textbox.rect.height + 4
    
    def create_title(self, top_left):
        """Creates the setting name text at the top of the setting."""

        title = Text(self.name.capitalize(), self.font_name, 15, self.text_color, top_left)
        self.title = title
    
    def create_textbox(self, top_left):
        """Creates a textbox below the title for editing the setting value."""

        textbox = TextBox(self, str(self.value), self.font_name, 150, 15, top_left, self.text_color)
        self.textbox = textbox
    
    def create_slider(self, top_left):
        """Creates a slider below the textbox for quickly editing the setting value."""
        
        slider = Slider(self, self.value, self.min_value, self.max_value, 150, 20, top_left, self.slider_color, self.shade_color)
        self.slider = slider
    
    def create_button(self):
        x, y = self.textbox.rect.midright
        button = Button(self, self.font_name, 70, 15, (x + 3, y), self.text_color, self.slider_color, self.get_accents(self.slider_color))
        self.button = button
    
    def get_accents(self, color):
        def reduce(c):
            return max(c - 30, 0)

        def increase(c):
            return min(c + 30, 255)

        return [tuple([reduce(c) for c in color]), tuple([increase(c) for c in color])]

    def update_button(self):
        if self.settings[self.name]["value"] == self.default_settings[self.name]["value"]:
            self.button.active = False
        else:
            self.button.active = True
    
    def draw(self, screen, offset_y):
        self.title.draw(screen, Vector(0, offset_y))
        self.textbox.draw(screen, Vector(0, offset_y))
        self.slider.draw(screen, Vector(0, offset_y))
        self.button.draw(screen, Vector(0, offset_y))


class Button:
    """This is for a button that returns the value back to the default."""

    def __init__(self, parent, font_name, width, height, mid_left, text_color, button_color, button_accents):
        self.parent = parent
        self.font_name = font_name
        self.width = width
        self.height = height
        self.mid_left = mid_left
        self.text_color = text_color
        self.button_color = button_color
        self.button_accents = button_accents
        self.rect = Rect(0, 0, width, height)
        self.rect.midleft = mid_left
        self.text = Text("Default", font_name, height, text_color, self.rect.topleft)
        self.text.rect.center = self.rect.center
        self.active = False
    
    def draw(self, screen, offset=Vector(0, 0)):
        """Draws the button to the screen."""

        new_rect = get_offset_rect(self.rect, offset)
        if self.active:
            self.text.set_color(self.text_color)
            pygame.draw.rect(screen, self.button_accents[1], (new_rect.left, new_rect.top, new_rect.width - 2, new_rect.height - 2), border_radius=2)
            pygame.draw.rect(screen, self.button_accents[0], (new_rect.left + 2, new_rect.top + 2, new_rect.width - 2, new_rect.height - 2), border_radius=2)
        else:
            self.text.set_color(tuple([c + 50 for c in self.text_color]))
            pygame.draw.rect(screen, self.button_accents[0], (new_rect.left, new_rect.top, new_rect.width - 2, new_rect.height - 2), border_radius=2)
            pygame.draw.rect(screen, self.button_accents[1], (new_rect.left + 2, new_rect.top + 2, new_rect.width - 2, new_rect.height - 2), border_radius=2)
        
        pygame.draw.rect(screen, self.button_color, (new_rect.left + 2, new_rect.top + 2, new_rect.width - 4, new_rect.height - 4), border_radius=2)
        
        self.text.draw(screen, offset)
        # if self.active:
        #     pygame.draw.rect(screen, self.button_accents[0], new_rect, 1, 2)
        # else:
        #     pygame.draw.rect(screen, self.button_accents[1], new_rect, 1, 2)


class TextBox:
    """This creates an editable box where a user can select the box and type
    whatever number value they want."""

    def __init__(self, parent, value, font_name, width, height, top_left, text_color):
        self.parent = parent # Links to parent Setting so the textbox can affect the slider
        self.value = value
        self.text = Text(str(value), font_name, height, text_color, top_left)
        self.width = width
        self.height = height
        self.top_left = top_left
        self.selected = False
        self.highlighted = False
        self.rect = pygame.Rect(list(top_left), (width, height))
    
    def set_value(self, value):
        """Changes the text value, then makes sure it can fit all characters in the textbox."""

        self.text.set_text(value)
        if self.text.rect.width > self.rect.width:
            self.text.set_text(self.value)
        else:
            self.value = value
    
    def apply_value(self, settings):
        """This function is used when the user enters the value. It will
        then change send its value to the slider/settings."""

        self.value = self.value or "0"
        value = float(self.value) or 0.0 # Default the value to 0 if there's no value
        setting = settings[self.parent.name]
        setting["value"] = min(setting["max"], max(setting["min"], value)) # Make sure within bounds
        if setting["value"] == int(setting["value"]): # Doesn't need to show decimals
            self.set_value(str(int(setting["value"])))
        else:
            self.set_value(str(setting["value"]))
        
        self.parent.slider.set_value(setting["value"])
        self.parent.update_button()
    
    def check_typing_event(self, event):
        """This will edit the value based on values typed."""

        if event.key == K_BACKSPACE:
            if self.value:
                if self.highlighted: # Delete all text
                    self.set_value("")
                    self.highlighted = False
                else:
                    self.set_value(self.value[:-1]) # Only delete one char
        
        # Checks if number or - or . and in the right context
        elif event.dict["unicode"].isdigit() or \
                (event.dict["unicode"] == "." and "." not in self.value) or \
                ((self.value == "" or self.highlighted) and event.dict["unicode"] == "-"):

            if self.highlighted:
                # Replace the previous value with the input char
                self.set_value(event.dict["unicode"])
                self.highlighted = False
            else:
                self.set_value(self.value + event.dict["unicode"])
    
    def draw(self, screen, offset=Vector(0, 0)):
        """Creates the bounding box and shows the text."""

        rect = get_offset_rect(self.rect, offset)
        if self.selected:
            # Make the background white
            pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=5)
        else:
            # Make the background more gray
            pygame.draw.rect(screen, (225, 225, 225), rect, border_radius=5)
        
        if self.highlighted:
            # Create a blue highlight border around the text
            text_rect = get_offset_rect(self.text.rect, offset)
            text_rect.width += 5
            pygame.draw.rect(screen, (50, 100, 212), text_rect, border_radius=5)
        
        if not self.selected:
            pygame.draw.rect(screen, (150, 150, 150), rect, 1, border_radius=5)
        else:
            pygame.draw.rect(screen, (0, 0, 0), rect, 1, border_radius=5)
            if not self.highlighted:
                # Draw a cursor for more intuitive user experience
                line_rect = get_offset_rect(self.text.rect, offset + Vector(3, 0))
                pygame.draw.line(screen, (0, 0, 0), (line_rect.right, line_rect.top), (line_rect.right, line_rect.bottom))
        
        self.text.draw(screen, Vector(offset.x + 3, offset.y))


class Slider:
    """A slider that allows the user to set a value between two values by moving the slider."""

    def __init__(self, parent, value, min_val, max_val, width, height, top_left, slider_color, text_color):
        self.parent = parent # Link to the parent setting for changing the settings and textbox
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.width = width
        self.height = height
        self.top_left = top_left
        self.slider_color = slider_color
        self.accents = self.get_accents(self.slider_color)
        self.slide_line_color = text_color
        self.rect = Rect(top_left.x, top_left.y, width, height)
        self.ratio = self.get_ratio() # The pixel to value ratio
    
    def get_accents(self, color):
        def reduce(c):
            return max(c - 30, 0)

        def increase(c):
            return min(c + 30, 255)

        return [tuple([reduce(c) for c in color]), tuple([increase(c) for c in color])]
    
    def get_ratio(self):
        """Based on the value range, get the ratio of value change per pixel change."""

        val_range = self.max_val - self.min_val
        ratio = self.width / val_range
        return ratio
    
    def set_value(self, value):
        """Sets the value within the bounds."""

        value = min(self.max_val, max(self.min_val, value))
        self.value = value
    
    def apply_value(self, settings):
        """Changes the settings and also the textbox value."""

        setting = settings[self.parent.name]
        setting["value"] = round(self.value, 4)
        self.parent.textbox.set_value(str(setting["value"]))
        self.parent.update_button()
    
    def update_pos(self, pos):
        """Moves the slider to the correct x position and sets the value based on the position."""

        x_pos = max(self.rect.left, min(self.rect.right, pos[0])) # Make sure the mouse is within the bounds
        if pos[0] >= self.rect.right:
            # Makes sure the maximum value can be reached rather than being a decimal off
            self.set_value(self.max_val)
            return
        
        # The pixel representation of the value
        x_length = x_pos - self.rect.left
        # Get value based on pixel length
        value = x_length / self.ratio
        self.set_value(value)
    
    def draw(self, screen, offset=Vector(0, 0)):
        """Draw the slider at the position based off its value."""

        rect = get_offset_rect(self.rect, offset)
        pygame.draw.line(screen, self.slide_line_color, rect.midleft, rect.midright)
        pygame.draw.line(screen, self.accents[1], (rect.midleft[0], rect.midleft[1] + 1), (rect.midright[0], rect.midright[1] + 1))
        x_pos = rect.left + (self.value - self.min_val) * self.ratio
        pygame.draw.rect(screen, self.accents[0], (x_pos - 5, rect.top, 10, self.height))
        pygame.draw.rect(screen, self.accents[1], (x_pos - 2, rect.top, 8, self.height - 2))
        pygame.draw.rect(screen, self.slider_color, (x_pos - 2, rect.top + 2, 6, self.height - 4))


class Text:
    """A text GUI element that can be positioned on the screen to show any text."""

    def __init__(self, text, font_name, size, color, top_left):
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.font = pygame.font.SysFont(self.font_name, self.size, True) # The font_name is the string name of a built-in font
        self.surf = None
        self.top_left = top_left
        self.rect = None
        self.create_surf() # Pre-renders the text so it can simply be placed on the screen each time
    
    def create_surf(self):
        """This function pre-renders the given text/font and finds its rect bounds
        so these are not calculated each time. They can simply be blit."""

        self.render()
        self.rect = self.surf.get_rect()
        self.rect.topleft = list(self.top_left)
    
    def render(self):
        self.surf = self.font.render(self.text, False, self.color)
    
    def set_color(self, color):
        self.color = color
        self.render()
    
    def draw(self, screen, offset=Vector(0, 0)):
        """Blits the rendered text to the screen at the position of rect."""
        
        if not self.text:
            return # Skips trying to display if there isn't any text to display
        
        if list(offset) == (0, 0):
            screen.blit(self.surf, self.rect)
        else:
            screen.blit(self.surf, get_offset_rect(self.rect, offset))
    
    def set_text(self, text):
        """Changes the text value and then renders the text again."""

        self.text = text
        if self.text:
            self.create_surf()