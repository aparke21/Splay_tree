# This is provided to you so that you can test your bst.py file with a particular tracefile.

import argparse
import csv
import splay

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-tf', '--tracefile')
    args = parser.parse_args()
    tracefile = args.tracefile

    forest = splay.SplayForest({})
    #t = splay.SplayTree(None)
    with open(tracefile, "r") as f:
        reader = csv.reader(f)
        lines = [l for l in reader]
        for l in lines:
            if l[0] == 'newtree':
                forest.newtree(l[1])
            if l[0] == 'insert':
                forest.insert(l[1],int(l[2]))
            if l[0] == 'delete':
                forest.delete(l[1],int(l[2]))
            if l[0] == 'search':
                forest.search(l[1],int(l[2]))
            if l[0] == 'dump':
                forest.dump()