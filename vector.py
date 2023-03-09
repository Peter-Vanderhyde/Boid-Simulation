import math


class Vector:
    """A custom vector class for simplifying arithmetic operations."""

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
        if isinstance(other, (Vector, int, float)):
            return self.__add__(-other)
        else:
            raise RuntimeError(f"Cannot subtract Vector and {type(other)}.")
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        else:
            raise RuntimeError(f"Attempt to multiply Vector by {type(other)}.")
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise RuntimeError("Cannot divide Vector by 0.")
            
            return Vector(self.x / other, self.y / other)
        else:
            raise RuntimeError(f"Attempt to divide Vector by {type(other)}.")
    
    def __itruediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise RuntimeError("Cannot divide Vector by 0.")
            
            self.x /= other
            self.y /= other
            return self
        else:
            raise RuntimeError(f"Attempt to divide Vector by {type(other)}.")
    
    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise RuntimeError("Cannot divide Vector by 0.")
            
            return Vector(self.x // other, self.y // other)
        else:
            raise RuntimeError(f"Attempt to divide Vector by {type(other)}.")
    
    def __ifloordiv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise RuntimeError("Cannot divide Vector by 0.")
            
            self.x //= other
            self.y //= other
            return self
        else:
            raise RuntimeError(f"Attempt to divide Vector by {type(other)}.")
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def values(self):
        return self.x, self.y
    
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self):
        length = self.length()
        if length == 0:
            raise RuntimeError("Cannot normalize Vector of length 0.")
        
        return self.__truediv__(length)


if __name__ == '__main__':
    v = Vector(3, 4)
    v /= 10
    print(v)