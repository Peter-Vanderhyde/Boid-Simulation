import random
import pygame
from pygame.locals import *
from canvas import Canvas
from boid import Boid
from vector import Vector
import simulation

settings = {
    "view distance": 50,
    "separation distance": 15,
    "minimum speed": 2,
    "maximum speed": 6,
    "centering factor": 0.0005,
    "matching factor": 0.05,
    "avoid factor": 0.05,
    "turn factor": 0.2,
    "margin": 100,
    "boid size": 8
}


def create_boids(width, height, num_of_boids=10):
    """Randomly places boids on the screen and returns a list of the created line objects."""

    boids = []
    for i in range(num_of_boids):
        x, y = random.randint(0, width), random.randint(0, height)
        center = Vector(x, y)
        velocity = Vector(random.random(), random.random()).normalize() * random.randint(settings["minimum speed"], settings["maximum speed"])
        boid = Boid(center, velocity,
                    settings["minimum speed"],
                    settings["maximum speed"],
                    settings["view distance"],
                    settings["separation distance"])
        boids.append(boid)
    
    return boids


def main(width=1920, height=1080):
    global SHOW_CIRCLES
    
    FPS = 60
    clock = pygame.time.Clock()
    
    screen = pygame.display.set_mode((width, height), FULLSCREEN)
    canvas = Canvas(screen, (255, 255, 255))
    width, height = canvas.width, canvas.height
    
    margin = settings["margin"]
    # Create rectangle area the boids will try to stay within
    # ((corner_x, corner_y), (width, height))
    active_area = ((margin, margin),
                   (width - margin * 2, height - margin * 2))
    
    boids = create_boids(width, height, num_of_boids=50)

    while True:
        canvas.get_events() # Keypress events
        
        simulation.simulate(boids, active_area, settings)
        
        canvas.draw_background(active_area)
        canvas.draw_boids(boids, settings["boid size"])

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()