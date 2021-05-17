# Kotsis Antonios AM 3018
import argparse
import ast
import heapq
import math


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
        return not self.isnonleaf


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


def distance(q, mbr):
    """Returns the min distance between a point and an mbr"""
    if not mbr:
        return math.inf
    x, y = q
    x_low, x_high, y_low, y_high = mbr
    if x < x_low:
        dx = x_low - x
    elif x > x_high:
        dx = x_high - x
    else:
        dx = 0
    if y < y_low:
        dy = y_low - y
    elif y > y_high:
        dy = y_high - y
    else:
        dy = 0

    return math.sqrt(dx * dx + dy * dy)


def get_next_bf_nn(q, heap_Q, r_tree):
    """Best First Search nearest neighbor algorithm"""
    nn = None
    top_q_mbr = heap_Q[0][1][-1]
    while heap_Q and distance(q, top_q_mbr) < distance(q, nn[-1] if nn else nn):
        top = heapq.heappop(heap_Q)
        e = r_tree.get_node_by_id(top[1][0])
        if top[-1] == 'node' and not e.is_leaf():
            for data in e.data:
                if distance(q, data[-1]) < distance(q, nn[-1] if nn else nn):
                    heapq.heappush(heap_Q, (distance(q, data[-1]), data, 'node'))
            top_q_mbr = heap_Q[0][1][-1]
        elif top[-1] == 'node' and e.is_leaf:
            for data in e.data:
                if distance(q, data[-1]) < distance(q, nn[-1] if nn else nn):
                    heapq.heappush(heap_Q, (distance(q, data[-1]), data, 'obj'))
            top_q_mbr = heap_Q[0][1][-1]
        elif top[-1] == 'obj':
            if distance(q, top[1][-1]) < distance(q, nn[-1] if nn else nn):
                heapq.heappush(heap_Q, (distance(q, top[1][-1]), top[1], 'obj'))
                nn = top[1]
            top_q_mbr = heap_Q[0][1][-1]
    return nn


def bf_nn_search(q, r_tree):
    """Incremental Best First Search nearest neighbor algorithm. Calls BF-NN as many times as the given k
    to return the k closest neighbours"""
    res = []
    _heap = []
    root = r_tree.root()
    for node_data in root.data:
        heapq.heappush(_heap, (distance(q, node_data[-1]), node_data, 'node'))
    while len(res) < k:
        nn = get_next_bf_nn(q, _heap, r_tree)
        heapq.heappop(_heap)
        res.append(nn)
    return [i[0] for i in res]


def send_k_nn_queries(r_tree):
    """Send the queries from NN-queries.txt to the algorithm and prints the result."""
    output = open(f"k_NNqueries_results.txt", "w")
    for line_count, q in enumerate(kNN_queries):
        query = [float(coords) for coords in q.strip().split()]
        result = bf_nn_search(query, r_tree)
        output.write(f"{line_count}: {', '.join((map(str, result)))}\n")
        print(f"{line_count}: {', '.join((map(str, result)))}")


def main():
    r_tree = create_r_tree()
    send_k_nn_queries(r_tree)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="kNN Queries")
    parser.add_argument("Rtree", metavar='rtree_file', help="file containing the r-tree from partA")
    parser.add_argument("NNqueries", metavar='queries_file', help="file containing the NN queries")
    parser.add_argument("k", metavar='k', help='The number of the closest neighbours')
    args = parser.parse_args()

    r_tree_file = open(args.Rtree)
    kNN_queries = open(args.NNqueries)
    k = int(args.k)

    main()
