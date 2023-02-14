import pygame

class Canvas:
    def __init__(self, screen, bg_color):
        self.screen = screen
        self.bg_color = bg_color
        self.width = screen.get_width()
        self.height = screen.get_height()
    
    def draw_background(self):
        self.screen.fill(self.bg_color)
    
    def draw_boids(self, boids):
        pass
    
    def draw(self, boids):
        self.draw_background()
        self.draw_boids(boids)