import time
import ast


class Rtree:
    def __init__(self):
        self.nodes = []

    def add_node(self, node_id, data, isnonleaf, root):
        node = Node(node_id, data, isnonleaf, root)
        self.nodes.append(node)

    def get_node_data(self, n_id):
        for node in self.nodes:
            if node.id == n_id:
                return node.get_data()

    def get_node_by_id(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node

    def is_leaf(self, n_id):
        for node in self.nodes:
            if node.id == n_id:
                return node.is_leaf()

    def root(self):
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
        return self.data

    def is_leaf(self):
        return self.isnonleaf


def string_to_list(string):
    return ast.literal_eval(string)


def construct_r_tree(tree_list):
    tree = Rtree()
    for index, node in enumerate(tree_list):
        isnonleaf = node[0]
        node_id = node[1]
        data = node[-1]
        tree.add_node(node_id, data, isnonleaf, True if index == 0 else None)
    return tree


def create_r_tree():
    tree_list = []
    node = r_tree_file.readline()
    while node:
        tree_list.append(string_to_list(node))
        node = r_tree_file.readline()
    return construct_r_tree(list(reversed(tree_list)))


def is_adjacent(w, mbr):
    query_x_low, query_y_low, query_x_high, query_y_high = map(float, w)
    mbr_x_low, mbr_x_high, mbr_y_low, mbr_y_high = mbr
    x_axis = query_x_low == mbr_x_high or query_y_high == mbr_y_low
    x_axis1 = query_y_low <= mbr_y_high <= query_y_high+mbr_y_high

    y_axis = query_y_low == mbr_y_high or query_y_high == mbr_y_low
    y_axis1 = query_x_low <= mbr_x_high <= query_x_high+mbr_x_high

    return (x_axis and x_axis1) or (y_axis1 and y_axis)


def intersection(w, mbr):
    query_x_low, query_y_low, query_x_high, query_y_high = map(float, w)
    mbr_x_low, mbr_x_high, mbr_y_low, mbr_y_high = mbr
    x_axis = (query_x_high >= mbr_x_low) or (query_x_high <= mbr_x_high)
    y_axis = (query_y_low <= mbr_y_high) or (query_y_high <= mbr_y_low)

    return x_axis and y_axis


def contains(w, mbr):
    window_x_low, window_y_low, window_x_high, window_y_high = map(float, w)
    x_min, x_max, y_min, y_max = mbr
    x_axis = (x_max >= window_x_high) and (x_min <= window_x_low)
    y_axis = (y_min <= window_y_low) and (y_max >= window_y_high)
    return x_axis and y_axis


def is_inside(w, mbr):
    query_x_low, query_y_low, query_x_high, query_y_high = map(float, w)
    mbr_x_low, mbr_x_high, mbr_y_low, mbr_y_high = mbr
    x_axis = (query_x_high >= mbr_x_high) and (query_x_low <= mbr_x_low)
    y_axis = (query_y_low <= mbr_y_low) and (query_y_high >= mbr_y_high)

    return x_axis and y_axis


def equals(w, mbr):
    window_x_low, window_y_low, window_x_high, window_y_high = map(float, w)
    x_min, x_max, y_min, y_max = mbr
    if window_x_high == x_max and window_y_high == y_max and window_x_low == x_min and window_y_low == y_min:
        return True
    return False


def range_query(window, tree, node, result):
    window_x_low, window_y_low, window_x_high, window_y_high = map(float, window)

    if node.isnonleaf:
        for mbr in node.data:
            node_id = mbr[0]
            x_low, x_high, y_low, y_high = mbr[-1]
            if ((window_x_high >= x_low) or (window_x_high <= x_high)) and \
                    ((window_y_low <= y_high) or (window_y_high <= y_low)):
                range_query(window, tree, tree.get_node_by_id(node_id), result)

    else:
        for data in node.data:
            if is_inside(window, data[-1]):
                result.append(data[0])


def send_queries(r_tree):
    w = range_queries.readline().split()
    count = 0
    while w:
        res = []
        range_query(w, r_tree, r_tree.root(), res)
        print(f"{count} ({len(res)}): {','.join(map(str, res))}")
        w = range_queries.readline().split()
        count += 1


def main():
    r_tree = create_r_tree()
    send_queries(r_tree)


if __name__ == '__main__':
    st = time.time()
    r_tree_file = open("Rtree.txt", 'r')
    range_queries = open("Rqueries.txt")
    main()
    end = time.time()
    print(end - st)
