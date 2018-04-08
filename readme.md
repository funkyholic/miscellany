## challenge   
input: two words A and B and the cost of each modification ways
output: a chain of words starting from A, ending with B. 
Each step of the change must follow the following four ways:
1.replace one character
2.add one character
3.delete one character
4.make anagram

also each words in the middle must also be in the dictionary.

for example:
input: 
1 3 1 5
HEALTH
HANDS

should output:
HEALTH - HEATH - HEATS - HENTS - HENDS - HANDS



## to run
using python3

to run the test by manual input, run in the terminal:

`python3 app.py`

you will need to input 3 lines of inputs:
c1 c2 c3 c4
src
des



to run the unittest:

`python3 tests.py -v`



## algorithm & method


It turned out to be a quite direct problem with mere dijkstra algorithm.
It is not dynamic programming, because the words in dictionary are discrete. 
Unlike the arbitrary modification of single letters in levenshtein distance, even if you find an optimal subproblem definition, it is still conditionalized by the dictionary.
So best way to solve a conditionally discrete optimization problem could be using a graph.

The main idea of this problem is that we start from a word A and end at a word B by taking one step each time.
Dijkstra algorithm fits well in finding the path of minimum cost.

The only problem left is how to define the structure of graph. Adjacent matrix is easy to go but the number of words is upto 230000, so no way.
A refined adjacent list should be consided.

At the visit of each node in graph, we should have a easy of figuring out the neighbouring nodes of the current node(each node represents a word).
Note there are four kinds of relationship between nodes: 1.add one char, 2.delete one char, 3.change one char, 4.take anagram


All addition, deletion, modification of adjacent words are dealt with only on character. (literally there won't be too much choice as words are limited)
So there are n kinds of variations for a word of length n. We put (root, index) into the hashtable as key, and a list of words as value sharing the same root.
For example, "cat" and "can" share the same root of "ca" by removing the character at index 2, so we put an entry ("ca",2):["cat", "can"] into the hashtable.
Making anagram is easy, we just built an anagram dictionary ahead of time. Each time when needing to check if a word is anagram to the other, just search in hashtable. It is fast.
By doing such preprocessing, we can easily find adjacent words during the search.

And all needed is to combine this with dijkstra algorithm.
