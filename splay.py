from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

class SplayForest():
    def  __init__(self,
                  roots : None):
        self.roots = roots

    def newtree(self,treename):
        self.roots[treename] = None

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!!!
    def dump(self):
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.roots == None:
            dict_repr = {}
        else:
            dict_repr = {}
            for t in self.roots:
                if self.roots[t] is not None:
                    dict_repr[t] = _to_dict(self.roots[t])
        print(json.dumps(dict_repr,indent = 2))

    # Search:
    # Search for the key or the last node before we fall out of the tree.
    # Splay that node.
    def search(self, treename: str, key: int):
        root = self.roots[treename]
        if root is None:
            return

        root = self.splay(root, key, treename)
        self.roots[treename] = root

    # Insert Type 1:
    # The key is guaranteed to not be in the tree.
    # Call splay(x) and respond according to whether we get the IOP or IOS.
    def insert(self, treename: str, key: int):
        root = self.roots[treename]
        if root is None:
            self.roots[treename] = Node(key)
            return

        root = self.splay(root, key, treename)

        new_node = Node(key)

        if key < root.key:
            new_node.leftchild = root.leftchild

            if new_node.leftchild is not None:
                new_node.leftchild.parent = new_node

            new_node.rightchild = root
            root.leftchild = None
        else:
            new_node.rightchild = root.rightchild

            if new_node.rightchild is not None:
                new_node.rightchild.parent = new_node

            new_node.leftchild = root
            root.rightchild = None

        root.parent = new_node
        self.roots[treename] = new_node

    # Delete Type 1:
    # The key is guarenteed to be in the tree.
    # Call splay(key) and then respond accordingly.
    # If key (now at the root) has two subtrees call splay(key) on the right one.
    def delete(self,treename:str,key:int):
        root = self.roots[treename]

        root = self.splay(root, key, treename)
        
        if root.leftchild is None:
            self.roots[treename] = root.rightchild
            if root.rightchild is not None:
                root.rightchild.parent = None
        elif root.rightchild is None:
            self.roots[treename] = root.leftchild
            if root.leftchild is not None:
                root.leftchild.parent = None
        else:
            # always the right subtree
            right_subtree = root.rightchild 
            right_subtree = self.splay(right_subtree, key, treename)
            right_subtree.leftchild = root.leftchild
            
            if right_subtree.leftchild is not None:
                right_subtree.leftchild.parent = right_subtree
            
            self.roots[treename] = right_subtree
            right_subtree.parent = None


    def splay(self, root, key: int, treename: str):
        node = root

        while node is not None:
            if key == node.key:
                break
            elif key < node.key:
                if node.leftchild is None:
                    self.splay_helper(node, treename)
                    return node
                node = node.leftchild
            else:
                if node.rightchild is None:
                    self.splay_helper(node, treename)
                    return node
                node = node.rightchild

        self.splay_helper(node, treename)
        return node

    def splay_helper(self, node, treename):
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                if node == parent.leftchild:
                    self.right_rot(parent, treename)
                else:
                    self.left_rot(parent, treename)
            else:
                if node == parent.rightchild and parent == grandparent.rightchild:
                    self.left_rot(grandparent, treename)
                    self.left_rot(parent, treename)
                elif node == parent.leftchild and parent == grandparent.leftchild:
                    self.right_rot(grandparent, treename)
                    self.right_rot(parent, treename)
                elif node == parent.rightchild and parent == grandparent.leftchild:
                    self.left_rot(parent, treename)
                    self.right_rot(grandparent, treename)
                else:
                    self.right_rot(parent, treename)
                    self.left_rot(grandparent, treename)

    def left_rot(self, node, treename):
        right_child = node.rightchild
        node.rightchild = right_child.leftchild

        if right_child.leftchild is not None:
            right_child.leftchild.parent = node

        right_child.parent = node.parent

        if node.parent is None:
            self.roots[treename] = right_child
        elif node == node.parent.leftchild:
            node.parent.leftchild = right_child
        else:
            node.parent.rightchild = right_child

        right_child.leftchild = node
        node.parent = right_child

    def right_rot(self, node, treename):
        left_child = node.leftchild
        node.leftchild = left_child.rightchild

        if left_child.rightchild is not None:
            left_child.rightchild.parent = node

        left_child.parent = node.parent

        if node.parent is None:
            self.roots[treename] = left_child
        elif node == node.parent.rightchild:
            node.parent.rightchild = left_child
        else:
            node.parent.leftchild = left_child

        left_child.rightchild = node
        node.parent = left_child