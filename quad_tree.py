from pygame.math import Vector2 as Vector
from pygame.locals import Rect
import pygame
from boid import Boid


def create_tree(width, height, center, max_nodes, min_nodes):
    """Returns a tree based on the width, height, etc."""

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
    """A quad tree containing multiple nodes per leaf that dynamically change as the nodes move."""

    def __init__(self, top_left, bottom_right, nodes=[], parent=None, max_nodes=25, min_nodes=15):
        self.nodes = nodes
        self.parent = parent
        self.max_nodes = max_nodes # Node number at which the leaf will subdivide
        self.min_nodes = min_nodes # Node number at which a parent will reabsorb its kids' nodes
        self.node_count = len(nodes) # The number of total nodes whithin all children combined
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
        """Returns the child tree object based on the given child string."""

        try:
            return self.children[string]
        except:
            raise RuntimeError(f"Unable to retrieve child with the string '{string}'.")

    def set_child(self, string, tree):
        """Sets the child tree object of the given child string."""

        if tree is None or type(tree) == QuadTree:
            self.children[string] = tree
        else:
            raise TypeError("Attempted to set child as non quadtree type.")
    
    def node_within_bounds(self, n):
        """Returns the string of which child quad the node is inside."""

        x, y = self.center
        tx, ty = self.tl_corner
        bx, by = self.br_corner
        return tx <= n.x <= bx and ty <= n.y <= by
    
    def find_child_string_for_node(self, n):
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
        """Subdivides the current leaf and separate its nodes into the appropriate children."""

        for node in self.nodes:
            child_string = self.find_child_string_for_node(node)
            child = self.get_child(child_string)
            if child is None: # No child in that quadrant yet
                self.create_child(child_string, node, self)
            else:
                child.insert_node(node)
        
        self.nodes = []
        self.leaf = False
    
    def insert_node(self, n):
        """Finds the correct leaf to place the given node into."""

        if self.parent == None and not self.node_within_bounds(n): # In the root
            # The node is outside of the area of the tree.
            raise RuntimeError("Node outside of tree boundaries.")

        if self.leaf:
            self.nodes.append(n)
            self.node_count += 1
            if len(self.nodes) > self.max_nodes and\
                    abs(self.tl_corner.x - self.br_corner.x) >= 4 and\
                    abs(self.tl_corner.y - self.br_corner.y) >= 4: # There's room for more subtrees
                # The node has too many objects, so it will subdivide
                self.divide()
        else:
            child_string = self.find_child_string_for_node(n)
            child = self.get_child(child_string)
            if child is None:
                # Create a new leaf to place the node in
                self.create_child(child_string, n, self)
            else:
                child.insert_node(n)
            
            self.node_count += 1
    
    def get_all_leaves(self):
        """Finds all of the leaves' nodes within itself/its children."""

        if self.leaf: # Reached a leaf
            return self.nodes
        else:
            leaves = []
            for child in self.children.values():
                if child:
                    leaves += child.get_all_leaves()
            
            return leaves
    
    def reabsorb(self):
        """Finds every node in its children, it makes itself a leaf to hold them, and deletes its children."""

        self.nodes = self.get_all_leaves()
        self.clear_children()
        self.leaf = True
    
    def remove_node(self, n):
        """Checks the appropriate leaf where the node should be located, then removes it when found."""

        if self.nodes != []:
            for index, node in enumerate(self.nodes):
                if node.boid is n.boid:
                    self.nodes.pop(index)
                    self.node_count -= 1
                    return
            
            raise RuntimeError("Unable to find boid in tree.")
        else:
            child_string = self.find_child_string_for_node(n)
            child = self.get_child(child_string)
            if child is None:
                raise RuntimeError("Unable to find boid in tree.")
            
            child.remove_node(n)
            self.node_count -= 1
            if child.node_count <= 0: # No nodes left in that child
                self.set_child(child_string, None) # Remove the child
            
            if self.node_count < self.min_nodes:
                # The combined nodes in its children are less than the minimum, so combine them
                self.reabsorb()
    
    def get_possible_nodes(self, check_rect):
        """Based on a given Rect, find all quads who overlap with that rect, as
        they may contain nodes within the Rect."""

        if self.leaf:
            return self.nodes
        else:
            all_nodes = []
            for child in self.children.values():
                if child and check_rect.colliderect(child.rect): # Overlaps
                    all_nodes += child.get_possible_nodes(check_rect)
            
            return all_nodes
    
    def find_points_in_radius(self, position, radius):
        """First finds the possible nodes within a Rect surrounding
        the circle. Then it checks each node separately to see if it is within the circle."""

        rect = Rect(position.x - radius, position.y - radius, radius*2, radius*2) # Rect surrounding circle
        possible_points = self.get_possible_nodes(rect)
        in_range = []
        for node in possible_points: # Check each node separately
            if position.distance_squared_to(node.boid.position) <= radius**2: # Checking the square for computation time
                in_range.append(node)
        
        return in_range
    
    def get_boids_in_sight(self, boid):
        """This finds all boids within sight of this boid based on the boids'
        position and view distance."""

        nodes = self.find_points_in_radius(boid.position,
                                           max(boid.settings["view distance"]["value"],
                                            boid.settings["separation distance"]["value"]))
        return [node.boid for node in nodes] # Return the boids, not the nodes

    def adjust_boid_position(self, boid, dt):
        """This will move the boid based on its velocity. It then checks
        where it used to be in the tree and checks whether it would still
        stay within that leaf. If not, it is moved."""

        node = Node(boid) # Make a node based on the old position
        boid.position += boid.velocity * dt * 60 # Update its position
        outside_tree_bounds = self.update_node(node)
        # If a node was returned, the new node climbed so far up the tree trying to find
        # the correct node that it exited. This means there is no leaf that
        # can contain it
        if outside_tree_bounds:
            # Quick dirty fix
            boid.velocity *= -1 # Reverse the velocity
            # Move the boid back within the bounds of the tree
            boid.position.x = min(max(boid.position.x, self.tl_corner.x + 10), self.br_corner.x - 10)
            boid.position.y = min(max(boid.position.y, self.tl_corner.y + 10), self.br_corner.y - 10)
            self.insert_boid(boid)
    
    def update_node(self, n):
        """Find where this node is, check if it can stay in the same leaf.
        Either update the old node, or move the node to a new leaf."""

        if self.leaf:
            for node in self.nodes:
                if node.boid is n.boid: # Found old node
                    if self.rect.collidepoint(n.boid.position): # Can stay within the leaf
                        # Update the old node
                        node.x = n.boid.position.x
                        node.y = n.boid.position.y
                        return False # Found a satisfactory leaf
                    else:
                        self.nodes.remove(node)
                        self.node_count -= 1
                        return n
            
            raise RuntimeError("Unable to find boid.")
        else:
            child_string = self.find_child_string_for_node(n)
            child = self.get_child(child_string)
            if child is None:
                raise RuntimeError("Unable to find boid.")
            
            node = child.update_node(n)
            if not node: # Node was updated
                return False
            else:
                # Need to find the correct new leaf
                self.node_count -= 1
                if child.node_count <= 0: # The child it was just removed from should be deleted
                    self.set_child(child_string, None)
                
                if self.rect.collidepoint(n.boid.position): # The node fits somewhere within the current node
                    n.x = n.boid.position.x
                    n.y = n.boid.position.y
                    self.insert_node(n)
                    return False
                else:
                    if self.node_count < self.min_nodes: # Update the tree as it goes
                        self.reabsorb()
                    
                    return n
    
    def update_node_size(self, minimum, maximum):
        """Changes the minimum and maximum node sizes for the tree
        as the setting is dynamically altered."""

        self.min_nodes = minimum
        self.max_nodes = maximum
        if self.leaf:
            return
        
        # Propogate the change to its children
        for child in self.children.values():
            if child:
                child.update_node_size(minimum, maximum)
    
    def draw_grid(self, screen):
        """For display the node quadrants on the simulation screen."""

        pygame.draw.rect(screen, (255, 255, 255), (self.rect.left,
                                                   self.rect.top, 
                                                   self.rect.width + 1,
                                                   self.rect.height + 1), 1)
        if not self.leaf:
            for child in self.children.values():
                if child:
                    child.draw_grid(screen)

    def draw(self, screen):
        """For drawing the grid in the testing/example view."""

        if self.leaf:
            for node in self.nodes:
                pygame.draw.circle(screen, node.boid.color, (node.x, node.y), 2)
            
            pygame.draw.rect(screen, (255, 0, 0), (self.tl_corner, self.br_corner - self.tl_corner + Vector(1, 1)), 1)
        else:
            for child in self.children.values():
                if child is not None:
                    child.draw(screen)
            
            pygame.draw.rect(screen, (255, 0, 0), (self.tl_corner, self.br_corner - self.tl_corner + Vector(1, 1)), 1)


if __name__ == "__main__":
    import pygame
    import sys
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
                    # Add 200 boids to the tree
                    new_boids = create_boids(1280, 720, tree, 200)
                    boids += new_boids
                elif event.key == K_MINUS and boids:
                    for i in range(min(100, len(boids))):
                        boid = random.choice(boids)
                        tree.remove_boid(boid)
                        boids.remove(boid)
                elif event.key == K_RETURN:
                    # Create a random circle, to show finding nodes within a radius
                    position = Vector(random.randint(0, 1280), random.randint(0, 720))
                    circle = [position, random.randint(1, 1280)]
            elif event.type == MOUSEBUTTONDOWN:
                # Add a boid at the position of the click
                pos = Vector(pygame.mouse.get_pos())
                boid = Boid({}, pos)
                success = tree.insert_boid(boid)
                boids.append(boid)

        screen.fill((255, 255, 255))
        tree.draw(screen)
        if circle:
            in_nodes = tree.find_points_in_radius(circle[0], circle[1])
            for node in in_nodes:
                pygame.draw.circle(screen, (0, 255, 0), node.boid.position, 2)

            pygame.draw.circle(screen, (0, 200, 0), circle[0], circle[1], 2)
        
        pygame.display.update()