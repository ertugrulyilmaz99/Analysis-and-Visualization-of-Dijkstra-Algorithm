import math
from heapq import *
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
import time
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from justDijkstraComparison import main
#It is so important for closing the plot windows for the backends which is MacOSX
plt.switch_backend('TkAgg')

#**************RUN THE PROJECT WITH PYTHON3****************

def takeNumberN():#Takes the city number for button
    global numberN
    global numberNStr
    numberNStr = numberN.get()
    openingWindow.quit()
    openingWindow.destroy()
    return numberNStr

def runDijkstra():#Run dijkstra for button
    global startingNode
    global destinationNode
    startingNode = numberS.get()
    destinationNode = numberD.get()
    dijkstra(matrix, int(startingNode), int(destinationNode),G)

def getGraphSpecs(G):# Gets the graph object specs before plotting
    colors = nx.get_edge_attributes(G, 'color').values()
    weights = nx.get_edge_attributes(G, 'weight').values()

    pos = nx.circular_layout(G)
    nx.draw(G, pos,
            width=1,
            edge_color=colors,
            with_labels=True,
            node_color='lightgreen')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos,edge_labels=labels)

def printGraph(matrix):#Prints the graph matrix
    digit = len(str(len(matrix)*2-1)) + 2
    print(f'{"":{digit}}',end='')
    for i in range(1,N+1):
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

def relax(u, v, matrix, pi, d, G):#Relax operation for a path
    G.add_edge(str(u), str(v), weight=matrix[int(u) - 1][int(v) - 1], color='b')
    getGraphSpecs(G)

    plt.draw()
    plt.pause(0.10)
    time.sleep(0.1)
    plt.clf()

    if d[str(v)] > d[str(u)] + matrix[int(u) - 1][int(v) - 1]:

        d[str(v)] = d[str(u)] + matrix[int(u) - 1][int(v) - 1]
        print("predecessor ", str(v), "->", u)
        pi[str(v)] = u

def dijkstra(matrix, start, destination,G):#Runs dijkstra algorithm
    G.remove_edges_from(list(G.edges))
    #Initialize Single Source
    d = {} #Shortest path weight as dictionary
    pi = {} # Predecessor as dictionary
    for i in range (0, len(matrix)):
        d[str(i+1)] = math.inf # d[v] = ∞
        pi[str(i+1)] = None # pi[v] = NIL
    d[str(start)] = 0
    print("d: ", d)
    print("pi: ", pi)
    Q = list(d.items())
    Q = [(y, x) for x, y in Q] # Reversing tuples in a list to (city,weight)
    S = []
    heapify(S)
    heapify(Q)

    while Q:
        print("While Q: ", Q)
        u = heappop(Q)# Popping the min
        heappush(S, u)# Pushing min to S
        print("Smallest Vertice u:", u[1], "weight:", u[0])
        for i in range(0, len(matrix)):
            if matrix[int(u[1])-1][i] != 0 and matrix[int(u[1])-1][i] != math.inf:
                relax(u[1], i+1, matrix, pi, d, G)

        Q = [(y, x) for x, y in Q]  # Reversing tuples in a list to (city,weight)
        Q = dict(Q)

        for x in Q: # For just taking the elements which is in Q
            Q[str(x)] = d[str(x)]

        Q = list(Q.items())
        Q = [(y, x) for x, y in Q]  # Reversing tuples in a list to (city,weight)
        heapify(Q)
        print()
    S = [(y, x) for x, y in S]  # Reversing tuples in a list to (city,weight)
    print(S)
    print(pi)

    tmp = str(destination)# Temporary to show iterations
    while(pi[tmp] != None):#red edges
        G.remove_edge(pi[tmp], tmp)# Remove the blue edge
        if G.has_edge(tmp, pi[tmp]):
            G.remove_edge(tmp, pi[tmp])# Remove the opposite side blue edge

        G.add_edge(pi[tmp], tmp, weight=matrix[int(pi[tmp])-1][int(tmp)-1], color='r', width=5)# Add red edge
        tmp = pi[tmp]# Next vertex on the path
        getGraphSpecs(G) # Get the new graph visual


        plt.draw()
        time.sleep(0.3)
        plt.pause(0.05)
        plt.clf()

def writeToGraph(matrix, G): #Writes the matrix graph inside the graph object
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix)):
            if matrix[i][j] != math.inf:
                G.add_edge(str(i+1), str(j+1), weight=matrix[i][j], color='b')

global matrix
global G

openingWindow = Tk()
openingWindow.title("Welcome to Dijkstra Visualization Program")
openingWindow.geometry("350x130")
openingWindow.eval('tk::PlaceWindow . center')
openingWindow.configure(background='yellow')
howMany = Label(openingWindow, text="How many cities \nyou want to implement?", relief=RAISED, anchor=CENTER ).grid(row=0,padx=90)
numberN = Entry(openingWindow)
numberN.grid(row=1)
numberN.focus_set()
b = Button(openingWindow,text='Create Graph', command=takeNumberN, fg='brown4') # For create graph
b.grid(row=2)
c = Button(openingWindow,text='Or See Running Times\n(Can Take A While)', command=main, fg='blue2') # To see running times
c.grid(row=3)
openingWindow.mainloop()


N = int(numberNStr)
matrix = [[0 for x in range(N)] for y in range(N)]
printGraph(matrix)# Empty graph matrix
fillGraph(matrix)# Filling the graph matrix
printGraph(matrix)# Filled graph matrix
G = nx.DiGraph()# Directed Graph
writeToGraph(matrix, G)# Write graph matrix to graph
getGraphSpecs(G)# Prepares the graph
fig = plt.gcf()# Gets plt's current graph



mainWindow = Tk()
mainWindow.geometry("1000x500")
mainWindow.eval('tk::PlaceWindow . center')
mainWindow.title("Graph Window")
mainWindow.configure(background='cyan3')
leftSide = Frame(mainWindow)
leftSide.grid(row=0,column=0)
rightSide = Frame(mainWindow)
rightSide.grid(row=0,column=1)
forS = Label( rightSide, text="Starting Node S:", relief=RAISED ).grid(row=0,column=0,ipadx=5,pady=1,padx=1,sticky='W')
forD = Label( rightSide, text="Destinaiton Node D:", relief=RAISED).grid(row=1,column=0,pady=1,padx=1,sticky='W' )
runButton = Button(rightSide,text='Run Dijkstra', command=runDijkstra, fg='red4').grid(row=2,column=1)

numberS = Entry(rightSide) # Gets starting node information
numberS.grid(row=0,column=1,pady=1,padx=1)
numberS.focus_set()
numberD = Entry(rightSide) # Gets destination node information
numberD.grid(row=1,column=1,pady=1,padx=1)
numberD.focus_set()

canvas = FigureCanvasTkAgg(fig, master=leftSide) # Shows the graph
canvas.draw()

graph = Label(leftSide, text="GRAPH", relief=RAISED ).grid(row=0,column=0)
canvas.get_tk_widget().grid(row=1,column=0)

mainWindow.mainloop()
