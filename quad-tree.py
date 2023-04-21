from pygame.math import Vector2 as Vector
from pygame.locals import Rect
from boid import Boid

class Node:
    def __init__(self, boid):
        self.boid = boid
        self.x = boid.position.x
        self.y = boid.position.y


class QuadTree:
    def __init__(self, top_left, bottom_right, nodes=[], parent=None, max_nodes=25, min_nodes=15):
        self.nodes = nodes
        self.parent = parent
        self.max_nodes = max_nodes
        self.min_nodes = min_nodes
        self.node_count = len(nodes)
        self.leaf = True
        self.tl_corner = top_left
        self.br_corner = bottom_right
        self.center = Vector((self.tl_corner.x + self.br_corner.x) // 2, (self.tl_corner.y + self.br_corner.y) // 2)
        self.rect = Rect(top_left, bottom_right - top_left + Vector(1, 1))
        self.clear_children()
    
    def clear_children(self):
        self.children = {
            "tl":None,
            "tr":None,
            "bl":None,
            "br":None
        }
    
    def remove_boid(self, boid):
        self.remove_node(Node(boid))
    
    def insert_boid(self, boid):
        self.insert_node(Node(boid))
    
    def get_child(self, string):
        """Returns the tree object of the given child string."""

        try:
            return self.children[string]
        except:
            raise RuntimeError(f"Unable to retrieve child with the string '{string}'.")

    def set_child(self, string, tree):
        """Sets the tree object of the given child string."""

        if tree is None or type(tree) == QuadTree:
            self.children[string] = tree
        else:
            raise TypeError("Attempted to set child as non quadtree type.")
    
    def find_child_for_node(self, n):
        """Returns the string of which child quad the node is inside."""

        x, y = self.center
        if n.x <= x:
            if n.y <= y:
                return "tl"
            else:
                return "bl"
        else:
            if n.y <= y:
                return "tr"
            else:
                return "br"
    
    def create_child(self, child_string, node, parent=None):
        """Creates a new tree object based on the given child string to quadrant off the correct area."""

        if child_string == "tl":
            new_child = QuadTree(self.tl_corner,
                                 self.center,
                                 nodes=[node],
                                 parent=parent,
                                 max_nodes=self.max_nodes,
                                 min_nodes=self.min_nodes)
            self.set_child("tl", new_child)
            return new_child
        elif child_string == "bl":
            new_child = QuadTree(Vector(self.tl_corner.x, self.center.y + 1),
                                Vector(self.center.x, self.br_corner.y),
                                nodes=[node],
                                parent=parent,
                                max_nodes=self.max_nodes,
                                min_nodes=self.min_nodes)
            self.set_child("bl", new_child)
            return new_child
        elif child_string == "tr":
            new_child = QuadTree(Vector(self.center.x + 1, self.tl_corner.y),
                                Vector(self.br_corner.x, self.center.y),
                                nodes=[node],
                                parent=parent,
                                max_nodes=self.max_nodes,
                                min_nodes=self.min_nodes)
            self.set_child("tr", new_child)
            return new_child
        elif child_string == "br":
            new_child = QuadTree(self.center + Vector(1, 1),
                                self.br_corner,
                                nodes=[node],
                                parent=parent,
                                max_nodes=self.max_nodes,
                                min_nodes=self.min_nodes)
            self.set_child("br", new_child)
            return new_child
        else:
            raise RuntimeError("Received invalid child string.")
    
    def divide(self):
        for node in self.nodes:
            child_string = self.find_child_for_node(node)
            child = self.get_child(child_string)
            if child is None:
                self.create_child(child_string, node, self)
            else:
                child.insert_node(node)
        
        self.nodes = []
        self.leaf = False
    
    def insert_node(self, n):
        if self.leaf:
            self.nodes.append(n)
            self.node_count += 1
            if len(self.nodes) > self.max_nodes and\
                    abs(self.tl_corner.x - self.br_corner.x) >= 4 and\
                    abs(self.tl_corner.y - self.br_corner.y) >= 4: # There's room for more subtrees:
                # The node has too many objects, so it will subdivide
                self.divide()
        else:
            child_string = self.find_child_for_node(n)
            child = self.get_child(child_string)
            if child is None:
                self.create_child(child_string, n, self)
            else:
                child.insert_node(n)
            
            self.node_count += 1
    
    def get_all_leaves(self):
        if self.nodes != []:
            return self.nodes
        else:
            leaves = []
            for child in self.children.values():
                if child:
                    leaves += child.get_all_leaves()
            
            return leaves
    
    def reabsorb(self):
        self.nodes = self.get_all_leaves()
        self.clear_children()
        self.leaf = True
    
    def remove_node(self, n):
        if self.nodes != []:
            for index, node in enumerate(self.nodes):
                if node.boid is n.boid:
                    self.nodes.pop(index)
                    self.node_count -= 1
                    return
            
            raise RuntimeError("Unable to find boid in tree.")
        else:
            child_string = self.find_child_for_node(n)
            child = self.get_child(child_string)
            if child is None:
                raise RuntimeError("Unable to find boid in tree.")
            
            child.remove_node(n)
            self.node_count -= 1
            if child.node_count <= 0:
                self.set_child(child_string, None)
            
            if self.node_count < self.min_nodes:
                self.reabsorb()
    
    def draw(self, screen):
        if self.leaf:
            for node in self.nodes:
                pygame.draw.circle(screen, node.boid.color, (node.x, node.y), 2)
            
            pygame.draw.rect(screen, (255, 0, 0), (self.tl_corner, self.br_corner - self.tl_corner + Vector(1, 1)), 1)
        else:
            for child in self.children.values():
                if child is not None:
                    child.draw(screen)
            
            pygame.draw.rect(screen, (255, 0, 0), (self.tl_corner, self.br_corner - self.tl_corner + Vector(1, 1)), 1)


if __name__ == '__main__':
    import pygame
    import sys, time
    from pygame.locals import *
    from main import create_boids
    import random
    screen = pygame.display.set_mode((1280,720))
    tree = QuadTree(Vector(0, 0), Vector(1280, 720), max_nodes=4, min_nodes=3)
    boids = []
    
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_EQUALS:
                    new_boids = create_boids(1280, 720, 50)
                    for boid in new_boids:
                        tree.insert_boid(boid)
                    
                    boids += new_boids
                elif event.key == K_MINUS and boids:
                    for i in range(min(50, len(boids))):
                        boid = random.choice(boids)
                        tree.remove_boid(boid)
                        boids.remove(boid)
            elif event.type == MOUSEBUTTONDOWN:
                pos = Vector(pygame.mouse.get_pos())
                boid = Boid(pos, Vector(0, 1), None)
                success = tree.insert_boid(boid)
        
        screen.fill((255, 255, 255))
        tree.draw(screen)
        pygame.display.update()