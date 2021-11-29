""" Author: https://github.com/Ekan5h
"""

import copy
from collections import deque

class Module:
    def __init__(self):
        self.children = []
    def new(self):
        x = copy.deepcopy(self)
        x.__init__()
        return x
    def operation(self, x):
        return x
    def evaluate(self):
        vals = [x.evaluate() for x in self.children]
        return self.operation(*vals)
    def update(self, real):
        for x in self.children:
            x.update(real)

class XOR(Module):
    def operation(self, a, b):
        return a^b

class AND(Module):
    def operation(self, a, b):
        return a&b

class OR(Module):
    def operation(self, a, b):
        return a|b

class ADD(Module):
    def operation(self, a, b):
        return a+b

class NOT(Module):
    def operation(self, a):
        return ~a

class MSB(Module):
    def operation(self, a):
        return int(a<0)

class LSB(Module):
    def operation(self, a):
        return a%2

class HASH1(Module):
    def operation(self, a):
        if 96396^a>=0:
            x = bin(96396^a)[2:][::-1]
        else:
            x = bin(96396^a)[3:][::-1]
        x = x[25:32] + x[:7]
        return int(x,2)

class HASH2(Module):
    def operation(self, a):
        if 2706292298^a>=0:
            x = bin(2706292298^a)[2:][::-1]
        else:
            x = bin(2706292298^a)[3:][::-1]
        x = x[55:62] + x[:7]
        return int(x,2)
    
class HASH3(Module):
    def operation(self, a):
        if 1329306534^a>=0:
            x = bin(1329306534^a)[2:][::-1]
        else:
            x = bin(1329306534^a)[3:][::-1]
        x = x[115:122] + x[:7]
        return int(x,2)

class CONSTANT_VALUE_1(Module):
    def operation(self):
        return 1

class CONSTANT_VALUE_0(Module):
    def operation(self):
        return 0

class PREDICTOR_1BIT_GLOBAL(Module):
    def  __init__(self):
        super().__init__()
        self.state = 0
    def operation(self):
        return self.state
    def update(self, real):
        self.state = real

class PREDICTOR_1BIT(Module):
    def __init__(self):
        super().__init__()
        self.last = {}
        self.pcs = deque()
        self.state = 1
        self.lastpc = 0
    def operation(self, pc):
        self.lastpc = pc
        if pc in self.last:
            return self.last[pc]
        return self.state
    def update(self, real):
        if self.lastpc in self.last:
            self.last[self.lastpc] = real
        else:
            self.state = real
            if len(self.pcs) == 16384:
                x = self.pcs.popleft()
                del self.last[x]
            self.last[self.lastpc] = real
            self.pcs.append(self.lastpc)

class PREDICTOR_2BIT_GLOBAL(Module):
    def  __init__(self):
        super().__init__()
        self.state = 1
    def operation(self):
        return self.state//2
    def update(self, real):
        self.state = max(min(self.state + 2*real-1, 3), 0)
        

class PREDICTOR_2BIT(Module):
    def __init__(self):
        self.children = []
        self.states = {}
        self.outs = {}
        self.state = 0
        self.out = 0
        self.last_pc = 0
        self.pcs = deque()
    def operation(self, pc):
        self.last_pc = pc
        if pc in self.outs:
            return self.outs[pc]
        return self.out
    def update(self, real):
        if self.last_pc in self.states:
            if self.outs[self.last_pc]!=real:
                if self.states[self.last_pc] == 0:
                    self.outs[self.last_pc] = real
                    self.states[self.last_pc] = 1
                else:
                    self.states[self.last_pc] -= 1
            else:
                self.states[self.last_pc] = min(self.states[self.last_pc]+1, 3)
            return
        if real!=self.out:
            if self.state == 0:
                self.out = real
                self.state = 1
            else:
                self.state -= 1
        else:
            self.state = min(self.state+1, 3)
        if len(self.states) == 16384:
            x = self.pcs.popleft()
            del self.states[x]
            del self.outs[x]
        self.states[self.last_pc] = 1
        self.outs[self.last_pc] = real
        self.pcs.append(self.last_pc)

class TAGE_TABLE(Module):
    def __init__(self):
        self.children = []
        self.last_val = 0
        self.last_out = 0
        self.lookup = {}
        for i in range(16384):
            self.lookup[i] = [2, 0]

    def operation(self, val):
        self.last_val = val
        if val not in self.lookup:
            self.last_out = 1
            return 3
        else:
            self.last_out = self.lookup[val][0]//2
            return self.lookup[val][0]//2
    
    def update(self, real):
        if self.last_val in self.lookup:
            self.lookup[self.last_val][0] = min(max(self.lookup[self.last_val][0]+2*real-1, 0), 3)
            if self.last_out == real:
                self.lookup[self.last_val][1] = min(self.lookup[self.last_val][1]+1, 3)
            else:
                self.lookup[self.last_val][1] = max(self.lookup[self.last_val][1]-1, 0)
        else:
            for x in self.lookup:
                if self.lookup[x][1] == 0:
                    del self.lookup[x]
                    self.lookup[self.last_val] = [1+real, 0]
                    for x in self.children:
                        x.update(real)
                    return
            for x in self.lookup:
                self.lookup[x][1] -= 1
        for x in self.children:
            x.update(real)

class HIGHEST_PRIORITY(Module):
    def operation(self, *a):
        self.vals = a
        for x in a[::-1]:
            if x in [0, 1]:
                return x
        return 0