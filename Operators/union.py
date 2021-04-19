# AM: 3018 Name: Kotsis Antonios

def write_file(pointer):
    """Writes the outcome of the join operation to file RjoinS.tsv"""
    output_file.write(f'{pointer[0]}\t{pointer[1]}\n')


def skip_duplicates(pointer, reader):
    """Returns pointer's correct position by skipping duplicate tuples"""
    next_pointer = move_pointer(reader)
    while pointer == next_pointer:
        next_pointer = move_pointer(reader)
    return next_pointer


def move_pointer(reader):
    """Moves every pointer to the next line.
      Returns either a tuple of the next line or
       None if there are no other values"""
    x = reader.readline().strip()
    if x:
        x = x.split('\t')
        try:
            result = x[0], int(x[1])
        except ValueError:
            result = x[0], float(x[1])
        return result
    return None


def empty_pointer(pointer, file_reader):
    write_file(pointer)
    next_ptr = skip_duplicates(pointer, file_reader)
    while next_ptr:
        write_file(next_ptr)
        next_ptr = skip_duplicates(next_ptr, file_reader)


def check_pointers(ptr, pts, reader_r, reader_s):
    if ptr:
        empty_pointer(ptr, reader_r)
    elif pts:
        empty_pointer(pts, reader_s)
    else:
        return


def open_files():
    r_sorted = open('R_sorted.tsv')
    s_sorted = open('S_sorted.tsv')
    result = open('RunionS.tsv', 'w')
    return r_sorted, s_sorted, result


def close_files():
    """Closes all opened file streams"""
    R.close()
    S.close()
    output_file.close()


def altered_merge_join():
    """Implementation of the merge join algorithm"""
    pointer_r = move_pointer(R)
    pointer_s = move_pointer(S)
    while pointer_r and pointer_s:

        if pointer_r == pointer_s:

            write_file(pointer_r)
            pointer_r = skip_duplicates(pointer_r, R)
            pointer_s = skip_duplicates(pointer_s, S)

        elif pointer_r > pointer_s:

            write_file(pointer_s)
            pointer_s = skip_duplicates(pointer_s, S)

        else:
            write_file(pointer_r)
            pointer_r = skip_duplicates(pointer_r, R)
    check_pointers(pointer_r, pointer_s, R, S)


if __name__ == '__main__':
    R, S, output_file = open_files()
    altered_merge_join()
    close_files()
