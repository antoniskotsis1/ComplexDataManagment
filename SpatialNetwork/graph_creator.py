class Node:

    def __init__(self, node_id, dimensions):
        self.__node_id = node_id
        self.__dimensions = dimensions
        self.__neighbours = []

    def add_neighbour(self, node_id, e_distance):
        self.__neighbours.append((node_id, e_distance))

    def get_node_id(self):
        return self.__node_id

    def get_dimension(self):
        return self.__dimensions

    def get_neighbours(self):
        return self.__neighbours


def get_next_node():
    line = nodes_file.readline().strip()
    if line:
        return line.split()


def get_next_edge():
    line = edges_file.readline().strip()
    if line:
        return line.split()[1:]


def create_nodes():
    total_road_nodes = []
    node_from_file = get_next_node()
    while node_from_file:
        node = Node(node_from_file[0], [node_from_file[1], node_from_file[2]])
        total_road_nodes.append(node)
        node_from_file = get_next_node()
    return total_road_nodes


def format_output_file():
    for node in total_nodes:
        node_id = node.get_node_id()
        distance = f'{node.get_dimension()[0]} {node.get_dimension()[1]}'
        neighbours = ""
        for neighbour in node.get_neighbours():
            neighbours += f'{neighbour[0]} {neighbour[1]} '
        output_file.write(f'{node_id} {distance} {neighbours.rstrip()}\n')


def connect_nodes():
    edge = get_next_edge()
    while edge:
        edge_node_id_1 = edge[0]
        edge_node_id_2 = edge[1]
        l_distance = edge[-1]
        total_nodes[int(edge_node_id_1)].add_neighbour(edge_node_id_2, l_distance)
        total_nodes[int(edge_node_id_2)].add_neighbour(edge_node_id_1, l_distance)
        edge = get_next_edge()


if __name__ == '__main__':
    nodes_file = open("CaliforniaRoadNetworkNodes")
    edges_file = open("CaliforniaRoadNetworkEdges")
    total_nodes = create_nodes()

    output_file = open("out.txt", "w")
    connect_nodes()

    format_output_file()

    # output_file.write(f'{node.get_node_id()} {node.get_dimension()}  {node.get_neighbours()}\n')
    # if index ==10:
    #     break
