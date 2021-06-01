import argparse
import heapq
import math


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


def euclidean_distance(init_node, target_node):
    x2, y2 = target_node.get_dimensions()
    x1, y1 = init_node.get_dimensions()
    return math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))


def exists_in_search_frontier(sf, node):
    for distance, sf_node in sf:
        if node == sf_node:
            print(f"mode {node} already in heap with: {distance}")
            return True
    else:
        return False


def update_heap(search_frontier, neighbour, heuristic_cost):
    remove_value = ()
    for distance, sf_node in search_frontier:
        if neighbour == sf_node:
            if distance > heuristic_cost:
                remove_value = (distance, sf_node)
            break
    else:
        heapq.heappush(search_frontier, (heuristic_cost, neighbour))

    if remove_value:
        search_frontier.remove(remove_value)
        heapq.heapify(search_frontier)
        heapq.heappush(search_frontier, (heuristic_cost, neighbour))


def shortest_path_search_algorithm(algorithm, source_node, target_node):
    for i in graph:
        i.set_visited(False)
    target_node = graph[target_node]
    source_node = graph[source_node]
    search_frontier = []
    spd = {i: math.inf for i in graph}
    path = {i: [source_node] for i in graph}
    heapq.heappush(search_frontier, (0, source_node))
    spd[source_node] = 0
    loop_count = 0
    path[target_node].append(source_node)
    while search_frontier:
        loop_count += 1
        current_distance, current_node = heapq.heappop(search_frontier)
        current_node.set_visited(True)
        if current_node.get_node_id() == target_node.get_node_id():
            present_results(algorithm, loop_count, path.get(target_node), spd.get(target_node))
            return
        for neighbour, edge_weight in current_node.get_neighbours():

            if not neighbour.get_visited():
                if spd.get(neighbour) > spd.get(current_node) + float(edge_weight):

                    path[neighbour] = path.get(current_node).copy()
                    path[neighbour].append(neighbour)
                    spd[neighbour] = float(edge_weight) + spd.get(current_node)

                    if algorithm == "dijkstra":
                        update_heap(search_frontier, neighbour, spd.get(neighbour))
                    else:
                        heuristic_cost = spd.get(neighbour) + euclidean_distance(neighbour, target_node)
                        update_heap(search_frontier, neighbour, heuristic_cost)


def present_results(algorithm, loop_count, path, path_distance):
    if algorithm == "dijkstra":
        print("--Dijkstra Results--")
    else:
        print("--A* Results--")
    print(f"Shortest Path Length: {len(path)}")
    print(f"Shortest Path Distance: {path_distance}")
    print(f"Shortest Path Detected: {list(map(lambda x: x.get_node_id(), path))}")
    print(f"Number Of Visited Nodes: {loop_count}\n")


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
    graph_file = open("out.txt")
    graph = create_graph()
    graph_file.close()

    parser = argparse.ArgumentParser(description="Dijkstra and A* algorithms")
    parser.add_argument("source_node", metavar='source_node', help="starting node of the path")
    parser.add_argument("target_node", metavar='target_node', help="target node")

    args = parser.parse_args()

    shortest_path_search_algorithm("dijkstra", int(args.source_node), int(args.target_node))
    shortest_path_search_algorithm("a*", int(args.source_node), int(args.target_node))
