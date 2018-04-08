from collections import deque, defaultdict
from time import time, clock
import operator
from itertools import chain
import heapq


def load_words(file):
    '''
    the function reads a dictionary file in file system into a python dict removing all words with less than 3 letters
    :param file: dictionary file path, ex. /usr/share/dict/words on macox
    :return: a python dictionary
    '''
    d = {}
    with open(file, "r") as f:
        for line in f:
            w = line.strip(" \n")
            if len(w) > 2:
                d[w] = w
    return d

def get_anagram(dic):
    '''
    this function reads a python dict which stores the dictionary words and reindex it in terms of anagram
    :param dic: a python dict of dictionary
    :return: an indexed anagram dict
    '''
    a = defaultdict(list)
    for word in dic:
        a["".join(sorted(list(word)))].append(word)
    return a


def get_roots(word):
    '''
    a tool function that generates all variant roots of a word.
    here a root of a word means one arbitrary character being removed from                                                                                                                                                                                                                 that word, ex. "ca" is a root of both "cat" and "can"
    a word of length n has n roots
    :param word: an english word
    :return: a generator generates all roots
    '''
    for i in range(len(word)):
        yield (word[:i]+word[i+1:], i)


def init_graph(dic):
    '''
    designed adjacent list represented by a python dict based on get_roots function
    all words in the dictionary is reindexed into a key of its roots
    time complexity: O(mn), where n is the count of words in dictionary, m is the average length of words
    :param dic: a python dict of dictionary
    :return:
    '''
    d = defaultdict(list)
    for word in dic:
        for root in get_roots(word):
            d[root].append(word)
    return d





def get_path(graph, analist, dic, src, des, operations):
    '''
    the main funtion implemented with dijkstra algorithm that finds the path from src to des with minimum cost

    :param graph:  a designed adjacent list storing edge information
    :param dic:  the original dictionary
    :param src:  the source word
    :param des:  the destination word
    :param operations: an operation list of（opr_name, cost）, sorted by cost
    :return:
    '''

    # priority queue for unvisited words, element type: [cost_from_src, previous_word, current_word]
    # elements are priorized by cost_from_src
    pq = []

    # a set of marked words whose cost from src are confirmed and will not change
    marked = set()

    # a dynamically changing dictionary of words visited but not marked
    visited = defaultdict(list)    #words keep-to-update

    # the initial element of src: cost of 0 to itself, no previous words
    visited[src] = [0, None, src]
    # push the reference into the priority queue
    heapq.heappush(pq, visited[src])

    while pq:
        cost, pre, word = heapq.heappop(pq) #get next node in priority queue

        #only unmarked word will go through this process
        if word not in marked:
            # by dijkstra alg
            # if a word is to pop from priority queue, we already got the minimum cost for it, so it is marked
            marked.add(word)  #marked word will never go back to priority queue

            # find the destination word
            if word == des:
                # visited contains the transformation chain
                return visited, word

            # intitialize the list of neighboring words from adjacent list
            adjwords = {}
            #four kinds of adjacent nodes
            addone = chain(*(graph[word, i] for i in range(len(word)+1)))
            changeone = chain(*(graph[root] for root in get_roots(word)))
            deleteone = (w for w,i in get_roots(word) if w in dic)
            anagram = analist["".join(sorted(list(word)))]
            adjwords["add"] = addone
            adjwords["cha"] = changeone
            adjwords["del"] = deleteone
            adjwords["ana"] = anagram

            # go through all neighboring words
            for opr, c in operations:
                for w in adjwords[opr]:
                    if w in visited:  #w has already been visited, thus having a cost from src
                        if visited[word][0] + c < visited[w][0]:
                            visited[w][0] = visited[word][0] + c
                            visited[w][1] = word
                            #update: percolate up since value is smaller
                            heapq._siftdown(pq, 0, pq.index(visited[w]))

                    else: #the word is visited for the first time
                        visited[w] = [visited[word][0] + c, word, w]
                        #add into the priority queue
                        heapq.heappush(pq, visited[w])

    #all reachable words from src are checked, and no des
    return None

def get_chain(data, src, des):
    if data == None:
        return (-1, "no solutions")
    else:
        linker, word = data[0], data[1]
        cost = linker[des][0]
        chainer = [word]
        cur = word
        pre = linker[src][1]
        while pre != src:
            pre = linker[cur][1]
            cur = linker[pre][2]
            chainer.append(pre)
        return (cost, " - ".join(chainer[::-1]))




if __name__ == "__main__":

    # cost for add, delete, change, anagram bu order
    # for example: input 1 3 1 5
    c = input().split()
    costs = {"add": int(c[0]), "del": int(c[1]), "cha": int(c[2]), "ana": int(c[3])}
    # sorted list by cost value
    operations = sorted(costs.items(), key=operator.itemgetter(1))


    dic = load_words("words")  #about 130ms
    analist = get_anagram(dic)  #about 700ms
    graph = init_graph(dic)

    src = input()
    des = input()

    data = get_path(graph,analist,dic,src,des,operations)
    res = get_chain(data, src, des)
    print(res[0])
    print(res[1])



