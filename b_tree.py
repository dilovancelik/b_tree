from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import copy 

@dataclass
class BTreeNode:
    keys: List[int]
    children: List[BTreeNode]
    min_degree: int

    def __init__(self, keys: List[int], children: List[BTreeNode], min_degree: int) -> BTreeNode:
        self.keys = keys
        self.children = children 
        self.min_degree = min_degree
    
    def is_leaf(self) -> bool:
        return len(self.children) == 0
    
    def search_node(self, key: int) -> int:
        if key in self.keys:
            return key
        elif self.is_leaf():
            raise LookupError("Key not available in tree")
        else:
            i = sum(1 for x in self.keys if x < key)
            self.search_node(self.children[i])
    
    def split_child(self, child_index: int):
        child = self.children[child_index]
        med_key = len(child.keys) // 2

        x = BTreeNode(
            keys = child.keys[0:med_key],
            children = child.children[:med_key],
            min_degree = self.min_degree
        )
        y = BTreeNode(
            keys = child.keys[med_key-1:],
            children = child.children[med_key:],
            min_degree = self.min_degree
        )
        self.children.insert(child_index, y)
        self.children.insert(child_index, x)

        self.keys.append(med_key)
        self.keys.sort()
    
    def insert_non_full(self, key: int):        
        if self.is_leaf():
            self.keys.append(key)
            self.keys.sort()
        else:
            i = sum(1 for x in self.keys if x > key)
            if len(self.children[i].keys) == (2 * self.min_degree) - 1:
                self.split_child(child_index = i)
                self.children[i + 1].insert_non_full(key = key)
            else:
                self.children[i].insert_non_full(key = key)

    def traverse(self):
        for i in range(len(self.keys)):
            if not self.is_leaf():
                self.children[i].traverse()
            print(self.keys[i], end=' ')
            
        if not self.is_leaf():
            self.children[i + 1].traverse()
        print("\n")

@dataclass
class BTree:
    root: BTreeNode
    min_degree: int

    def __init__(self, min_degree: int) -> BTree:
        self.root = BTreeNode(keys = [], children = [], min_degree = min_degree)
        self.min_degree = min_degree

    def seach(self, key) -> int:
        self.root.search_node(key)

    def insert(self, key: int):
        if self.root.keys == []:
            self.root.keys.append(key)
        elif len(self.root.keys) >= (2 * self.min_degree) - 1:
            old_root = copy.copy(self.root)
            self.root = BTreeNode(keys = [], children = [], min_degree = self.min_degree)
            self.root.children.append(old_root)

            self.root.split_child(child_index = 0)
            self.root.insert_non_full(key)
        else:
            
            self.root.insert_non_full(key)

    def traverse(self):
        self.root.traverse()