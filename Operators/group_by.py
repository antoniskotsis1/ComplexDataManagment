# AM: 3018 Name: Kotsis Antonios

def create_list(file):
    x = file.readline().strip()
    ret_list = []
    while x:
        x = x.split('\t')
        try:
            ret_list.append((x[0], x[1]))
        except IndexError:
            exit('Values should be separated by -> \\t')
        x = file.readline().strip()
    return ret_list if ret_list else []


def empty_lists(l1, l2, result):
    while l1:
        result.append(l1[0])
        l1.remove(l1[0])
    while l2:
        result.append(l2[0])
        l2.remove(l2[0])


def merge(first_list, second_list):
    """Basic merge algorithms for two given lists"""
    result_list = []

    def check_for_group():
        """Inner function,so that it has access to merges' local variables,
        that checks for groups"""
        if first_list[0][0] == second_list[0][0]:
            try:
                result = first_list[0][0], str(int(first_list[0][1]) + int(second_list[0][1]))
            except ValueError:
                result = first_list[0][0], str(float(first_list[0][1]) + float(second_list[0][1]))
            result_list.append(result)
            first_list.remove(first_list[0])
            second_list.remove(second_list[0])
            return True
        return False

    while first_list and second_list:
        if first_list[0] > second_list[0]:
            if not check_for_group():
                result_list.append(second_list[0])
                second_list.remove(second_list[0])
        else:
            if not check_for_group():
                result_list.append(first_list[0])
                first_list.remove(first_list[0])
    empty_lists(first_list, second_list, result_list)
    return result_list


def create_output_file(arr):
    """Writes the result to the .tsv file"""
    for i in arr:
        output_file.write(f'{i[0]}\t{i[1]}\n')


def merge_sort(arr):
    """Classic divide and conquer merge-sort algorithm"""
    if len(arr) == 1:
        return arr
    middle = len(arr) // 2
    first_half = merge_sort(arr[:middle])
    second_half = merge_sort(arr[middle:])
    return merge(first_half, second_half)


def close_files():
    unsorted_r_file.close()
    output_file.close()


def open_files():
    r = open('R.tsv')
    output = open('Rgroupby.tsv', 'w')
    return r, output


if __name__ == '__main__':
    unsorted_r_file, output_file = open_files()
    r_list = create_list(unsorted_r_file)
    final_result = merge_sort(r_list)
    create_output_file(final_result)
