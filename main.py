""" Author: https://github.com/Ekan5h
"""

from random import choice
from PyBPD.utils import evaluate, generate_agent, offspring, printBP, strBP
from PyBPD.TraceReader import TraceReader
from PyBPD.agents.optimal_tage import tage

# Initial setup for the genetic algorithm
population  = [tage]
for _ in range(9):
    population.append(generate_agent())

# Read traces from two files and evaluate on the first 100000 instructions 
tr9 = TraceReader('SHORT_SERVER-9.bt9.trace')
tr12 = TraceReader('SHORT_SERVER-12.bt9.trace')
tr9.inscount = 100000
tr12.inscount = 100000

# Run for a 1000 generations
for _ in range(1000):
    acc1 = evaluate(tr9, population)
    acc2 = evaluate(tr12, population)
    print(acc1, acc2, sep='\n')

    # Accuracy of the predictor is the lesser of the two values
    acc = [min(x, y) for x, y in zip(acc1, acc2)]

    # Only the top 4 predictors remain in the population
    top = sorted(range(len(population)), key=lambda x: acc[x], reverse=True)
    population = [population[x] for x in top[:4]]
    
    # Print the top performing predictor in each generation
    print()
    printBP(population[0])
    print(acc[top[0]], '\n')
    
    # Generate the remaining 6 predictors from any two predictors already in the population
    for _ in range(6):
        temp = offspring(choice(population), choice(population))
        while strBP(temp) in [strBP(x) for x in population]:
            temp = offspring(choice(population), choice(population))
        population.append(temp)