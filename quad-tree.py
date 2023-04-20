from pygame.math import Vector2 as Vector
from boid import Boid

class Node:
    def __init__(self, boid):
        self.boid = boid
        self.x = boid.position.x
        self.y = boid.position.y


class QuadTree:
    def __init__(self, top_left, bottom_right, node=None, parent=None):
        self.node = node
        self.parent = parent
        self.leaf = True
        self.tl_corner = top_left
        self.br_corner = bottom_right
        self.center = Vector((self.tl_corner.x + self.br_corner.x) // 2, (self.tl_corner.y + self.br_corner.y) // 2)
        self.clear_children()
    
    def clear_children(self):
        self.children = {
            "tl":None,
            "tr":None,
            "bl":None,
            "br":None
        }
    
    def remove_boid(self, boid):
        self.remove(Node(boid))
    
    def is_leaf(self):
        """Returns boolean of whether this node is a leaf or not."""

        return self.leaf
    
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
    
    def get_all_leaves(self):
        if self.is_leaf():
            return [self.node]

        nodes = []
        for child in self.children.values():
            if child:
                nodes += child.get_all_leaves()
        
        return nodes
    
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
    
    def create_child(self, child_string, node=None, parent=None):
        """Creates a new tree object based on the given child string to quadrant off the correct area."""

        if child_string == "tl":
            self.set_child("tl", QuadTree(Vector(self.tl_corner),
                                            Vector(self.center),
                                            node,
                                            parent))
        elif child_string == "bl":
            self.set_child("bl", QuadTree(Vector(self.tl_corner.x, self.center.y),
                                            Vector(self.center.x, self.br_corner.y),
                                            node,
                                            parent))
        elif child_string == "tr":
            self.set_child("tr", QuadTree(Vector(self.center.x, self.tl_corner.y),
                                            Vector(self.br_corner.x, self.center.y),
                                            node,
                                            parent))
        elif child_string == "br":
            self.set_child("br", QuadTree(Vector(self.center),
                                            Vector(self.br_corner),
                                            node,
                                            parent))
        else:
            raise RuntimeError("Received invalid child string.")

    def remove(self, n):
        """Remove a node from the tree and, if necessary, remove leaves until it reaches
        a branch to remove unecessary branches."""

        if self.is_leaf():
            if self.node.boid is n.boid: # Make sure this leaf node is the correct one
                self.node = None
                return True # Removed the node
            else:
                raise RuntimeError("Boid no longer exists.")
        
        else:
            child_string = self.find_child_for_node(n) # Find which child the node is in
            # Find how many children are in the current node
            total_children = sum([int(c is not None) for c in self.children.values()])

            removed_from_child = self.get_child(child_string).remove(n)
            if removed_from_child and total_children > 1:
                # The node was successfully found and removed, but
                # don't delete this node because there are other children connected
                self.set_child(child_string, None)
                total_children -= 1
            elif removed_from_child:
                for child in self.children.values():
                    if child and not child.leaf:
                        print(self.children.values())
            
            if total_children == 1: # This was a node of two, now one, so it can be simplified
                for child_string, child in self.children.items():
                    if child and child.is_leaf():
                        # There is one child and it's a leaf, so it can be simplified
                        # If it weren't a leaf, there are multiple leaves connected further down
                        self.node = child.node # Set the current node to the child's node
                        self.leaf = True
                        self.clear_children()
                        return False
            
            return False

    def insert(self, n):
        if self.is_leaf():
            # This is the bottom of the branch, so a new node needs to be made to make room
            # The current leaf is moved into whatever quadrant it needs to

            if self.node == None: # This is the first insert and the root is empty
                self.node = n
                return
            
            child_string = self.find_child_for_node(self.node)
            self.create_child(child_string, self.node, self)
            
            self.node = None
            self.leaf = False
        
        if abs(self.tl_corner.x - self.br_corner.x) >= 4 and abs(self.tl_corner.y - self.br_corner.y) >= 4:
            # There's room for more subtrees
            child_string = self.find_child_for_node(n)
            child = self.get_child(child_string)
            if child == None:
                self.create_child(child_string, n, self)
                return
            
            return child.insert(n)
        else:
            return
    
    def draw(self, screen):
        if self.is_leaf():
            if self.node is None:
                print("why?")
            pygame.draw.rect(screen, (255, 0, 0), (self.tl_corner, self.br_corner - self.tl_corner + Vector(1, 1)), 1)
            pygame.draw.circle(screen, (0, 0, 0), (self.node.x, self.node.y), 2)
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
    screen = pygame.display.set_mode((1280,720))
    tree = QuadTree(Vector(0, 0), Vector(1280, 720))
    boids = create_boids(1280, 720, 500)
    # boids[0].position = Vector(10, 100)
    # boids[1].position = Vector(300, 100)
    # boids[2].position = Vector(800, 100)
    for boid in boids:
        node = Node(boid)
        tree.insert(node)
        screen.fill((255,255,255))
        tree.draw(screen)
        pygame.display.update()
        time.sleep(0.01)
    
    time.sleep(5)
    
    for boid in boids:
        tree.remove_boid(boid)
        screen.fill((255,255,255))
        tree.draw(screen)
        pygame.display.update()
        time.sleep(0.01)
    
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()