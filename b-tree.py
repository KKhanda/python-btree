"""
    Created by Kevin Khanda
"""


class BTreeNode(object):
    """
    BTreeNode constructor, where
    * is_leaf - shows is current node is leaf node
    * keys - slice with keys stored inside current node
    * children - slice with children of current node
    """
    def __init__(self, is_leaf):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

    """
    Override method '__str__' for node representation
    """
    def __str__(self):
        if self.is_leaf:
            return 'Leaf node with keys: {0} and children: {1}'.format(self.keys, self.children)
        else:
            return 'Internal node with keys: {0} and children: {1}'.format(self.keys, self.children)


class BTree(object):
    """
    
    """
    def __init__(self, min_degree):
        self.root = BTreeNode(True)
        self.min_degree = min_degree

    """
    Search BTree for the given key
    * key - the term, for which lookup is made
    * node - node, where the search is made (could be None, in this case the entire tree is searched)
    """
    def search(self, key, node):
        # checking if node is specified (it may be None)
        if node is not None:
            i = 0
            # searching for key index
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            # if key was found
            if i < len(node.keys) and key == node.keys[i]:
                return node, i
            # if node is leaf and no keys matching, there are no matching at all
            elif node.is_leaf:
                return None
            # if nothing was found in internal node, search in i-th child node
            else:
                return self.search(key, node.children[i])
        # if node is None, search the entire tree
        else:
            return self.search(key, self.root)
