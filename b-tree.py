"""
    Developed by Kevin Khanda
    Resources, which were used during this implementation: https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/
"""
from random import randint


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

    # def __str__(self):
    #     return 'node with keys: {0} and children: \n\t{1}'\
    #                .format(self.keys, [child.__str__() for child in self.children])

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.keys) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return self.keys

    # if self.is_leaf:
    #     return 'Leaf node with\n\tkeys: {0}\n\tand children: {1}\n'.format(self.keys,
    #                                                                        [child.keys for child in self.children])
    # else:
    #     return 'Internal node with\n\tkeys: {0}\n\tand children with keys: {1}\n'.format(self.keys,
    #                                                                                      [child.keys for child in
    #                                                                                       self.children])
"""
B-Tree properties:
* all leaves are at the same level
* all keys in nodes are sorted in ascending order
* complexity of all operations is O(logN)
* tree is defined by minimum degree (min_degree field)
* len(node.keys) >= min_degree - 1;  (condition 1)
* len(root.keys) >= 1;  (condition 2)
* len(node.keys) <= 2 * min_degree - 1;  (condition 3) 
* len(node.children) == len(node.keys) + 1;  (condition 4)
"""


class BTree(object):
    """
    BTree constructor, where
    * min_degree - minimum degree amount (number of child nodes that are allowed)
    """

    def __init__(self, min_degree):
        self.root = BTreeNode(True)
        self.min_degree = min_degree

    def __str__(self):
        return str(self.root)

    """
    Search BTree for the given key
    * key - the term, for which lookup is made
    * node - node, where the search is made (could be None, in this case the entire tree is searched)
    """

    def search(self, key, node):
        # checking if node is specified (it may be None)
        if node is not None:
            index = 0
            # searching for key index
            while index < len(node.keys) and key > node.keys[index]:
                index += 1
            # if key was found
            if index < len(node.keys) and key == node.keys[index]:
                return node, index
            # if node is leaf and no keys matching, there are no matching at all
            elif node.is_leaf:
                return None
            # if nothing was found in internal node, search in i-th child node
            else:
                return self.search(key, node.children[index])
        # if node is None, search the entire tree
        else:
            return self.search(key, self.root)

    """
    Method to split a given node by child index
    * node - node, which should be splitted
    * index - child index 
    """

    def _children_split(self, node, index):
        min_degree = self.min_degree
        child = node.children[index]
        new_node = BTreeNode(child.is_leaf)
        # insert new node as a child to given node
        node.children.insert(index + 1, new_node)
        # insert child's middle key into node keys
        node.keys.insert(index, child.keys[min_degree - 1])
        # put child's right keys to new node
        new_node.keys = child.keys[min_degree: 2 * min_degree - 1]
        # reduce child's keys only to left keys
        child.keys = child.keys[0: min_degree - 1]

        # splitting child's children if child is not leaf node
        if not child.is_leaf:
            new_node.children = child.children[min_degree: 2 * min_degree]
            child.children = child.children[0: min_degree - 1]

    """
    Method to insert a key into a not full node
    * node - node, in which the key is inserted
    * key - key for insertion
    """

    def _insert(self, node, key):
        index = len(node.keys) - 1
        # if node is leaf node, then just insert a key
        if node.is_leaf:
            node.keys.append(0)
            # while key is less than current indexed element, shift all elements right and decrement index
            while index >= 0 and key < node.keys[index]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            # inserting key on next element (if current is less than 'key' or index is 0)
            node.keys[index + 1] = key
        # otherwise, insert a new node and then insert a key
        else:
            # decreasing index
            while index >= 0 and key < node.keys[index]:
                index -= 1
            # if child is full, split the node
            if len(node.children[index].keys) == (2 * self.min_degree - 1):
                self._children_split(node, index)
                if key > node.keys[index]:
                    index += 1
            # insert key to the child node
            self._insert(node.children[index], key)

    """
    Insert key into tree
    * key - term, which should be inserted
    """

    def insert(self, key):
        root = self.root
        # if condition 2 is violated, we should split the node
        if len(root.keys) == (2 * self.min_degree - 1):
            new_node = BTreeNode(False)
            self.root = new_node
            # insert current root as a child for new node
            new_node.children.insert(0, root)
            # splitting new node
            self._children_split(new_node, 0)
            # inserting key to new node
            self._insert(new_node, key)
        # if condition 2 holds, insert key into a root node
        else:
            self._insert(root, key)


b_tree = BTree(2)
for i in range(0, 100):
    b_tree.insert(randint(0, 150))
print(b_tree)
