import time
import sys
import tkinter
from tkinter import *

n = 10

class PathFinder :

    def __init__(self):
        self.win = Tk()

        self.clear()

    def clear(self):
        self.grid_Layout = Frame(self.win, padx = 20, pady = 20)
        self.operations_layout = Frame(self.win, padx = 20, pady = 20)
        self.grid_size = -1
        self.nodes = dict()
        self.visited = dict()
        self.accessable = dict()
        self.buttons = []
        self.source = None
        self.destination = None
        self.launch = None
        self.path = []
        self.instruction = Label(self.win)
        self.setOperations()

    def prepareNodes(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                connections = []
                if i-1 >= 0 :
                    connections.append(self.grid_size*(i-1)+j)
                if i+1 < self.grid_size :
                    connections.append(self.grid_size*(i+1)+j)
                if j-1 >= 0 :
                    connections.append(self.grid_size*i + (j-1))
                if j+1 < self.grid_size :
                    connections.append(self.grid_size*i + (j+1))

                self.nodes[self.grid_size*i + j] = connections
                self.visited[self.grid_size*i + j] = False
                self.accessable[self.grid_size*i + j] = True



    def createLayout(self):
        for i in range(self.grid_size):
            buttonRow = []
            for j in range(self.grid_size):
                b = Button(self.grid_Layout, text = "", bg = '#888A85')
                buttonRow.append(b)
                buttonRow[j].configure(command = lambda r = i, c = j : self.change(r, c))
                buttonRow[j].grid(row = i, column = j)
            self.buttons.append(buttonRow)
        self.grid_Layout.grid(row = 0, column = 0)


    def setOperations(self):
        self.instruction['text'] = 'Enter grid size and hit create'
        self.instruction.grid()
        e =Entry(self.operations_layout,fg='white',text='Enter Grid Size')
        create = Button(self.operations_layout, text="create", command = lambda e=e :self.create(e.get()))
        e.grid()
        create.grid()
        s = StringVar()
        s.set("DFS")
        ops = OptionMenu(self.operations_layout,s,"DFS","BFS")
        ops.grid()
        self.launch = Button(self.operations_layout, text = "Go", command= lambda o=s: [self.findPath(o),self.show()])
        self.launch.grid()
        self.operations_layout.grid(row = 0, column = 1)

    def findPath(self,e):
        print('here')
        if e.get() == "DFS":
            self.DFS(self.source)
        elif e.get() == 'BFS':
            self.BFSDriver(self.source)

    def create(self,n):
        self.clear()
        n = int(n)
        self.grid_size = n
        self.prepareNodes()
        self.createLayout()
        self.instruction['text'] = 'Click on a block to set starting node'

    def change(self, i, j):
        if self.source == None:
            self.source = self.grid_size*i + j
            self.buttons[i][j]['bg'] = '#73D216'
            self.instruction['text'] = 'Click on a block to set Destination node'
        elif self.destination == None:
            self.destination = self.grid_size*i + j
            self.buttons[i][j]['bg'] = '#EDD400'
            self.instruction['text'] = 'Click on a block to set obstracles \n select a traversal algorithm\n and hit go once done !'

        else:
            if self.buttons[i][j]['bg'] == '#888A85':
                self.buttons[i][j]['bg'] = '#000000'
                self.accessable[self.grid_size*i +j] = False
            elif self.buttons[i][j]['bg'] == '#000000':
                self.buttons[i][j]['bg'] = '#888A85'
                self.accessable[self.grid_size*i +j] = True

    def DFS(self,curr):        #DFS
        self.visited[curr] = True
        for node in self.nodes[curr]:
            if not self.visited[node] and self.accessable[node]:
                self.visited[node] = True
                self.display(node)
                if node == self.destination :
                    return True
                if self.DFS(node):
                    self.path.append(node)
                    return True
        return False

    def BFSDriver(self,curr):
        lst = self.BFS(curr)
        if lst:
            prev = self.destination
            self.path.append(prev)
            while lst[prev] != -1:
                self.path.append(lst[prev])
                prev = lst[prev]

    def BFS(self,curr):
        q = []
        prev = [-1]*self.grid_size*self.grid_size
        dist = [sys.maxsize]*self.grid_size*self.grid_size
        self.visited[curr] = True
        dist[curr] = 0
        q.append(curr)
        while q :
            nxt = q.pop(0)
            for node in self.nodes[nxt]:
                if not self.visited[node] and self.accessable[node]:
                    self.visited[node] = True
                    self.display(node)
                    dist[node] = dist[nxt]+1
                    prev[node] = nxt
                    q.append(node)
                    if node == self.destination:
                        return prev
        return None




    def display(self,n):
        if n != self.destination:
            i = n//self.grid_size
            j = n%self.grid_size
            self.buttons[i][j]['bg'] = 'red'
            time.sleep(0.05)
            self.win.update()


    def show(self):
        if(self.path == []):
            self.instruction['text'] = 'No path found'

        else:
            l = self.path[::-1]
            for index in l:
                i = index//self.grid_size
                j = index % self.grid_size
                self.buttons[i][j].configure(bg = 'white')
                time.sleep(0.1)
                self.win.update()


def toGrid(n):
    n = int(n)
    pf = PathFinder(n)
    pf.createLayout()
    pf.win.mainloop()
    print(pf.path)

if __name__ == "__main__":
    # popup = Tk()
    # Label(popup,text = "Enter grid size", padx = 10, pady = 10 ).pack()
    # e = Entry(popup)
    # e.pack()
    # b = Button(popup, text='create', command= lambda e=e ,popup = popup:[popup.quit(),toGrid(e.get())])
    # b.pack()
    # popup.mainloop()
    pf = PathFinder()
    pf.win.mainloop()
