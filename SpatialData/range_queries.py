# Kotsis Antonios AM 3018
import argparse
import ast


class Rtree:
    def __init__(self):
        self.nodes = []

    def add_node(self, node_id, data, isnonleaf, root):
        """Method that creates new Node objects and ads them to the tree"""
        node = Node(node_id, data, isnonleaf, root)
        self.nodes.append(node)

    def get_node_by_id(self, node_id):
        """Accessor method to get a node based on the given id"""
        for node in self.nodes:
            if node.id == node_id:
                return node

    def is_leaf(self, n_id):
        """Method that returns if a node is leaf or not"""
        for node in self.nodes:
            if node.id == n_id:
                return node.is_leaf()

    def root(self):
        """Method that return the root of the tree"""
        for node in self.nodes:
            if node.is_root:
                return node


class Node:
    def __init__(self, node_id, data, isnonleaf, is_root):
        self.id = node_id
        self.data = data
        self.isnonleaf = isnonleaf
        self.is_root = is_root

    def get_data(self):
        """Accessor method that returns node's data"""
        return self.data

    def is_leaf(self):
        """Accessor method that returns if a node is leaf or not"""
        return self.isnonleaf


def construct_r_tree(tree_list):
    """Construct the Rtree based on the given list with all nodes"""
    tree = Rtree()
    for index, node in enumerate(tree_list):
        isnonleaf = node[0]
        node_id = node[1]
        data = node[-1]
        tree.add_node(node_id, data, isnonleaf, True if index == 0 else None)
    return tree


def create_r_tree():
    """Creates a list containing the tree nodes and calls construct_r_tree to create it."""
    tree_list = []
    node = r_tree_file.readline()
    while node:
        tree_list.append(ast.literal_eval(node))
        node = r_tree_file.readline()
    return construct_r_tree(list(reversed(tree_list)))


def is_overlapping(w, mbr):
    """Function that decides whether an mbr is overlapping with the search query window"""
    window_x_low, window_y_low, window_x_high, window_y_high = w
    mbr_x_low, mbr_x_high, mbr_y_low, mbr_y_high = mbr
    case1 = window_y_low <= mbr_y_low <= window_y_high and window_x_high >= mbr_x_high >= window_x_low
    case2 = window_y_low <= mbr_y_high <= window_y_high and window_x_high >= mbr_x_high >= window_x_low
    case3 = window_y_low <= mbr_y_high <= window_y_high and window_x_high >= mbr_x_low >= window_x_low
    case4 = window_y_low <= mbr_y_low <= window_y_high and window_x_high >= mbr_x_low >= window_x_low
    return case1 or case2 or case3 or case4


def contains(w, mbr):
    """Function that decides whether an mbr contains the search query window"""
    window_x_low, window_y_low, window_x_high, window_y_high = w
    x_min, x_max, y_min, y_max = mbr
    x_axis = (x_max >= window_x_high) and (x_min <= window_x_low)
    y_axis = (y_min <= window_y_low) and (y_max >= window_y_high)
    return x_axis and y_axis


def is_inside(w, mbr):
    """Function that decides whether an mbr is inside the search query window"""
    window_x_low, window_y_low, window_x_high, window_y_high = w
    mbr_x_low, mbr_x_high, mbr_y_low, mbr_y_high = mbr
    x_axis = (window_x_high >= mbr_x_high) and (window_x_low <= mbr_x_low)
    y_axis = (window_y_low <= mbr_y_low) and (window_y_high >= mbr_y_high)

    return x_axis and y_axis


def range_query(window, tree, node, result):
    """Recursive function that traverses the Rtree"""
    window_x_low, window_y_low, window_x_high, window_y_high = window
    if node.isnonleaf:
        for mbr in node.data:
            node_id = mbr[0]
            x_low, x_high, y_low, y_high = mbr[-1]
            if ((window_x_high >= x_low) or (window_x_high <= x_high)) and \
                    ((window_y_low <= y_high) or (window_y_high <= y_low)):
                range_query(window, tree, tree.get_node_by_id(node_id), result)
    else:
        for data in node.data:
            if is_inside(window, data[-1]) or is_overlapping(window, data[-1]) or contains(window, data[-1]):
                result.append(data[0])


def send_queries(r_tree):
    """Function that sends the data from the queries in the recursive range_query function"""
    ress = open("range_queries_results.txt", "w")
    w = [float(i) for i in range_queries.readline().split()]
    count = 0
    while w:
        res = []
        range_query(w, r_tree, r_tree.root(), res)
        print(f"{count} ({len(res)}): {', '.join(map(str, res))}")
        ress.write(f"{count} ({len(res)}): {', '.join(map(str, res))}\n")
        w = [float(i) for i in range_queries.readline().split()]
        count += 1


def main():
    r_tree = create_r_tree()

    send_queries(r_tree)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Range Queries")
    parser.add_argument("Rtree", metavar='rtree_file', help="file containing the r-tree from partA")
    parser.add_argument("RangeQueries", metavar='queries_file', help="file containing the range queries")
    args = parser.parse_args()

    r_tree_file = open(args.Rtree)
    range_queries = open(args.RangeQueries)

    main()

