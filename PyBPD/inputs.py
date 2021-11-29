##############################################################################
#                       Possible Inputs                                      #
##############################################################################
""" Author: https://github.com/Ekan5h
"""

from .modules import Module

history = [0]
pc = 0
ip = 0

def setPC(val):
    global pc
    pc = val

def setIP(val):
    global ip
    ip = val

def setHistory(val):
    global history
    history = val

def addHistory(val):
    global history
    history.append(val)

class PC(Module):
    def operation(self):
        return pc
    
class IP(Module):
    def operation(self):
        return ip

class HISTORY5(Module):
    def operation(self):
        x = ''.join([str(x) for x in history[-5:]])
        return int(x, 2)

class HISTORY15(Module):
    def operation(self):
        x = ''.join([str(x) for x in history[-15:]])
        return int(x, 2)

class HISTORY44(Module):
    def operation(self):
        x = ''.join([str(x) for x in history[-44:]])
        return int(x, 2)

class HISTORY130(Module):
    def operation(self):
        x = ''.join([str(x) for x in history[-130:]])
        return int(x, 2)