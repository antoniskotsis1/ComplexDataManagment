
class Node:

    def __init__(self, node_id, dimensions, neighbours):
        self.__node_id = node_id
        self.__dimensions = dimensions
        self.__neighbours = neighbours
        self.visited = False

    def __lt__(self, other):
        """Needed for priority queue's comparisons"""
        pass

    def get_node_id(self):
        return int(self.__node_id)

    def get_dimensions(self):
        return map(float, self.__dimensions)

    def get_neighbours(self):
        return self.__neighbours

    def get_visited(self):
        return self.visited

    def set_visited(self, visited):
        self.visited = visited


def create_graph():
    total_nodes = []
    node_info = graph_file.readline().strip().split()
    while node_info:
        node_id = node_info[0]
        node_coordinates = node_info[1:3]
        neighbours = [[node_info[3:][i], node_info[3:][i + 1]] for i in range(0, len(node_info[3:]) - 1, 2)]
        node = Node(node_id, node_coordinates, neighbours)
        total_nodes.append(node)
        node_info = graph_file.readline().strip().split()
    for node in total_nodes:
        for neighbour in node.get_neighbours():
            neighbour[0] = total_nodes[int(neighbour[0])]
    return total_nodes


if __name__ == '__main__':
    graph_file = open("out.txt","r")
    create_graph()