import matplotlib.pyplot as plt
import numpy as np
import math
from random import random

def readBerlin52File():
        try:
                f = open('berlin52.tsp')
        except:
                return []

        data = []
        for i in range(6):
                f.readline()
        
        arr = ['0']
        while arr[0] != '52':
                x = f.readline()
                x  = x.rstrip()
                arr = x.split(' ')
                data.append([float(arr[1]),float(arr[2])])

        f.close()
        return data

def printConectedGraph(data):
        #!!!Pode ser otimizado!!!
        points = data.shape[0]
        x = []
        y = []
        for i in range(points):
                for j in range(points - 1, i, -1):
                        x.append(data[i][0])
                        y.append(data[i][1])
                        x.append(data[j][0])
                        y.append(data[j][1])
        plt.plot(x,y, 'r-')
        plt.plot(x,y, 'bo')
        plt.show()

def printPath(path, data):
        points = len(path)
        x = []
        y = []
        for i in range(points):
                x.append(data[path[i]][0])
                y.append(data[path[i]][1])
        x.append(data[path[0]][0])
        y.append(data[path[0]][1])
        plt.plot(x,y,'b-')
        plt.plot(x,y,'k.')
        plt.show()

def printPheromoneTrails(pheromoneMatrix, data):
        points = len(data)
        lineGreaterValue = []
        for i in range(points):
                lineGreaterValue.append(max(pheromoneMatrix[i]))
        greaterValue = max(lineGreaterValue)
        normalizedPheromoneMatrix = pheromoneMatrix/greaterValue
        a = []
        b = []
        for i in range(points):
                a.append(data[i][0])
                b.append(data[i][1])
                for j in range(points):
                        if(normalizedPheromoneMatrix[i][j] >= 0.01):
                                x=[]
                                y=[]
                                x.append(data[i][0])
                                y.append(data[i][1])
                                x.append(data[j][0])
                                y.append(data[j][1])
                                plt.plot(x,y, 'r-', linewidth=4*normalizedPheromoneMatrix[i][j], alpha = 0.5 + 0.5*normalizedPheromoneMatrix[i][j])
        plt.plot(a,b,'k.')
        plt.show()

def getPathLength(path, weightMatrix):
        points = len(path)
        length = 0
        for i in range(points - 1):
                length = length + weightMatrix[int(path[i])][int(path[i+1])]
        length = length + weightMatrix[int(path[points-1])][int(path[0])]
        return length

def getWeightMatrixForConectedGraph(data):
        points = data.shape[0]
        weightMatrix = np.zeros((points, points))
        visibilityMatrix = np.zeros((points,points))
        for i in range(points):
                for j in range(points - 1, i, -1):
                        weightMatrix[i][j] = math.sqrt(((data[i][0] - data[j][0])**2) + ((data[i][1] - data[j][1])**2))
                        weightMatrix[j][i] = weightMatrix[i][j]
                        visibilityMatrix[i][j] = 1.0/weightMatrix[i][j]
                        visibilityMatrix[j][i] = visibilityMatrix[i][j]
        return [weightMatrix, visibilityMatrix]                       

def getProbability(path, pheromone, visibility, alpha, beta):
        n = len(visibility)
        moves = getAvailableMoves(path, n)
        probability = np.zeros(n)
        denominator = 0
        for i in moves:
                denominator = denominator + ((pheromone[i]**alpha) * visibility[i])

        for i in moves:
                if(denominator == 0):
                        probability[i] = 0
                else:
                        probability[i] = ((pheromone[i]**alpha) * visibility[i]) / denominator
        return probability

def selectMove(path, probability):
        n = len(probability)
        moves = getAvailableMoves(path, n)
        sections = np.zeros(n)
        aux = 0
        selected = random()
        for i in moves:
                aux = aux + probability[i]
                sections[i] = aux
                if selected <= sections[i]:
                        return i
        return moves[0]

def getAvailableMoves(path, points):
        return list(set(range(points)) - set(path))
