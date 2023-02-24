import unittest
from vector import Vector


class TestVectorMethods(unittest.TestCase):
    def test_vector_add(self):
        v = Vector(2, 3)
        v2 = Vector(4, 4)
        self.assertEqual((v + v2).values(), (6, 7))


if __name__ == "__main__":
    unittest.main()