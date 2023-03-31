import random
import pygame
from pygame.locals import *
from canvas import Canvas
from boid import Boid
from vector import Vector
import simulation
pygame.init()

#TODO Have the sidebar check its own events
settings = {
    "view distance": {
        "value": 50,
        "min": 0,
        "max": 5000
    },
    "separation distance": {
        "value": 15,
        "min": 0,
        "max": 500
    },
    "minimum speed": {
        "value": 3,
        "min": 0.1,
        "max": 50
    },
    "maximum speed": {
        "value": 6,
        "min": 0.1,
        "max": 50
    },
    "centering factor": {
        "value": 0.0005,
        "min": 0,
        "max": 0.01
    },
    "matching factor": {
        "value": 0.05,
        "min": 0,
        "max": 1.0
    },
    "avoid factor": {
        "value": 0.05,
        "min": 0,
        "max": 1.0
    },
    "turn factor": {
        "value": 0.2,
        "min": 0,
        "max": 10
    },
    "margin": {
        "value": 100,
        "min": 0,
        "max": None
    },
    "boid size": {
        "value": 8,
        "min": 0.01,
        "max": 30
    }
}

default_settings = settings.copy()

def get_random_direction():
    x, y = 0, 0
    while x == 0 and y == 0:
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
        speed_range = settings["maximum speed"]["value"] - settings["minimum speed"]["value"]
        speed = settings["minimum speed"]["value"] + speed_range * random.random() # Randomize the speed
        velocity = get_random_direction() * speed
        boid = Boid(position,
                    velocity,
                    settings,
                    color=(155, 0, 0))
        boids.append(boid)
    
    return boids


def main(width=1920, height=1080):
    """Initializes the canvas and boid, then runs the main loop."""

    FPS = 60
    clock = pygame.time.Clock() # Allows pygame to limit the fps

    settings["margin"]["max"] = min(width, height) / 2 - 1
    canvas = Canvas(width, height, (255, 255, 255), settings) # Handles functions for drawing, and events
    canvas.create_sidebar(width=250, margins=(10, 10))
    for key in settings.keys():
        canvas.sidebar.add_property(key)
    
    width, height = canvas.width, canvas.height
    boids = create_boids(width, height, num_of_boids=100)

    while True:
        canvas.get_events() # Keypress events
        
        simulation.simulate(boids, canvas.active_area, settings)
        
        canvas.draw(boids)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main(1280, 720)