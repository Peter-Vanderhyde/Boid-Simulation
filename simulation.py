from boid import Boid
from vector import Vector


def simulate(dt, boids):
    for boid in boids:
        close = Vector(0, 0)
        neighboring_boids = 0
        for other in boids:
            if boid is not other:
                difference = boid.position - other.position
                if abs(difference.x) < boid.VIEW_DISTANCE and abs(difference.y) < boid.VIEW_DISTANCE:
                    pass