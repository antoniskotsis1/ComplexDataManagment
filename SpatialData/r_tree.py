import argparse
from pymorton import interleave_latlng
import time


def second_element(elem):
    return elem[1]


def get_mbr_values(cords_dict):
    x_max = max(cords_dict['x'])
    x_min = min(cords_dict['x'])
    y_max = max(cords_dict['y'])
    y_min = min(cords_dict['y'])
    return [x_min, x_max, y_min, y_max]


def delete_z_value(element):
    return element[0], element[-1]


def calculate_mbrs():
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
        # mbrs[info_list[0]] = mbr
        center_x = (mbr[0] + mbr[1]) / 2
        center_y = (mbr[2] + mbr[3]) / 2
        sorted_mbrs.append((mbr_id, interleave_latlng(center_y, center_x), mbr))
        info_list = offset.readline().split(',')
    return list(map(delete_z_value, sorted(sorted_mbrs, key=second_element)))


def main():
    mbrs = calculate_mbrs()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="R-Tree creation throw bulk loading")
    # parser.add_argument("coordinates", metavar='coors_file', help="file containing polygon's coordinates")
    # parser.add_argument("offsets", metavar='offset_file', help="file containing coordinate offsets")
    # args = parser.parse_args()

    # cords = open(args.coordinates)
    # offset = open(args.offsets)

    cords = open('coords.txt')
    offset = open('offsets.txt')



    st = time.time()
    main()
    en = time.time()
    print(f"time taken: {en - st}")
