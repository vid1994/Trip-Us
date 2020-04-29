# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 23:08:40 2020

@author: vidis
"""

import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
import random
import operator


"""
==============================
Genetic Algorithm Construction
==============================

Initialisation of the confounding search space

Chromosome: List of routes in chronological order of travel
            for example, if the location preference is A, B, C, D, E
            then [C,D,B,A,E] is one chromosome

Specified parameters
====================

1) Population --> sequence of the chromosomes or routes. Initial population is
                    random. Future population is based on selection, crossover and 
                    mutation
                    
2) popSize --> total size of the population is directly proportional to permutation rates.
                so, for example, if you have 5 locations, pop size must always be less than
                or equal to 5! = 120
                
                
3) Elite Size --> default 20


4) Mutation Rate --> default 0.01. Chromosomes with fitness value below 0.01 will be selected
                        for random mutation. 


5) Generations --> default 500. GA's usually have 50 to 500 generartions. More the generations, more
                    crossover, mutation and therefore better optimised results.
                    

"""



class LocationPreference:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def Distance(self, lon2, lat2):
        """    
        Distance is calculated between two points using radians traversed along the 
        radius of the earth. 
        
        Radius of Earth in km is 6371 km
        """
        self.y, self.x, lon2, lat2 = map(radians, [self.y, self.x, lon2, lat2])
        
        dlon = lon2 - self.y 
        dlat = lat2 - self.x 
        
        a = sin(dlat/2)**2 + cos(self.x) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        
        distance = 6371* c
        return distance
    
    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"
    
    
    
    
class FitnessFunction:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0
        
    def routeDistance(self):
        
        """
        Calculates the route distance for each route
        """
        i = 0
        
        if self.distance == 0:
            while i < len(self.route):
                fromPlace = LocationPreference(self.route[i][0], self.route[i][1])
                if i + 1 < len(self.route):
                    toPlace = self.route[i+1]
                    self.distance = self.distance + fromPlace.Distance(toPlace[1], toPlace[0])
                else:
                    toPlace = self.route[0]
                    self.distance = self.distance + fromPlace.Distance(toPlace[1], toPlace[0])
                i = i + 1
        
        return self.distance
                
    
    def routeFitness(self):
        if self.fitness == 0.0:
            self.fitness = 1/float(self.routeDistance())
        return self.fitness
    


class CreateRoute():
    
    def __init__(self, cityList, popSize):
        self.cityList = cityList
        self.popSize = popSize
    
    def createRoute(self):
        route = random.sample(self.cityList, len(self.cityList))
        return route
    
    def initialPopulation(self):
        population = []
    
        for i in range(0, self.popSize):
            population.append(self.createRoute())
        return population
    


def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = FitnessFunction(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)


class Selection():
    
    def __init__(self, popRanked, eliteSize):
        self.popRanked = popRanked
        self.eliteSize = eliteSize
        
    def selectionPop(self):
        selectionResults = []
        df = pd.DataFrame(np.array(self.popRanked), columns=["Index","Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
        
        for i in range(0, self.eliteSize):
            selectionResults.append(self.popRanked[i][0])
        for i in range(0, len(self.popRanked) - self.eliteSize):
            pick = 100*random.random()
            for i in range(0, len(self.popRanked)):
                if pick <= df.iat[i,3]:
                    selectionResults.append(self.popRanked[i][0])
                    break
        return selectionResults


class MatingPool:
    
    def __init__(self, population, selectionResults):
        self.population = population
        self.selectionResults = selectionResults
    
    def matingPool(self):
        matingpool = []
        for i in range(0, len(self.selectionResults)):
            index = self.selectionResults[i]
            matingpool.append(self.population[index])
        return matingpool



def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child
    
    
class Crossover:
    
    def __init__(self, matingpool, eliteSize):
        self.matingpool = matingpool
        self.eliteSize = eliteSize
    

    def breedPopulation(self):
        children = []
        length = len(self.matingpool) - self.eliteSize
        pool = random.sample(self.matingpool, len(self.matingpool))
    
        for i in range(0,self.eliteSize):
            children.append(self.matingpool[i])
        
        for i in range(0, length):
            child = breed(pool[i], pool[len(self.matingpool)-i-1])
            children.append(child)
        return children
    
    
    
def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual
        
def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

    
    
class NextGeneration:
    
    def __init__(self, currentGen, eliteSize, mutationRate):
        self.currentGen = currentGen
        self.eliteSize = eliteSize
        self.mutationRate = mutationRate
    
    def nextGeneration(currentGen, eliteSize, mutationRate):
        popRanked = rankRoutes(currentGen)
        selectionResults = Selection(popRanked, eliteSize).selectionPop()
        matingpool = MatingPool(currentGen, selectionResults).matingPool()
        children = Crossover(matingpool, eliteSize).breedPopulation()
        nextGeneration = mutatePopulation(children, mutationRate)
        return nextGeneration
            
progress = []
cityList = [(1.3521, 103.211), (1.3821, 104.512), (1.3421, 103.455)]
popSize=20
eliteSize=10
mutationRate=0.01
generations=500

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = CreateRoute(cityList, popSize)
    pop = pop.initialPopulation()
    progress.append(1 / rankRoutes(pop)[0][1])
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = NextGeneration.nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute


bestRoute = geneticAlgorithm(cityList, popSize, eliteSize, mutationRate, generations)

"""
Location1
Location2
Location3

Location4
Location5
Location6

Location7
Location8
Location9

"""
