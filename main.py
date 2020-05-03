import numpy as np
import matplotlib.pyplot as plt
import math
import time
from random import random, shuffle
from functions import readBerlin52File, printPath, getWeightMatrixForConectedGraph, getPathLength, getProbability, selectMove, printPheromoneTrails

#Ler Dados
data = np.array(readBerlin52File())

printProgress = True #Imprimir progresso da execução
printExecutionTime = True #Imprimir tempos de execução
showPheromoneMap = True #Mostrar mapa de feromônios final
showBestPath = True #Mostrar melhor caminho final
printPerformance = True #Mostrar gráficos de performance do algoritmo

#Variáveis
maxIt = 250 #Máximo de iterações
startingPheromone = 10 ** -6 #Feromonio inicial em todas as arestas
Q = 100.0 #Quantidade de feromônio depositado
alpha = 1 #Constante que influencia na percepção de feromônio
beta = 5 #Constante que influencia na percepção de distância
rho = 0.5 #Taxa de decaimento de feromônio

cities = len(data) #Número de cidades
[weightMatrix, visibilityMatrix] = getWeightMatrixForConectedGraph(data) #Matriz de pesos e visibilidade para as cidades
visibilityMatrix = visibilityMatrix ** beta #Cálculo para otimizar a execução e fazer a operação de potência só uma vez


ants = 52 #Número de formigas
elitistAnts = 10 #Número de formigas elitistas
elitistPheromoneDeposit = 0 #Quantidade de feromonio depositado por formigas elitistas
antPath = np.zeros((ants,cities), dtype="int") #Caminho da formiga na iteração
antPathLength = np.zeros(ants) #Tamanho do caminho de cada formiga
probabilityMatrix = np.zeros((ants,cities)) #Matriz com a probabilidade de cada formiga selecionar as cidades
pheromoneMatrix = np.ones((cities,cities)) * startingPheromone #Matriz com os feromonios
       

bestAnt = 0 #Indice da melhor formiga
bestPath = np.array(range(cities)) #Inicia melhor caminho
bestPathLength = np.Infinity #Comprimento do melhor caminho
iterationBestPathLength = [] #Lista com o comprimento do melhor caminho de cada iteração
bestPathList = [] #Lista com o melhor até a iteração
iterationAveragePathLength = [] #Lista com a média de cada iteração

step = 0

#Repita o número máximo de iterações
start = time.time()
meanItTime = 0
for it in range(maxIt):
        itStart = time.time()        
        prct = it/maxIt
        if(prct >= step and printProgress):
                end = time.time() - start
                print(str(prct*100)+"% (it="+str(it)+") - {:.3f}s".format(end))
                step += 0.1
        pheromoneVariationMatrix = pheromoneMatrix * (1 - rho) #Matriz com a variação do feromônio para a iteração
        #Construção do caminho
        avgLength = 0
        #Para cada formiga
        for i in range(ants):
                #Posiciona aleatóriamente as formigas em uma cidade
                antPath[i][0] = math.floor(random()*cities) 
                #Para o número de cidades a serem percorridas
                for j in range(cities - 1):                
                        probabilityMatrix[i] = getProbability(antPath[i][:j+1], pheromoneMatrix[antPath[i][j]], visibilityMatrix[antPath[i][j]], alpha, beta) #Encontra as probabilidades de movimento 
                        antPath[i][j+1] = selectMove(antPath[i][:j+1],probabilityMatrix[i]) #Insere o movimento na lista da formiga                        
                #Calcula os caminhos construídos
                antPathLength[i] = getPathLength(antPath[i], weightMatrix) 
                avgLength += antPathLength[i]

                #Calcula a variação de feromônio para a próxima iteração
                pheromoneDepositAmount =  Q / antPathLength[i]
                for j in range(cities - 1):
                        #Atualiza a variação de feromônios para a próxima iteração
                        pheromoneVariationMatrix[antPath[i][j]][antPath[i][j+1]] += pheromoneDepositAmount
                #Deposita feromônio na trilha da ultima cidade para a primeira
                pheromoneVariationMatrix[antPath[i][len(antPath)-1]][antPath[i][0]] += pheromoneDepositAmount


        #Insere o reforço das formigas elitistas
        for i in range(len(bestPath)-1):
                pheromoneVariationMatrix[bestPath[i]][bestPath[i+1]] += elitistAnts * elitistPheromoneDeposit

        pheromoneVariationMatrix[bestPath[len(bestPath)-1]][bestPath[0]] += elitistAnts * elitistPheromoneDeposit
        
        #Calcula a média do caminho
        avgLength = avgLength/ants
        iterationAveragePathLength.append(avgLength)

        bestAnt = antPathLength.tolist().index(min(antPathLength)) #Encontra o indice da melhor formiga
        iterationBestPathLength.append(antPathLength[bestAnt]) #Incrementa a lista de melhores resultados
        #Verifica se o melhor caminho da iteração é o melhor até agora e faz a troca
        if (antPathLength[bestAnt] < bestPathLength):
                bestPath = antPath[bestAnt]
                bestPathLength = antPathLength[bestAnt]
                elitistPheromoneDeposit = Q/bestPathLength
        bestPathList.append(bestPathLength)
        
        #Atualiza os feromônios
        pheromoneMatrix = pheromoneVariationMatrix

        meanItTime = (meanItTime + time.time() - itStart)/2 

executionTime = time.time() - start
if(printExecutionTime):
        print("\nTempo de execução: "+str(executionTime)+"s")
        print("Tempo médio de execução de cada iteração: "+str(meanItTime)+"s")
print("\nComprimento do melhor caminho: "+str(bestPathLength)+"\n")
if(printPheromoneTrails):
        printPheromoneTrails(pheromoneMatrix, data)
if(printPath):
        printPath(bestPath,data)
if(printPerformance):
        plt.plot(iterationAveragePathLength,'b-',label="Tamanho médio do caminho")
        plt.plot(iterationBestPathLength,'r-',label="Melhor tamanho para a iteração")
        plt.plot(bestPathList,'g-',label="Melhor caminho encontrado")
        plt.legend()
        plt.show()