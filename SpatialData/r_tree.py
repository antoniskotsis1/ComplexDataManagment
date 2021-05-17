# Kotsis Antonios AM 3018
import argparse
from pymorton import interleave_latlng
from math import ceil


def nodes_mbr(list_of_mbrs):
    x_cor = {'x': [], 'y': []}
    for i in list_of_mbrs:
        for index, values in enumerate(i[-1]):
            if index < 2:
                x_cor['x'].append(values)
            else:
                x_cor['y'].append(values)
    return get_mbr_values(x_cor)


def get_new_mbr(nodes):
    res = []
    for node in nodes:
        node_id = node[1]
        res.append([node_id, nodes_mbr(node[-1])])
    return res


def check_last_node(nodes, level, min_capacity):
    print(f"{len(nodes)} nodes at level {level}")
    if len(nodes[-1][-1]) < min_capacity and len(nodes) != 1:
        x = nodes[-2][-1][-(min_capacity - len(nodes[-1][-1])):]  # get the last n element from the exact
        # prev so that len of curr node becomes equal to 8
        y = nodes[-1][-1]
        nodes[-2][-1] = nodes[-2][-1][:-(min_capacity - len(nodes[-1][-1]))]
        nodes[-1][-1] = x + y


def create_tree(mbrs, node_capacity, level, start_node_id, min_capacity):
    if len(mbrs) == 1:
        return
    res = []
    node_id = 0
    mbr = 0
    nodes = ceil(len(mbrs) / node_capacity)
    for node_id in range(nodes):
        temp = []

        if len(mbrs) > node_capacity:
            group = node_capacity
        else:
            group = len(mbrs)

        for mbr in range(group):
            temp.append(mbrs[mbr])
        mbrs = mbrs[mbr+1:]
        if level != 0:
            new = get_new_mbr(temp)
            res.append([1, node_id + start_node_id, new])
        else:
            res.append([0 if level == 0 else 1, node_id + start_node_id, temp])
    check_last_node(res, level, min_capacity)
    for i in res:
        r_t.write(str(i)+'\n')
    create_tree(res, 20, level + 1, node_id + start_node_id + 1, min_capacity)  # create the parent nodes


def get_mbr_values(cords_dict):
    x_max = max(cords_dict['x'])
    x_min = min(cords_dict['x'])
    y_max = max(cords_dict['y'])
    y_min = min(cords_dict['y'])
    return [x_min, x_max, y_min, y_max]


def calculate_original_mbrs():
    cords_dict = {'x': [], 'y': []}
    sorted_mbrs = []
    info_list = offset.readline().split(',')
    while len(info_list) == 3:
        mbr_id = int(info_list[0])
        start = int(info_list[1])
        end = int(info_list[-1].strip())
        for i in range(start, end + 1):
            x, y = cords.readline().strip().split(',')
            cords_dict['x'].append(float(x))
            cords_dict['y'].append(float(y))
        mbr = get_mbr_values(cords_dict)
        cords_dict['x'].clear()
        cords_dict['y'].clear()
        center_x = (mbr[0] + mbr[1]) / 2
        center_y = (mbr[2] + mbr[3]) / 2
        sorted_mbrs.append([mbr_id, interleave_latlng(center_y, center_x), mbr])
        info_list = offset.readline().split(',')
    return list(map(lambda elem: [elem[0], elem[-1]], sorted(sorted_mbrs, key=lambda el: el[1])))


def main():
    mbrs = calculate_original_mbrs()
    min_capacity = 8
    max_capacity = 20
    start_node_id = 0
    level = 0
    create_tree(mbrs, max_capacity, level, start_node_id, min_capacity)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="R-Tree creation throw bulk loading")
    parser.add_argument("coordinates", metavar='coords_file', help="file containing polygon's coordinates")
    parser.add_argument("offsets", metavar='offset_file', help="file containing coordinate offsets")
    args = parser.parse_args()

    cords = open(args.coordinates)
    offset = open(args.offsets)

    r_t = open("Rtree.txt", "w")

    main()


