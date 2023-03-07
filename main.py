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

def get_random_direction():
    flipped_x = random.choice([-1, 1])
    x = random.random() * 2 * flipped_x
    flipped_y = random.choice([-1, 1])
    y = random.random() * 2 * flipped_y
    return Vector(x, y).normalize()

def create_boids(width, height, num_of_boids=10):
    """Creates boid objects with random positions and velocities."""

    boids = []
    for i in range(num_of_boids):
        x, y = random.randint(0, width), random.randint(0, height)
        position = Vector(x, y)
        speed_range = settings["maximum speed"] - settings["minimum speed"]
        speed = settings["minimum speed"] + speed_range * random.random() # Randomize the speed
        velocity = get_random_direction() * speed
        boid = Boid(position,
                    velocity,
                    settings["minimum speed"],
                    settings["maximum speed"],
                    settings["view distance"],
                    settings["separation distance"],
                    color=(155, 0, 0))
        boids.append(boid)
    
    return boids


def main(width=1920, height=1080):
    """Initializes the canvas and boid, then runs the main loop."""

    FPS = 60
    clock = pygame.time.Clock() # Allows pygame to limit the fps
    
    canvas = Canvas(width, height, bg_color=(255, 255, 255)) # Handles functions for drawing, and events
    
    width, height = canvas.width, canvas.height
    margin = settings["margin"]
    # Create rectangle area the boids will try to stay within
    # ((corner_x, corner_y), (width, height))
    active_area = ((margin, margin),
                   (width - margin * 2, height - margin * 2))
    
    boids = create_boids(width, height, num_of_boids=100)

    while True:
        canvas.get_events() # Keypress events
        
        simulation.simulate(boids, active_area, settings)
        
        canvas.draw_background(active_area)
        canvas.draw_boids(boids, settings["boid size"])

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()