from vector import Vector


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class QuadTree:
    def __init__(self):
        self.tl = None
        self.tr = None
        self.bl = None
        self.br = None