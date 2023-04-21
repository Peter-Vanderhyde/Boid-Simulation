from pygame.math import Vector2 as Vector
from pygame.locals import Rect
import pygame
from boid import Boid


def create_tree(width, height, center, max_nodes, min_nodes):
    tl = Vector(center.x - width // 2, center.y - height // 2)
    br = tl + Vector(width, height)
    tree = QuadTree(tl, br, max_nodes=max_nodes, min_nodes=min_nodes)
    return tree

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
        self.rect = Rect(top_left, bottom_right - top_left)
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
    
    def get_possible_nodes(self, check_rect):
        if self.leaf:
            return self.nodes
        else:
            all_nodes = []
            for child in self.children.values():
                if child and check_rect.colliderect(child.rect):
                    all_nodes += child.get_possible_nodes(check_rect)
            
            return all_nodes
    
    def find_points_in_radius(self, position, radius):
        rect = Rect(position.x - radius, position.y - radius, radius*2, radius*2)
        possible_points = self.get_possible_nodes(rect)
        in_range = []
        for node in possible_points:
            if position.distance_squared_to(node.boid.position) <= radius**2:
                in_range.append(node)
        
        return in_range
    
    def get_boids_in_sight(self, boid):
        nodes = self.find_points_in_radius(boid.position, max(boid.settings["view distance"]["value"], boid.settings["separation distance"]["value"]))
        return [node.boid for node in nodes]

    def adjust_boid_position(self, boid, dt):
        node = Node(boid)
        boid.position += boid.velocity * dt * 60
        return self.update_node(node)
    
    def update_node(self, n):
        if self.leaf:
            for node in self.nodes:
                if node.boid is n.boid:
                    if self.rect.collidepoint(n.boid.position):
                        node.x = n.boid.position.x
                        node.y = n.boid.position.y
                        return False
                    else:
                        self.nodes.remove(node)
                        self.node_count -= 1
                        return n
            
            raise RuntimeError("Unable to find boid.")
        else:
            child_string = self.find_child_for_node(n)
            child = self.get_child(child_string)
            if child is None:
                raise RuntimeError("Unable to find boid.")
            
            node = child.update_node(n)
            if not node:
                return False
            else:
                self.node_count -= 1
                if child.node_count <= 0:
                    self.set_child(child_string, None)
                
                if self.rect.collidepoint(n.boid.position):
                    n.x = n.boid.position.x
                    n.y = n.boid.position.y
                    self.insert_node(n)
                    return False
                else:
                    if self.node_count < self.min_nodes:
                        self.reabsorb()
                    return n
    
    def update(self, minimum, maximum):
        self.min_nodes = minimum
        self.max_nodes = maximum
        if self.leaf:
            return
        for child in self.children.values():
            if child:
                child.update(minimum, maximum)
    
    def draw_grid(self, screen):
        pygame.draw.rect(screen, (150, 150, 150), (self.rect.left, self.rect.top, self.rect.width + 1, self.rect.height + 1), 1)
        if not self.leaf:
            for child in self.children.values():
                if child:
                    child.draw_grid(screen)

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
    tree = QuadTree(Vector(0, 0), Vector(1280, 720), max_nodes=25, min_nodes=15)
    boids = []
    circle = None
    
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_EQUALS:
                    new_boids = create_boids(1280, 720, tree, 200)
                    
                    boids += new_boids
                elif event.key == K_MINUS and boids:
                    for i in range(min(50, len(boids))):
                        boid = random.choice(boids)
                        tree.remove_boid(boid)
                        boids.remove(boid)
                elif event.key == K_RETURN:
                    position = Vector(random.randint(0, 1280), random.randint(0, 720))
                    circle = [position, random.randint(1, 1280)]
            elif event.type == MOUSEBUTTONDOWN:
                pos = Vector(pygame.mouse.get_pos())
                boid = Boid(pos, Vector(0, 1), None)
                success = tree.insert_boid(boid)

        screen.fill((255, 255, 255))
        tree.draw(screen)
        if circle:
            in_nodes = tree.find_points_in_radius(circle[0], circle[1])
            for node in in_nodes:
                pygame.draw.circle(screen, (0, 255, 0), node.boid.position, 2)

            pygame.draw.circle(screen, (0, 200, 0), circle[0], circle[1], 2)
        pygame.display.update()
        for boid in boids:
            failed = tree.adjust_boid_position(boid)
            if failed:
                boid.velocity *= -1
                tree.insert_boid(boid)