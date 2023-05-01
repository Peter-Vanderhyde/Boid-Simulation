import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import quad_tree as qt
from pygame.math import Vector2
from boid import Boid


class TestQuadTreeMethods(unittest.TestCase):
    def setUp(self):
        self.tree = qt.QuadTree(Vector2(-1000, -1000), Vector2(1000, 1000), max_nodes=3, min_nodes=2)
        self.tree.nodes = []
        self.tree.clear_children()
    
    def test_1_node(self):
        b = Boid({}, Vector2(100, 100))
        n = qt.Node(b)
        self.assertEqual((n.x, n.y), (b.position.x, b.position.y))
    
    def test_2_quad_root_insert(self):
        n = qt.Node(Boid({}, Vector2(100, 100)))
        self.tree.insert_node(n)
        with self.subTest("Node inserted in root."):
            self.assertEqual(self.tree.nodes[0], n)
        
        n = qt.Node(Boid({}, Vector2(-100, 100)))
        self.tree.insert_node(n)
        with self.subTest("Multiple nodes inserted."):
            self.assertEqual(self.tree.nodes[1], n)
    
    def test_3_quad_divide(self):
        n1 = qt.Node(Boid({}, Vector2(100, 100)))
        self.tree.insert_node(n1)
        n2 = qt.Node(Boid({}, Vector2(-100, 100)))
        self.tree.insert_node(n2)
        self.tree.divide()
        with self.subTest("BR child created."):
            child = self.tree.children['br']
            self.assertTrue(child and child.nodes == [n1])
        
        with self.subTest("BL child created."):
            child = self.tree.children['bl']
            self.assertTrue(child and child.nodes == [n2])
        
        with self.subTest("TL and TR are empty."):
            self.assertFalse(self.tree.children['tl'] or self.tree.children['tr'])
        
        with self.subTest("Root empty."):
            self.assertListEqual(self.tree.nodes, [])


if __name__ == '__main__':
    unittest.main()