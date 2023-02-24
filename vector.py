import numpy as np


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector(self.x + other, self.y + other)
        else:
            raise RuntimeError(f"Cannot add Vector and {type(other)}.")
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector(self.x - other, self.y - other)
        else:
            raise RuntimeError(f"Cannot subtract Vector and {type(other)}.")
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        else:
            raise RuntimeError(f"Attempt to multiply Vector by {type(other)}.")
    
    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        else:
            raise RuntimeError(f"Attempt to divide Vector by {type(other)}.")
    
    def __str__(self):
        return f"({self.x}, {self.y})"