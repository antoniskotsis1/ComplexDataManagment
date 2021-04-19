# AM: 3018 name: Kotsis Antonios

def move_pointer(reader):
    """Moves every pointer to the next line.
    Returns either a tuple of the next line or None if there are no other values"""
    x = reader.readline().strip()
    if x:
        x = x.split('\t')
        try:
            result = x[0], int(x[1])
        except ValueError:
            result = x[0], float(x[1])
        return result
    return None


def write_file(r0, r1, s1):
    """Writes the outcome of the join operation to file RjoinS.tsv"""
    output_file.write(f'{r0}\t{r1}\t{s1}\n')


def check_previous(visited, pointer):
    """Checks for values already read by merge-join algorithm using a buffer
     to avoid backtracking and reading over and over again the same tuples"""
    if visited and visited[-1][0] == pointer[0]:
        for i in visited:
            write_file(pointer[0], pointer[1], i[1])


def clear_buffer():
    """Clears buffer and calculates max buffer length"""
    global buffer, max_buffer_size
    if len(buffer) > max_buffer_size:
        max_buffer_size = len(buffer)
    buffer.clear()


def open_files():
    r_sorted = open('R_sorted.tsv')
    s_sorted = open('S_sorted.tsv')
    result = open('RjoinS.tsv', 'w')
    return r_sorted, s_sorted, result


def close_files():
    """Closes all opened file streams"""
    R.close()
    S.close()
    output_file.close()


def merge_join():
    """Implementation of the merge join algorithm"""
    pointer_r = move_pointer(R)
    pointer_s = move_pointer(S)

    while pointer_r:
        current_r = pointer_r
        if pointer_s and pointer_r[0] == pointer_s[0]:
            write_file(pointer_r[0], pointer_r[1], pointer_s[1])
            buffer.append(pointer_s)
            pointer_s = move_pointer(S)

        elif pointer_s and pointer_r[0] > pointer_s[0]:
            pointer_s = move_pointer(S)
            if not pointer_s:
                break
        else:
            pointer_r = move_pointer(R)
            if pointer_r and pointer_r[0] == current_r[0]:
                check_previous(buffer, pointer_r)
            elif pointer_r and pointer_r[0] != current_r[0]:
                clear_buffer()


if __name__ == '__main__':
    buffer = []
    max_buffer_size = 0
    R, S, output_file = open_files()
    merge_join()
    close_files()
    print(f'Maximum buffer size: {max_buffer_size}')

