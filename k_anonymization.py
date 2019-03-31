from igraph import *
from random import randint
import numpy as np
import numpy
import collections

 # Calculation of the function I that calculates the cost of the operation 
def Icalc(T): 
    valMax = T[0]
    res = 0
    for e in T: 
        res += valMax - e
    return res

# Calculation of the cost cmerge
def cMerge(T,d1,k):
    res = d1 - T[k] + Icalc(T[k+1:min(len(T),2*k+1)])
    return res

# Calculation of the cost cnew
def cNew(T,k):
    t = T[k:min(len(T),2*k)]
    res = Icalc(t)
    return res

# Recursive function of the greedy algorithm that returns an anonymized sequence of degrees
# PARAMETERS
# arrayDegrees : array of the ordered degrees
# kdegree : the k of the k-anonymization
# posIni : initial position (by default 0)
# extension : extension by default equal to k
def greedyRecAlgorithm(arrayDegrees, kdegree, posIni, extension):
    if (posIni+extension >= len(arrayDegrees)-1):
        for i in range(posIni,len(arrayDegrees)):
            arrayDegrees[i] = arrayDegrees[posIni]
        return 0
    else:
        d1 = arrayDegrees[posIni]
        cmerge = cMerge(arrayDegrees,d1,posIni+extension)
        cnew = cNew(arrayDegrees,posIni+extension)
        if(cmerge > cnew): #new groups starts at index k+1
            for i in range(posIni,posIni+extension):
                arrayDegrees[i] = d1
            greedyRecAlgorithm(arrayDegrees,kDegree,posIni+extension,kDegree)
        else: # we merge the k+1th and starts at k+2
            greedyRecAlgorithm(arrayDegrees,kdegree,posIni,extension + 1)

# Backtrack function to construct the correct array of degrees giving the array of couples that is return by the dynamic programming algorithm 
# PARAMETERS
# arrayDegrees : array of the ordered degrees
# array of couples that permit to reconstruct the correct sequence of degrees anonymized
def backtrackFunction(arrayDegrees, tabCouples):
    backtrackCurrent = tabCouples[-1]
    maxRange = len(arrayDegrees)
    backtrack = True
    while backtrack:
        valueToApply = arrayDegrees[backtrackCurrent[1]+1]
        for i in range(backtrackCurrent[1]+1, maxRange):
            arrayDegrees[i] = valueToApply
        maxRange = backtrackCurrent[1]+1
        if(backtrackCurrent[1] == -1):
            backtrack = False
        backtrackCurrent = tabCouples[backtrackCurrent[1]]

# Dynammic Programming algorithm that returns an anonymized sequence of degrees
# PARAMETERS
# arrayDegrees : array of the ordered degrees
# kdegree : the k of the k-anonymization
# empty array that will be filled with couples that permit to reconstruct the correct sequence of degrees anonymized
def DPGraphAnonymization(arrayDegrees, k, array):
    for i in range(1,len(arrayDegrees)+1):
        if i < 2*k: 
            array.append((Icalc(arrayDegrees[0:i]), -1))
        else:
            minI = Icalc(arrayDegrees[0:i])
            tSave = -1
            for t in range(k,i-k+1):
                tmp = array[t-1][0] + Icalc(arrayDegrees[t:i])
                minI = min(minI, tmp)
                if(minI == tmp):
                    tSave = t - 1
            array.append((minI,tSave))
    return array

# Construct Graph that builds the anonymized graph based on the anonymized sequence of degrees and the based graph
# PARAMETERS
# graph : the existing non-anonymized graph
# tabIndexes = [4,2,3,1,0,5] # "4" means that the first "3" of the anonymizedDegrees list is associated with the 4th vertex in the graph
# anonymizedDegrees = [3,3,2,2,1,1]
def constructGraphAlgorithm(graph, tabIndexes, anonymizedDegrees):
    if sum(anonymizedDegrees) % 2 == 1:
        return "Error, sum of d(i) is odd"
    # First we remove the already existing edges of the graph from the anonymizedDegrees list
    for i, value in enumerate(g.degree()):
        anonymizedDegrees[np.where(tabIndexes == i)] = max(0, anonymizedDegrees[np.where(tabIndexes == i)] - value)
    while True:
        if not all([di >= 0 for di in anonymizedDegrees]):
            return "Error one or more d(i) are < 0"
        if all([di == 0 for di in anonymizedDegrees]):
            return graph
        v = np.random.choice((np.where(np.array(anonymizedDegrees) > 0))[0])
        count = anonymizedDegrees[v] 
        anonymizedDegrees[v] = 0
        for w, value in enumerate(anonymizedDegrees):
            if count == 0:
                break
            if value != 0:
                if not graph.are_connected(tabIndexes[v], tabIndexes[w]):
                    graph.add_edge(tabIndexes[v], tabIndexes[w])
                    anonymizedDegrees[w] = anonymizedDegrees[w] - 1
                    count = count - 1
        if count != 0: # Happens in case of a low number of vertex in a graph
            print("The vertex number {} did not succeed to connect to another vertex".format(tabIndexes[v]))
            

if __name__ == "__main__":

    # SETTINGS (k-anonymity and size of the graph) (3 and 30 for a simple example, 15 and 3000 for a big one)
    kDegree = 3
    maxRangeOfVertices = 30 # Must be superior to 20

    # Construction of the base graph
    n = randint(max(20, round(maxRangeOfVertices/10)), maxRangeOfVertices)
    m = max(35, round(n * (1 + randint(1, round(maxRangeOfVertices/10)) / 10)))
    g = Graph.Erdos_Renyi(n=n, m=m)
    plot(g, vertex_label=range(0, g.vcount()))

    # Degree arrays preparation
    d = g.degree()
    arrayIndexes = numpy.argsort(d)[::-1]
    arrayDegrees = numpy.sort(d)[::-1]
    print("Array of degrees (d) : {}".format(d))
    print("Array of degrees sorted (arrayDegrees) : {}".format(arrayDegrees))

    # Greedy algorithm
    arrayDegreesGreedy = np.copy(arrayDegrees)
    greedyRecAlgorithm(arrayDegreesGreedy, kDegree, 0, kDegree)
    
    # Dynamic programming algorithm
    maxDegreeIndex = 0
    arrayDynamic = []
    arrayDegreesDP = np.copy(arrayDegrees)
    tabCouples = DPGraphAnonymization(arrayDegreesDP, kDegree, arrayDynamic)
    backtrackFunction(arrayDegreesDP, tabCouples)

    # RESULTS
    print("Array of degrees anonymized by Greedy Algorithm (arrayDegreesGreedy) : {}".format(arrayDegreesGreedy))
    print("Array of degrees anonymized by DP Algorithm (arrayDegreesDP) : {}".format(arrayDegreesDP))
    print("Cost of anonymization for Greedy Algorithm : {}".format(sum(arrayDegreesGreedy) - sum(d)))
    print("Cost of anonymization for DP Algorithm : {}".format(sum(arrayDegreesDP) - sum(d)))
    print("Difference of cost between the two algorithms : {}".format(abs(sum(arrayDegreesGreedy) - sum(arrayDegreesDP))))

    # Construction algorithm
    gGreedy = g.copy()
    gDP = g.copy()

    constructGraphAlgorithm(gGreedy, arrayIndexes, arrayDegreesGreedy)
    plot(gGreedy, vertex_label=range(0, gGreedy.vcount()))

    constructGraphAlgorithm(gDP, arrayIndexes, arrayDegreesDP)
    plot(gDP, vertex_label=range(0, gDP.vcount()))
    

    print("End of the program")

