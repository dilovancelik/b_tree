import b_tree

tree = b_tree.BTree(min_degree=2)

for i in range(0, 200, 10):
    tree.insert(i)
tree.traverse()