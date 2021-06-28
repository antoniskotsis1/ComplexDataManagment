# Kotsis Antonios AM: 3018

import argparse
import ast
import time
import re


def move_pointer(reader):
    """Moves every pointer to the next line.
      Returns either a tuple of the next line
      or None if there are no other values"""
    if reader:
        return reader.pop(0)
    else:
        return None


def skip_duplicates(current_pointer, pointer):
    """Returns pointer's correct position by skipping duplicate tuples"""
    next_pointer = move_pointer(pointer)
    while current_pointer == next_pointer:
        next_pointer = move_pointer(pointer)
    return next_pointer


def altered_merge_join(R, S):
    """Implementation of the merge join algorithm"""
    result = []
    if len(R) == 0:
        return S
    elif len(S) == 0:
        return R

    pointer_r = move_pointer(R)
    pointer_s = move_pointer(S)
    while pointer_r and pointer_s:

        if pointer_r == pointer_s:
            result.append(pointer_s)
            pointer_r = skip_duplicates(pointer_r, R)
            pointer_s = skip_duplicates(pointer_s, S)
        elif pointer_r > pointer_s:
            pointer_s = skip_duplicates(pointer_s, S)
        else:
            pointer_r = skip_duplicates(pointer_r, R)
    return result


def create_transactions_list():
    transaction = transactions_file.readline().strip()
    while transaction:
        transactions_list.append(set(ast.literal_eval(transaction)))
        transaction = transactions_file.readline()


def naive_method(query, result):
    for transaction_id, transaction in enumerate(transactions_list):
        if query.issubset(transaction):
            result.append(transaction_id)


def naive_containment_queries(query_id):
    result = []
    if query_id >= 0:

        naive_time_start = time.perf_counter()
        query = queries_list[query_id]

        naive_method(query, result)
        naive_time_end = time.perf_counter()

        print("Naive Method Result:")
        print(result)
    else:
        naive_time_start = time.perf_counter()

        for query in queries_list:
            naive_method(query, result)

        naive_time_end = time.perf_counter()

    print(f"Naive Method Computation Time = {naive_time_end - naive_time_start} sec")


def create_queries_list():
    query = queries.readline()
    count = 0
    while query:
        count += 1
        queries_list.append(set(ast.literal_eval(query)))
        query = queries.readline().strip()


def create_sigfile():
    sig_file = open("sigfile.txt", "w")
    for transaction in transactions_list:
        n = max(transaction)
        bit_num = n * "0"
        for i in transaction:
            bit_num = bit_num[:int(i)] + "1" + bit_num[int(i + 1):]
        sig_file.write(f'{int(bit_num[::-1], 2)}\n')

        sigfile.append(int(bit_num[::-1], 2))


def exact_sig_file_method(query_signature, result):
    for transaction_id, transaction in enumerate(sigfile):
        if query_signature & ~transaction == 0:
            result.append(transaction_id)


def exact_signature_containment_queries(query_id):
    result = []

    if query_id >= 0:
        start_time = time.perf_counter()

        query_signature = sum((pow(2, i) for i in queries_list[query_id]))
        exact_sig_file_method(query_signature, result)

        end_time = time.perf_counter()

        print("Signature File result :")
        print(result)
    else:
        start_time = time.perf_counter()

        for query in queries_list:
            query_signature = sum((pow(2, i) for i in query))
            exact_sig_file_method(query_signature, result)

        end_time = time.perf_counter()

    print(f"Signature File Computation Time: {end_time - start_time} sec")


def create_bitslice_signature_file():
    bitslice_file = open("bitslice.txt", "w")
    for transaction_id, transaction in enumerate(transactions_list):
        for item in transaction:
            if bitslice.get(item):
                bitslice[item] += pow(2, transaction_id)
            else:
                bitslice[item] = pow(2, transaction_id)
    for key, value in sorted(bitslice.items()):
        bitslice_file.write(f"{key}: {value}\n")


def exact_bitslice_method(query):
    and_result = bitslice.get(list(query)[0])
    for i in query:
        and_result &= bitslice.get(i)

    m = str(bin(and_result))[::-1]
    return [n.start() for n in re.finditer('1', m)]


def exact_bitslice_signature_containment_queries(query_id):
    if query_id >= 0:
        start = time.perf_counter()

        query = queries_list[query_id]

        result = exact_bitslice_method(query)

        end = time.perf_counter()

        print(f"Bitsliced Signature File result: \n {result}")

    else:
        start = time.perf_counter()
        for query in queries_list:
            exact_bitslice_method(query)
        end = time.perf_counter()

    print(f"Bitsliced Computation Time: {end - start} sec")


def create_inverted_list():
    inv_file = open("invfile.txt", "w")
    for transaction_id, transaction in enumerate(transactions_list):
        for item in transaction:
            if inverted_list.get(item):
                inverted_list[item].append(transaction_id)
            else:
                inverted_list[item] = [transaction_id]
    for key, value in sorted(inverted_list.items()):
        inverted_list[key] = sorted(value)
        inv_file.write(f"{key}: {sorted(value)}\n")


def inverted_list_containment_queries(query_id):
    if query_id >= 0:
        start = time.perf_counter()
        query = queries_list[query_id]
        result = []
        for item in query:
            result = altered_merge_join(inverted_list[item], result)

        end = time.perf_counter()
        print("Inverted File Result: ")
        print(result)

    else:
        start = time.perf_counter()
        for query in queries_list:
            result = []
            for item in query:
                result = altered_merge_join(inverted_list[item], result)
        end = time.perf_counter()

    print(f"Inverted File Computational Time: {(end - start)} sec")


if __name__ == '__main__':
    transactions_list = []
    queries_list = []
    sigfile = []
    bitslice = dict()
    inverted_list = dict()

    parser = argparse.ArgumentParser(description="Containment Queries")
    parser.add_argument("transactions", metavar='transaction_file', help="File containing transactions")
    parser.add_argument("queries", metavar='queries_file', help="File containing all queries")
    parser.add_argument("qnum", metavar='query_number', help="Number of the query to send or -1 to run all")
    parser.add_argument("method", metavar='method',
                        help="-1: run all | "
                             "0: naive method | "
                             "1: exact signature | "
                             "2: exact bitslice | "
                             "3: inverted file ")
    args = parser.parse_args()

    transactions_file = open(args.transactions)
    queries = open(args.queries)

    create_queries_list()
    create_transactions_list()
    create_sigfile()
    create_bitslice_signature_file()
    create_inverted_list()

    # queries = open("queries.txt")
    # transactions_file = open("transactions.txt")
    qnum = int(args.qnum)
    if qnum > len(queries_list) - 1:
        exit("No such query..Exiting")
    method = int(args.method)

    if method == -1:
        naive_containment_queries(qnum)
        exact_signature_containment_queries(qnum)
        exact_bitslice_signature_containment_queries(qnum)
        inverted_list_containment_queries(qnum)
    elif method == 0:
        naive_containment_queries(qnum)
    elif method == 1:

        exact_signature_containment_queries(qnum)
    elif method == 2:

        exact_bitslice_signature_containment_queries(qnum)
    elif method == 3:

        inverted_list_containment_queries(qnum)
    else:
        print("No such method.")
