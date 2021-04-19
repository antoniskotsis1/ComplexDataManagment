# AM: 3018 Name: Kotsis Antonios

def write_file(pointer):
    """Writes the outcome of the join operation to file RjoinS.tsv"""
    output_file.write(f'{pointer[0]}\t{pointer[1]}\n')


def skip_duplicates(current_pointer, pointer):
    """Returns pointer's correct position by skipping duplicate tuples"""
    next_pointer = move_pointer(pointer)
    while current_pointer == next_pointer:
        next_pointer = move_pointer(pointer)
    return next_pointer


def move_pointer(reader):
    """Moves every pointer to the next line.
      Returns either a tuple of the next line
      or None if there are no other values"""
    x = reader.readline().strip()
    if x:
        x = x.split('\t')
        try:
            return tuple((x[0], int(x[1])))
        except ValueError:
            return tuple((x[0], float(x[1])))
    return None


def open_files():
    return open('R_sorted.tsv'), open('S_sorted.tsv'), open('RintersectS.tsv', 'w')


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
            pointer_s = skip_duplicates(pointer_s, S)
        else:
            pointer_r = skip_duplicates(pointer_r, R)


if __name__ == '__main__':
    R, S, output_file = open_files()
    altered_merge_join()
    close_files()
