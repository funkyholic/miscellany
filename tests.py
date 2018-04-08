import unittest
from app import get_path, get_anagram, get_roots, init_graph, load_words, get_chain
import operator




class SolutionTests(unittest.TestCase):
    dic = load_words("words")  # about 130ms
    analist = get_anagram(dic)  # about 700ms
    graph = init_graph(dic)


    def test_general(self):
        costs = {"add": 100, "del": 3, "cha": 5, "ana": 5}
        operations = sorted(costs.items(), key=operator.itemgetter(1))
        src = "team"
        des = "mate"

        data = get_path(SolutionTests.graph, SolutionTests.analist, SolutionTests.dic, src, des, operations)
        self.assertEqual((5,"team - mate"), get_chain(data, src, des))


if __name__ == '__main__':
    unittest.main()