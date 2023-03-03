import random
import sys
import math
import pygame
from pygame.locals import *
from canvas import Canvas
from boid import Boid
from vector import Vector
import simulation
import time

VIEW_DISTANCE = 40
SEPARATION_DISTANCE = 8


def create_boids(num_of_boids, width, height):
    """Randomly places boids on the screen and returns a list of the created line objects."""

    boids = []
    for i in range(num_of_boids):
        x, y = random.randint(0, width), random.randint(0, height)
        center = Vector(x, y)
        velocity = Vector(random.random(), random.random()).normalize() * random.randint(2, 3)
        boid = Boid(center, velocity, 3, 2, VIEW_DISTANCE, SEPARATION_DISTANCE)
        boids.append(boid)
    
    return boids


def main(width, height):
    FPS = 60
    clock = pygame.time.Clock()
    last_time = time.time()
    screen = pygame.display.set_mode((width, height))
    canvas = Canvas(screen, (255, 255, 255))
    active_area = ((100, 100),
                   width - 200,
                   height - 200)
    boids = create_boids(20, canvas.width, canvas.height)

    while True:
        dt = time.time() - last_time
        last_time = time.time()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        simulation.simulate(dt, boids, active_area)
        
        canvas.draw_background(active_area)
        canvas.draw_boids(boids)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    # args = sys.argv
    # if len(args) < 3:
    #     raise RuntimeError("Main file execution requires command line arguments: <main_filename> <window_width> <window_height>")
    # else:
    #     WIDTH, HEIGHT = args[-2], args[-1]
    WIDTH, HEIGHT = 1280, 720

    main(WIDTH, HEIGHT)