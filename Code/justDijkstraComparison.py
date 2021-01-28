import math
from heapq import *
import matplotlib.pyplot as plt

global lineRepeated # Line counter

def printGraph(matrix):#Prints the graph matrix
    digit = len(str(len(matrix)*2-1)) + 2
    print(f'{"":{digit}}',end='')
    for i in range(1,len(matrix)+1):
        print(f'{i:{digit}}',end='')
    print()
    for i in range (0,len(matrix)):
        print(f'{i+1:{digit}}',end='')
        for j in range(0,len(matrix)):
            print(f'{matrix[i][j]:{digit}}', end='')
        print()
    print()

def fillGraph(matrix):#Fills the matrix according to given property wij =i+j, if|i-j|<=3
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix)):
            if abs(i-j) <= 3 and i != j:
                matrix[i][j] = i+j + 2
            else:
                matrix[i][j] = math.inf

def relax(u, v, matrix, pi, d): #Relaxes the edge
    global lineRepeated
    if d[str(v)] > d[str(u)] + matrix[int(u) - 1][int(v) - 1]:
        lineRepeated += 1
        d[str(v)] = d[str(u)] + matrix[int(u) - 1][int(v) - 1]
        lineRepeated += 1
        #print("predecessor ", str(v), "->", u)
        pi[str(v)] = u
        #print("d in method after:  ", d)

def dijkstra(matrix, start, destination):# Dijkstra with line counter
    global lineRepeated
    #Initialize Single Source
    d = {} #Shortest path weight as dictionary
    lineRepeated += 1
    pi = {} # Predecessor as dictionary
    lineRepeated += 1
    for i in range (0, len(matrix)):
        d[str(i+1)] = math.inf # d[v] = ∞
        lineRepeated += 1
        pi[str(i+1)] = None # pi[v] = NIL
    d[str(start)] = 0
    lineRepeated += 1
    Q = list(d.items())
    lineRepeated += 1
    Q = [(y, x) for x, y in Q] # Reversing tuples in a list to (city,weight)
    S = []
    lineRepeated += 1
    heapify(S)
    heapify(Q)

    while Q:
        u = heappop(Q)
        lineRepeated += 1
        heappush(S, u)
        lineRepeated += 1
        #print("Smallest Vertice u:", u[1], "weight:", u[0])
        for i in range(0, len(matrix)):
            if matrix[int(u[1])-1][i] != 0 and matrix[int(u[1])-1][i] != math.inf:
                lineRepeated += 1
                relax(u[1], i+1, matrix, pi, d)
                lineRepeated += 1

        Q = [(y, x) for x, y in Q]  # Reversing tuples in a list to (city,weight)
        Q = dict(Q)
        lineRepeated += 1

        for x in Q: # For just taking the elements which is in Q
            Q[str(x)] = d[str(x)]

        Q = list(Q.items())
        Q = [(y, x) for x, y in Q]  # Reversing tuples in a list to (city,weight)
        heapify(Q)
        #print()
    S = [(y, x) for x, y in S]  # Reversing tuples in a list to (city,weight)
    #print(S)
    #print(pi)


def dijkstraMultipleDestinations(N):
    global lineRepeated
    matrix = [[0 for x in range(N)] for y in range(N)]
    fillGraph(matrix)
    dijkstra(matrix, 1, N)

def main():
    global  lineRepeated
    lineRepeated = 0
    dijkstraMultipleDestinations(10)# N = 10
    print("Line Repeated N 10:", lineRepeated)
    lineRepeated10 = lineRepeated

    lineRepeated = 0
    dijkstraMultipleDestinations(50)# N = 50
    print("Line Repeated N 50:", lineRepeated)
    lineRepeated50 = lineRepeated

    lineRepeated = 0
    dijkstraMultipleDestinations(100)# N = 100
    print("Line Repeated N 100:", lineRepeated)
    lineRepeated100 = lineRepeated

    lineRepeated = 0
    dijkstraMultipleDestinations(200)# N = 200
    print("Line Repeated N 200:", lineRepeated)
    lineRepeated200 = lineRepeated

    lineRepeated = 0
    dijkstraMultipleDestinations(500)# N = 500
    print("Line Repeated N 500:", lineRepeated)
    lineRepeated500 = lineRepeated

    lineRepeated = 0
    dijkstraMultipleDestinations(1000)# N = 1000
    print("Line Repeated N 1000:", lineRepeated)
    lineRepeated1000 = lineRepeated

    lineRepeated = 0
    dijkstraMultipleDestinations(2000)# N = 2000
    print("Line Repeated N 2000:", lineRepeated)
    lineRepeated2000 = lineRepeated

    x = [10, 50, 100, 200, 500, 1000, 2000]
    y = []
    y.append(lineRepeated10)
    y.append(lineRepeated50)
    y.append(lineRepeated100)
    y.append(lineRepeated200)
    y.append(lineRepeated500)
    y.append(lineRepeated1000)
    y.append(lineRepeated2000)

    plt.xlabel("Number Elements")
    plt.ylabel("Running Time")
    plt.title("N=10, 50, 100, 200, 500, 1000, 2000")
    plt.scatter(x, y)# Plot the running times
    plt.show()
