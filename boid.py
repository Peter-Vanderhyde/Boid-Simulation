
class Boid:
    def __init__(self, position, velocity, min_speed, max_speed, view_distance, separation_distance, color=(0, 0, 0)):
        self.position = position
        self.velocity = velocity
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.view_distance = view_distance
        self.separation_distance = separation_distance
        self.color = color