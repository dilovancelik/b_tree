import random
import b_tree

tree = b_tree.BTree(min_degree=2)
list = random.sample(range(0, 200, 10), 10)
print(list)
for i in list: #random.shuffle(list()):
    tree.insert(i)
tree.traverse()