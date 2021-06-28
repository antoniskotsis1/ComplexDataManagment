# Kotsis Antonios AM: 3018
import argparse
import ast
import heapq
import time
from collections import Counter


def skip_duplicates(pointer, reader):
    """Returns pointer's correct position by skipping duplicate tuples"""
    next_pointer = move_pointer(reader)
    while pointer == next_pointer:
        next_pointer = move_pointer(reader)
    return next_pointer


def move_pointer(reader):
    """Moves every pointer to the next line.
      Returns either a tuple of the next line
      or None if there are no other values"""
    if reader:
        return reader.pop(0)
    else:
        return None


def empty_pointer(pointer, file_reader, result):

    result.append(pointer)
    next_ptr = skip_duplicates(pointer, file_reader)
    while next_ptr:

        result.append(next_ptr)
        next_ptr = skip_duplicates(next_ptr, file_reader)


def check_pointers(ptr, pts, reader_r, reader_s, result):
    if ptr:
        empty_pointer(ptr, reader_r, result)
    elif pts:
        empty_pointer(pts, reader_s, result)
    else:
        return


def altered_merge_join(R, S):
    """Implementation of the merge join algorithm"""
    result = []
    pointer_r = move_pointer(R)
    pointer_s = move_pointer(S)
    while pointer_r and pointer_s:

        if pointer_r == pointer_s:
            result.append(pointer_r)

            pointer_r = skip_duplicates(pointer_r, R)
            pointer_s = skip_duplicates(pointer_s, S)

        elif pointer_r > pointer_s:


            result.append(pointer_s)
            pointer_s = skip_duplicates(pointer_s, S)

        else:

            result.append(pointer_r)
            pointer_r = skip_duplicates(pointer_r, R)
    check_pointers(pointer_r, pointer_s, R, S, result)
    return result


def create_queries_list():
    query = queries.readline()
    count = 0
    while query:
        count += 1
        queries_list.append(set(ast.literal_eval(query)))
        query = queries.readline().strip()


def create_transactions_list():
    transaction = transactions_file.readline().strip()
    while transaction:
        transactions_list.append((ast.literal_eval(transaction)))
        transaction = transactions_file.readline()


def get_trf_(transaction):
    for item in set(transaction):
        if trf.get(item):
            trf[item] += 1
        else:
            trf[item] = 1


def get_occ(item, transaction):
    if occ.get((item, str(transaction))):
        occ[(item, str(transaction))] += 1
    else:
        occ[(item, str(transaction))] = 1


def create_inverted_file():
    inv_file = open("invfileocc.txt", "w")
    temp_inv_file = dict()
    for transaction_id, transaction in enumerate(transactions_list):
        get_trf_(transaction)

        for item in transaction:
            get_occ(item, transaction)
            if temp_inv_file.get(item):
                temp_inv_file[item].append(transaction_id)
            else:
                temp_inv_file[item] = [transaction_id]

    for key in sorted(temp_inv_file):
        inverted_file[key] = Counter(temp_inv_file[key])

    inv = {key: [] for key in sorted(temp_inv_file)}

    for key, value in sorted(inverted_file.items()):

        inv_file.write(f"{key}: {len(transactions_list) / trf.get(key)}, [")
        count = 0
        for items, occurrence in sorted(value.items()):
            if count != len(value) - 1:
                inv[key].append(items)
                inv_file.write(f"[{items}, {occurrence}], ")
            else:
                inv[key].append(items)
                inv_file.write(f"[{items}, {occurrence}]")
            count += 1
        inv_file.write(f"]\n")
    return inv


def get_relevance(results, k, query):
    _results = []
    heapq.heapify(_results)
    rels = {i: 0 for i in results}
    for item in query:
        for transaction_id in results:
            if rels.get(transaction_id):
                rels[transaction_id] += (
                        (transactions_list[transaction_id].count(item) * len(transactions_list)) / trf.get(item))
            else:
                rels[transaction_id] = (
                        (transactions_list[transaction_id].count(item) * len(transactions_list)) / trf.get(item))
    for key, item in rels.items():
        heapq.heappush(_results, (item, key))

    return heapq.nlargest(k, _results)


def inverted_file_relevance_queries(query_id, k):
    if query_id >= 0:
        start = time.perf_counter()
        query = queries_list[query_id]
        results = []
        for q in query:
            results = altered_merge_join(inverted_file.get(q), results)
        end = time.perf_counter()
        print("Inverted File result:")
        print(get_relevance(results, k, query))
    else:
        start = time.perf_counter()
        for query in queries_list:
            results = []
            for q in query:
                results = altered_merge_join(inverted_file.get(q), results)
        end = time.perf_counter()

    print(f"Inverted File computation time: {end - start}")


def naive_relevance_query(query, k):
    _res = []
    heapq.heapify(_res)
    rel = {i: 0 for i in range(len(transactions_list))}
    for item in query:
        for transaction_id, transaction in enumerate(transactions_list):
            if item in transaction:
                occ = transaction.count(item)
                if rel.get(transaction_id):
                    rel[transaction_id] += occ * len(transactions_list) / trf[item]
                else:
                    rel[transaction_id] += occ * len(transactions_list) / trf[item]
    for transaction_id, relevance in rel.items():
        heapq.heappush(_res, (relevance, transaction_id))

    return heapq.nlargest(k, _res)


def naive_method(query_id, k):
    if query_id >= 0:
        start = time.perf_counter()
        query = queries_list[query_id]
        print("Naive Method Result: ")
        print(naive_relevance_query(query, k))
        end = time.perf_counter()
    else:
        start = time.perf_counter()
        for query in queries_list:
            naive_relevance_query(query, k)
        end = time.perf_counter()
    print(f"Naive Method computation time: {end - start}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Relevance Queries")
    parser.add_argument("transactions", metavar='transaction_file', help="File containing transactions")
    parser.add_argument("queries", metavar='queries_file', help="File containing all queries")
    parser.add_argument("qnum", metavar='query_number', help="Number of the query to send or -1 to run all")
    parser.add_argument("method", metavar='method',
                        help="-1: run all | "
                             "0: naive method | "
                             "1: inverted file ")
    parser.add_argument("k", metavar="k", help="Number of results to be fetched.")
    args = parser.parse_args()

    transactions_list = []
    queries_list = []
    inverted_file = dict()
    trf = {}
    occ = dict()

    transactions_file = open(args.transactions)
    queries = open(args.queries)
    qnum = int(args.qnum)
    method = int(args.method)
    k = int(args.k)

    create_transactions_list()
    create_queries_list()
    inverted_file = create_inverted_file()

    if method == -1:
        inverted_file_relevance_queries(qnum, k)
        naive_method(qnum, k)
    elif method == 0:
        naive_method(qnum, k)
    elif method == 1:
        inverted_file_relevance_queries(qnum, k)
    else:
        print("No such method.")
