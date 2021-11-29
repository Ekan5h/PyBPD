######################################################################################
# Available nodes
######################################################################################
""" Author: https://github.com/Ekan5h
"""

from .modules import *
from .inputs import *

modules = {
    'XOR': [XOR(), 2],
    'AND': [AND(), 2],
    'OR': [OR(), 2],
    'ADD': [ADD(), 2],
    'NOT': [NOT(), 1],
    'MSB': [MSB(), 1],
    'LSB': [LSB(), 1],
    'HASH1': [HASH1(), 1],
    'HASH2': [HASH2(), 1],
    'HASH3': [HASH3(), 1],
    'CONSTANT_0': [CONSTANT_VALUE_0(), 0],
    'CONSTANT_1': [CONSTANT_VALUE_1(), 0],
    'PREDICTOR_2BIT_LOCAL': [PREDICTOR_2BIT(), 1],
    'PREDICTOR_2BIT_GLOBAL': [PREDICTOR_2BIT_GLOBAL(), 0],
    'PREDICTOR_1BIT_LOCAL': [PREDICTOR_1BIT(), 1],
    'PREDICTOR_1BIT_GLOBAL': [PREDICTOR_1BIT_GLOBAL(), 0],
    'TAGE_TABLE': [TAGE_TABLE(), 1],
    'HIGHEST_PRIORITY_2': [HIGHEST_PRIORITY(), 2],
    'HIGHEST_PRIORITY_3': [HIGHEST_PRIORITY(), 3],
    'HIGHEST_PRIORITY_4': [HIGHEST_PRIORITY(), 4],
    'HIGHEST_PRIORITY_5': [HIGHEST_PRIORITY(), 5],
    'PC': [PC(), 0],
    'HISTORY_5': [HISTORY5(), 0],
    'HISTORY_15': [HISTORY15(), 0],
    'HISTORY_44': [HISTORY44(), 0],
    'HISTORY_130': [HISTORY130(), 0]
}