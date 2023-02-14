import random
import sys
import math
import pygame
from pygame.locals import *
from pygame.math import Vector2
from canvas import Canvas
from boid import Boid


def create_boids(num_of_boids, width, height):
    """Randomly places boids on the screen and returns a list of the created line objects."""

    SIZE = 7
    boids = []
    for i in range(num_of_boids):
        x, y = random.randint(0, width), random.randint(0, height)
        angle = random.randint(0, 360)
        # tip_x = SIZE * math.cos(math.radians(angle))
        # tip_y = SIZE * math.sin(math.radians(angle))
        center = Vector2(x, y)
        boid = Boid(center, angle, SIZE)
        boids.append(boid)
    
    return boids


def main(width, height):
    screen = pygame.display.set_mode((width, height))
    canvas = Canvas(screen, (255, 255, 255))
    boids = create_boids(200, canvas.width, canvas.height)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        canvas.draw(boids)
        pygame.display.update()


if __name__ == "__main__":
    # args = sys.argv
    # if len(args) < 3:
    #     raise RuntimeError("Main file execution requires command line arguments: <main_filename> <window_width> <window_height>")
    # else:
    #     WIDTH, HEIGHT = args[-2], args[-1]
    WIDTH, HEIGHT = 1100, 600

    main(WIDTH, HEIGHT)