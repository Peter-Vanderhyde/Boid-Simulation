from boid import Boid
from vector import Vector


def simulate(boids):
    for boid in boids:
        boid.rotate_ip(1)
        boid.move()