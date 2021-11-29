""" Author: https://github.com/Ekan5h
"""

from random import choice, random

from .module_registry import modules
from .inputs import addHistory, setHistory, setPC

def generate_agent(max_depth=6):
    mod = choice(list(modules.keys()))
    if max_depth == 1:
        while modules[mod][1]!=0: mod = choice(list(modules.keys()))
    obj = modules[mod][0].new()
    for _ in range(modules[mod][1]):
        obj.children.append(generate_agent(max_depth-1))
    return obj

def printBP(root):
    print(type(root).__name__, len(root.children), end=' ')
    for x in root.children:
        printBP(x)

def strBP(root):
    s = type(root).__name__ + str(len(root.children)) + ' '
    for x in root.children:
        s += strBP(x)
    return s

def resetBP(root):
    y = root.children
    for x in y:
        resetBP(x)
    root.__init__()
    root.children = y

def offspring(tree1, tree2):
    nodes = [[],[]]
    def fill(root, i):
        d = 1
        for x in root.children:
            d = max(fill(x, i)+1, d)
        nodes[i].append([root, d])
        return d
    fill(tree1, 0)
    fill(tree2, 1)
    
    def copy_tree(root, depth, i):
        head = root.new()
        for x in root.children:
            if random()<0.1:
                head.children.append(generate_agent(depth-1))
            elif random()<0.5:
                # Shift to tree2
                node = choice(nodes[i])
                while node[1]>=depth: node = choice(nodes[i])
                head.children.append(copy_tree(node[0], depth-1, 1-i))
            else:
                head.children.append(copy_tree(x, depth-1, i))
        return head
    return copy_tree(tree1, 6, 1)

def evaluate(tr, population):
    tr.reset_reader()
    
    # not_correct = {}

    setHistory([0])

    acc = [0 for _ in range(len(population))]
    tot = [0 for _ in range(len(population))]

    for x in population:
        resetBP(x)

    while True:
        pc, real, ip = tr.update()
        if pc == -1:
            break
        setPC(pc)
        for i, bpred in enumerate(population):
            predicted = bpred.evaluate()
            tot[i] += 1
            if real == predicted&1:
                acc[i] += 1
            # else:
            #     if hex(ip) in not_correct:
                    # not_correct[hex(ip)] += 1
                # else:
                #     not_correct[hex(ip)] = 1
            bpred.update(real)
        addHistory(real)
    # print(not_correct)
    # m = sorted(not_correct, key=lambda x: not_correct[x])
    # print([(x, not_correct[x]) for x in m])
    return [x/y for x, y in zip(acc, tot)]

