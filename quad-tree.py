from pygame.math import Vector2 as Vector

class Node:
    def __init__(self, x, y, boid):
        self.x = x
        self.y = y
        self.boid = boid


class QuadTree:
    def __init__(self, top_left, bottom_right, node=None, parent=None):
        self.node = node
        self.parent = parent
        self.leaf = True
        self.tl_corner = top_left
        self.br_corner = bottom_right
        self.center = Vector((self.tl_corner.x + self.br_corner.x) // 2, (self.tl_corner.y + self.br_corner.y) // 2)
        self.children = {
            "tl":None,
            "tr":None,
            "bl":None,
            "br":None
        }
    
    def is_leaf(self):
        return self.leaf
    
    def get_child(self, n):
        """Find which child quad the node is inside."""

        x, y = self.center
        if n.x <= x:
            if n.y <= y:
                return "tl"
            else:
                return "bl"
        else:
            if n.pos.y <= y:
                return "tr"
            else:
                return "br"

    def remove(self, n):
        """Remove a node from the tree and, if necessary, remove leaves until it reaches
        a branch to remove unecessary branches."""

        if self.is_leaf():
            if self.node.boid == n.boid: # Make sure this leaf node is the correct one
                self.node = None
                return True # Removed the node
            else:
                return False # Did not remove the node
        
        elif not self.is_leaf():
            child_string = self.get_child(n) # Find which child the node is in
            # Find how many children are in the current node
            total_children = sum([int(c is not None) for c in self.children.values()])

            if self.children[child_string].remove(n) and total_children > 1:
                # The node was successfully found and removed, but
                # don't delete this node because there are other children connected
                self.children[child_string] = None
                total_children -= 1
            
            if total_children == 1: # This was a node of two, now one, so it can be simplified
                for child_string, child in self.children.items():
                    if child and child.is_leaf():
                        # There is one child and it's a leaf, so it can be simplified
                        # If it weren't a leaf, there are multiple leaves connected further down
                        self.node = child.node # Set the current node to the child's node
                        self.leaf = True
                        self.children[child_string]
                        return False
            
            return False

    def insert(self, n):
        if self.node is None and self.is_leaf():  # Only occurs if it's the first insert
            self.node = n
            return

        if self.leaf:
            # This is the bottom of the branch, so a new node needs to be made to make room
            # The current leaf is moved into it
            if self.node.x <= self.center.x:
                if self.node.y <= self.center.y:
                    self.children["tl"] = QuadTree(Vector(*self.tl_corner),
                                                   Vector(self.center),
                                                   self.node,
                                                   self)
                else:
                    self.children["bl"] = QuadTree(Vector(self.tl_corner.x, self.center.y + 1),
                                                   Vector(self.center.x, self.br_corner.y),
                                                   self.node,
                                                   self)
            else:
                if self.node.pos.y <= self.center.y:
                    self.children["trt"] = QuadTree(Vector(self.center.x + 1, self.tl_corner.y),
                                                   Vector(self.br_corner.x, self.center.y),
                                                   self.node,
                                                   self)
                else:
                    self.children["brt"] = QuadTree(Vector(self.center + Vector(1, 1)),
                                                   Vector(self.br_corner),
                                                   self.node,
                                                   self)
            
            self.node = None
            self.leaf = False
        
        if abs(self.tl_corner.x - self.br_corner.x) >= 4 and abs(self.tl_corner.y - self.br_corner.y) >= 4:
            # There's room for more subtrees 
            if n.x <= self.center.x:
                # Left side
                if n.y <= self.center.y:
                    child_string = "tlt"
                    if self.children[child_string] == None:
                        self.children[child] = N_Quad_Tree(Vector2(self.tl.x, self.tl.y), Vector2(self.center.x+1, self.center.y+1), n, self)
                        return
                    return self.children[child].insert(n)
                else:
                    child = "blt"
                    if self.children[child] == None:
                        self.children[child] = N_Quad_Tree(Vector2(self.tl.x, self.center.y), Vector2(self.center.x+1, self.br.y), n, self)
                        return
                    return self.children[child].insert(n)
            else:
                if n.pos.y <= self.center.y:
                    child = "trt"
                    if self.children[child] == None:
                        self.children[child] = N_Quad_Tree(Vector2(self.center.x, self.tl.y), Vector2(self.br.x, self.center.y+1), n, self)
                        return
                    return self.children[child].insert(n)
                else:
                    child = "brt"
                    if self.children[child] == None:
                        self.children[child] = N_Quad_Tree(Vector2(self.center.x, self.center.y), Vector2(self.br.x, self.br.y), n, self)
                        return
                    return self.children[child].insert(n)
        else:
            return


if __name__ == '__main__':
    tree = QuadTree(Vector(0, 0), Vector(1000, 1000))