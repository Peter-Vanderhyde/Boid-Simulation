import unittest
from vector import Vector


class TestVectorMethods(unittest.TestCase):
    def test_vector_neg(self):
        v = Vector(2, 3)
        v1 = Vector(2, -3)
        v2 = Vector(-2, 3)
        v3 = Vector(-2, -3)
        self.assertEqual((-v).values(), (-2, -3))
        self.assertEqual((-v1).values(), (-2, 3))
        self.assertEqual((-v2).values(), (2, -3))
        self.assertEqual((-v3).values(), (2, 3))
    
    def test_vector_add(self):
        v = Vector(2, 3)
        v2 = Vector(4, 4)
        self.assertEqual((v + v2).values(), (6, 7))
    
    def test_vector_sub(self):
        v = Vector(2, 3)
        v2 = Vector(4, 4)
        self.assertEqual((v - v2).values(), (-2, -1))


if __name__ == "__main__":
    unittest.main()