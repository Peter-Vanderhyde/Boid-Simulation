import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import quad_tree as qt
from pygame.math import Vector2 as Vector
from pygame import Rect
from boid import Boid


class TestQuadTreeMethods(unittest.TestCase):
    def setUp(self):
        self.tree = qt.QuadTree(Vector(-1000, -1000), Vector(1000, 1000), max_nodes=3, min_nodes=2)
        self.tree.nodes = []
        self.tree.node_count = 0
        self.tree.clear_children()
    
    def test_1_node(self):
        b = Boid({}, Vector(100, 100))
        n = qt.Node(b)
        self.assertEqual((n.x, n.y), (b.position.x, b.position.y))
    
    def test_2_quad_root_insert(self):
        n = qt.Node(Boid({}, Vector(100, 100)))
        self.tree.insert_node(n)
        with self.subTest("Node inserted in root."):
            self.assertEqual(self.tree.nodes[0], n)
        
        n = qt.Node(Boid({}, Vector(-100, 100)))
        self.tree.insert_node(n)
        with self.subTest("Multiple nodes inserted."):
            self.assertEqual(self.tree.nodes[1], n)

        with self.subTest("Node at borders not inserted."):
            self.tree.max_nodes = 4
            self.tree.nodes = []
            self.tree.node_count = 0
            self.tree.insert_node(qt.Node(Boid({}, Vector(1000, 1000))))
            self.tree.insert_node(qt.Node(Boid({}, Vector(-1000, 1000))))
            self.tree.insert_node(qt.Node(Boid({}, Vector(1000, -1000))))
            self.tree.insert_node(qt.Node(Boid({}, Vector(-1000, -1000))))
            self.assertTrue(len(self.tree.nodes) == 4)
        
        with self.subTest("Node at center corner not inserted."):
            self.tree.nodes = []
            self.tree.node_count = 0
            self.tree.insert_node(qt.Node(Boid({}, Vector(0, 0))))
            self.assertTrue(len(self.tree.nodes) == 1)
        
        with self.subTest("Node inserted outside the border."):
            # Insert a node with x outside of 1000 boundary
            self.assertRaises(RuntimeError, self.tree.insert_node, qt.Node(Boid({}, Vector(1001, 0))))
    
    def test_3_quad_divide(self):
        n1 = qt.Node(Boid({}, Vector(100, 100)))
        self.tree.insert_node(n1)
        n2 = qt.Node(Boid({}, Vector(-100, 100)))
        self.tree.insert_node(n2)
        self.tree.divide()
        with self.subTest("BR child not created."):
            child = self.tree.children['br']
            self.assertTrue(child and child.nodes == [n1])
        
        with self.subTest("BL child not created."):
            child = self.tree.children['bl']
            self.assertTrue(child and child.nodes == [n2])
        
        with self.subTest("TL and TR are not empty."):
            self.assertFalse(self.tree.children['tl'] or self.tree.children['tr'])
        
        with self.subTest("Root not empty."):
            self.assertTrue(self.tree.nodes == [] and self.tree.node_count == 2)
    
    def test_4_quad_insert_divide(self):
        self.tree.insert_node(qt.Node(Boid({}, Vector(220, 220))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(20, 20))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(-220, 220))))
        with self.subTest("Tree divided too early."):
            self.assertTrue(not any(self.tree.children.values()) and len(self.tree.nodes) == 3)
        
        self.tree.insert_node(qt.Node(Boid({}, Vector(220, -220))))
        with self.subTest("Tree did not divide."):
            self.assertTrue(
                self.tree.nodes == [] and\
                any(self.tree.children.values()) and\
                self.tree.node_count == 4
            )
        
    def test_5_quad_insert_children(self):
        self.tree.insert_node(qt.Node(Boid({}, Vector(10, 10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(-10, 10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(10, -10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(-10, -10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(100, 100))))
        self.assertEqual(self.tree.children['br'].node_count, 2)
    
    def test_6_quad_reabsorb(self):
        self.tree.insert_node(qt.Node(Boid({}, Vector(10, 10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(100, 10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(10, -10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(-10, -10))))
        with self.subTest("Did not create child."):
            self.assertTrue(self.tree.children['br'].node_count == 2 and self.tree.nodes == [])

        self.tree.reabsorb()        
        with self.subTest("Nodes were not reabsorbed."):
            self.assertTrue(
                len(self.tree.nodes) == 4 and\
                not any(self.tree.children.values())
            )
    
    def test_7_quad_remove_node(self):
        n = qt.Node(Boid({}, Vector(10, 10)))
        self.tree.insert_node(n)
        with self.subTest("No error thrown when removing non-existent node."):
            self.assertRaises(RuntimeError, self.tree.remove_node, qt.Node(Boid({}, Vector(20, 20))))
        
        self.tree.remove_node(n)
        with self.subTest("Node was not removed."):
            self.assertTrue(
                n not in self.tree.nodes and\
                self.tree.node_count == 0
            )
        
        nodes = [qt.Node(Boid({}, Vector(i, i))) for i in range(4)]
        for n in nodes:
            self.tree.insert_node(n)
        
        with self.subTest("Progress check."):
            self.assertEqual(self.tree.node_count, 4)
        
        for n in nodes:
            self.tree.remove_node(n)
        
        with self.subTest("Tree not empty."):
            self.assertTrue(
                self.tree.node_count == 0 and\
                self.tree.nodes == [] and\
                not any(self.tree.children.values())
            )
    
    def test_8_quad_possible_nodes(self):
        n1 = qt.Node(Boid({}, Vector(100, 100)))
        n2 = qt.Node(Boid({}, Vector(800, -500)))
        self.tree.insert_node(n1)
        self.tree.insert_node(n2)
        self.tree.insert_node(qt.Node(Boid({}, Vector(-10, -10))))
        self.tree.insert_node(qt.Node(Boid({}, Vector(-10, 400))))
        rect = Rect(500, -20, 10, 80)
        possibilities = self.tree.get_possible_nodes(rect)
        self.assertTrue(len(possibilities) == 2 and n1 in possibilities and n2 in possibilities,
                        "Didn't find the correct possible nodes")



if __name__ == '__main__':
    unittest.main()