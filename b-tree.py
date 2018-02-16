"""
    Developed by Kevin Khanda
    Resources, which were used during this implementation: https://www.geeksforgeeks.org/b-tree-set-1-introduction-2/
"""
from random import randint
import time


class BTreeNode(object):

    """
    BTreeNode constructor, where
    * is_leaf - shows is current node is leaf node
    * keys - slice with keys stored inside current node
    * children - slice with children of current node
    """
    def __init__(self, min_degree, is_leaf):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []

    """
    Method to split a given node by child index
    * node - node, which should be splitted
    * index - child index 
    """
    def children_split(self, min_degree, node, index):
        # processing new node
        new_node = BTreeNode(min_degree, node.is_leaf)
        new_node.keys = node.keys[min_degree:(2 * min_degree - 1)]

        j = 0
        if not node.is_leaf:
            while j < min_degree:
                new_node.children.insert(j, node.children[j + min_degree])
                j += 1

        j = len(self.keys)
        while j >= index + 1:
            self.children.insert(j + 1, self.children[j])
            j -= 1

        self.children.insert(index + 1, new_node)

        j = len(self.keys) - 1
        while j >= index:
            self.keys.insert(j + 1, self.keys[j])
            j -= 1

        self.keys.insert(index, node.keys[min_degree - 1])

    """
    Method to insert a key into a not full node
    * node - node, in which the key is inserted
    * key - key for insertion
    """
    def insert(self, min_degree, key):
        index = len(self.keys) - 1
        if self.is_leaf:
            while index >= 0 and self.keys[index] > key:
                self.keys.insert(index + 1, self.keys[index])
                index -= 1
            self.keys.insert(index + 1, key)
        else:
            while index >= 0 and self.keys[index] > key:
                index -= 1
            if len(self.children[index + 1].keys) == (2 * min_degree - 1):
                self.children_split(min_degree, self.children[index + 1], index + 1)
                if self.keys[index + 1] < key:
                    index += 1
            self.children[index + 1].insert(min_degree, key)

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.keys) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return str(self.keys)


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
        self.min_degree = min_degree
        self.root = None

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
    Insert key into tree
    * key - term, which should be inserted
    """
    def insert(self, key):
        if self.root is None:
            self.root = BTreeNode(self.min_degree, True)
            self.root.keys.append(key)
        else:
            # if condition 2 is violated, we should split the node
            if len(self.root.keys) == (2 * self.min_degree - 1):
                new_node = BTreeNode(self.min_degree, False)
                # insert current root as a child for new node
                new_node.children.insert(0, self.root)
                # splitting new node
                new_node.children_split(self.min_degree, self.root, 0)
                index = 0
                if new_node.keys[0] < key:
                    index += 1
                new_node.children[index].insert(self.min_degree, key)
                self.root = new_node
            # if condition 2 holds, insert key into a root node
            else:
                self.root.insert(self.min_degree, key)


def b_tree_build_index(long_list):
    b_tree = BTree(16)
    for i in long_list:
        b_tree.insert(i)
    return b_tree


# generate a list L of items with len(L) = 20 000 # each item has a key() and data() methods
list_size = 20000
a_long_list = [x for x in range(0, list_size)]

# a random item from the list (L.index(item) > len(L) / 2)
item = a_long_list[randint(0, 20000)]


# a naive sequential search for baseline perfomance check
def naive_search(l, item):
    for i in l:
        if i == item:
            return i


# measure naive time
start = time.time()
naive_search(a_long_list, item)
end = time.time()
t_no_idx = end - start
# build index on list
idx_set = b_tree_build_index(a_long_list)
# measure index lookup time
start = time.time()
idx_set.search(item, None)
end = time.time()
t_idx = end - start
print(t_idx < t_no_idx)
# make sure that indexed operation is faster
assert t_idx < t_no_idx, 'Your implementation sucks!'
