import random
import pygame
from pygame.locals import *
from canvas import Canvas
from boid import Boid
from pygame.math import Vector2 as Vector
import simulation
import quad_tree
import time
import copy
pygame.init()

# Settings that appear on the sidebar
settings = {
    "boids": {
        "value": 100,
        "min": 1,
        "max": 5000
    },
    "view distance": {
        "value": 50,
        "min": 0,
        "max": 100
    },
    "separation distance": {
        "value": 15,
        "min": 0,
        "max": 100
    },
    "minimum speed": {
        "value": 3,
        "min": 0.1,
        "max": 20
    },
    "maximum speed": {
        "value": 6,
        "min": 0.1,
        "max": 20
    },
    "centering factor": {
        "value": 0.0005,
        "min": 0,
        "max": 0.01
    },
    "matching factor": {
        "value": 0.05,
        "min": 0,
        "max": 0.5
    },
    "avoid factor": {
        "value": 0.05,
        "min": 0,
        "max": 0.5
    },
    "avoid zone factor": {
        "value": 0.003,
        "min": 0,
        "max": 0.1
    },
    "turn factor": {
        "value": 0.2,
        "min": 0,
        "max": 5
    },
    "boid size": {
        "value": 8,
        "min": 0.01,
        "max": 30
    },
    "min per node": {
        "value": 15,
        "min": 1,
        "max": 50
    },
    "max per node": {
        "value": 20,
        "min": 1,
        "max": 50
    }
}

default_settings = copy.deepcopy(settings)

def get_random_direction():
    """A function that returns a simple random vector direction
    for spawning boids."""

    x, y = 0, 0
    while x == 0 and y == 0:
        flipped_x = random.choice([-1, 1])
        x = random.random() * 2 * flipped_x
        flipped_y = random.choice([-1, 1])
        y = random.random() * 2 * flipped_y
    
    return Vector(x, y).normalize()

def create_boids(width, height, tree, num_of_boids=10):
    """Creates boid objects with random positions and velocities, inserts them
    into the quad tree, then returns the list of created boids."""

    boids = []
    for _ in range(num_of_boids):
        x, y = random.randint(0, width), random.randint(0, height)
        position = Vector(x, y)
        speed_range = settings["maximum speed"]["value"] - settings["minimum speed"]["value"]
        speed = settings["minimum speed"]["value"] + speed_range * random.random() # Randomize the speed
        velocity = get_random_direction() * speed
        boid = Boid(settings,
                    position,
                    velocity,
                    color=(227, 220, 194))
        boids.append(boid)
        tree.insert_boid(boid)
    
    return boids

def delete_boids(boids, tree, amount):
    """Deletes the given amount of boids from the quad tree."""

    amount = min(amount, len(boids))
    for _ in range(amount):
        boid = random.choice(boids)
        tree.remove_boid(boid)
        boids.remove(boid)


def main(width=1920, height=1080):
    """Creates a canvas and a tree, adds boids to it, then runs the main loop."""

    FPS = 60
    clock = pygame.time.Clock() # Allows pygame to limit the fps to save on performance
    last_frame = time.time()

    canvas = Canvas(width, height, (27, 32, 33), settings, default_settings) # The canvas handles drawing and events
    canvas.create_sidebar(width=250,
                          margins=(10, 10),
                          bg_color=(206, 208, 143),
                          text_color=(81, 81, 61),
                          slider_color=(227, 220, 149))
    for key in settings.keys():
        canvas.sidebar.add_setting(key)
    
    width, height = canvas.width, canvas.height
    tree = quad_tree.create_tree(5000, 5000, Vector(width // 2, height // 2), 25, 15)
    canvas.tree = tree
    boids = create_boids(width, height, tree=tree, num_of_boids=settings["boids"]["value"])

    while True:
        dt = time.time() - last_frame # Calculate delta time
        last_frame = time.time()
        canvas.get_events() # Keypress events

        minimum = settings["min per node"]["value"]
        maximum = settings["max per node"]["value"]
        # Check whether it's necessary to update the tree's number of nodes settings
        if int(minimum) != tree.min_nodes or int(maximum) != tree.max_nodes:
            tree.update_node_size(int(minimum), int(maximum))

        """ New Simulation Method """
        boid_setting = int(settings["boids"]["value"])
        if boid_setting != len(boids): # The setting was changed, so boids should be adjusted
            if len(boids) < boid_setting:
                boids += create_boids(width, height, tree=tree, num_of_boids=boid_setting - len(boids))
            else:
                delete_boids(boids, tree, len(boids) - boid_setting)
        
        lost_boids = simulation.simulate(boids, canvas.active_area, settings, tree, canvas.zones, dt)
        # It is possible for the user to create situations where the boids get stuck outside the span
        # of the tree with a combination of extreme values and slow simulation update time.
        # This ensures that, when that happens, the boids are removed and reset within the simulation space.
        boids += create_boids(width, height, tree, lost_boids)
        
        canvas.draw(boids)

        pygame.display.update()
        clock.tick(FPS) # Update at a rate of FPS


if __name__ == "__main__":
    main(1280, 720)