import random

import matplotlib.pyplot as plt

UNTOUCHED = 0
VISITED = 1

height = 20
width = 20

class Vertex:
    def __init__(self, label):
        self.label = label
        self.neighbs = set([])
        self.walls = {}
        self.state = UNTOUCHED

    def __repr__(self):
        return "{}".format(self.label)

    def add_wall(self, cell, wall):
        self.walls[cell] = wall

    def unvisited_neighbs(self):
        return [neigh for neigh in self.neighbs if neigh.state == UNTOUCHED]

class Graph:
    def __init__(self, col, edge_col):
        self.vertices = {}
        self.col = col
        self.edge_col = edge_col

    def add_vertex(self, label):
        self.vertices[label] = Vertex(label)
        return self.vertices[label]
    def add_edge(self, label1, label2):
        self.vertices[label1].neighbs.add(self.vertices[label2])
        self.vertices[label2].neighbs.add(self.vertices[label1])
    def remove_edge(self, label1, label2):
        if self.vertices[label2] in self.vertices[label1].neighbs:
            self.vertices[label1].neighbs.remove(self.vertices[label2])
        if self.vertices[label1] in self.vertices[label2].neighbs:
            self.vertices[label2].neighbs.remove(self.vertices[label1])

    def draw(self):
        for vertex in self.vertices.values():
            #plt.plot(vertex.label[0], vertex.label[1], self.col)
            for neigh in vertex.neighbs:
                plt.plot([vertex.label[0], neigh.label[0]], [vertex.label[1], neigh.label[1]], self.edge_col)


def do_maze():
    maze = Graph("ro", "k-")
    allPaths = Graph('go', "k--")
    path = Graph('', 'g-')
    stack = []


    for i in range(width):
        for j in range(height):
            maze.add_vertex((i, j))
            if i < width - 1 and j < height - 1:
                pathi = i + .5
                pathj = j + .5
                vertice = allPaths.add_vertex((pathi , pathj))
                vertice.add_wall((pathi, pathj + 1), ((i, j + 1), (i + 1, j + 1))) # top wall
                vertice.add_wall((pathi + 1, pathj), ((i + 1, j + 1), (i + 1, j))) # right wall

                if i > 0:
                    allPaths.add_edge((i + .5, j + .5), (i - 1 + .5, j + .5))
                    vertice.add_wall((pathi - 1, pathj), ((i, j), (i, j + 1)))  # left wall
                if j > 0:
                    allPaths.add_edge((i + .5, j + .5), (i + .5, j - 1 + .5))
                    vertice.add_wall((pathi, pathj - 1), ((i, j), (i + 1, j))) # bottom wall

            if i > 0:
                maze.add_edge((i, j), (i-1, j))
            if j > 0:
                maze.add_edge((i, j), (i, j-1))

    #maze.remove_edge((0, 0), (0, 1))
    #maze.draw()
    #allPaths.draw()
    #plt.show()

    start = allPaths.vertices[(0.5, 0.5)]
    stack.append(start);
    start.state = VISITED

    while stack:
        cell = stack[-1]
        unvisited = cell.unvisited_neighbs()
        if unvisited:
            random.shuffle(unvisited)
            next_cell = unvisited.pop()
            maze.remove_edge(cell.walls[next_cell.label][0], cell.walls[next_cell.label][1])
            next_cell.state = VISITED
            stack.append(next_cell)
            path.add_vertex(cell.label)
            path.add_vertex(next_cell.label)
            path.add_edge(cell.label, next_cell.label)
        else:
            stack.pop()

    # remove two random outer walls to make an entrance and exit
    randx1 = random.randint(0, width - 2)
    randx2 = random.randint(0, width - 2)
    maze.remove_edge((randx1, 0), (randx1 + 1, 0))
    maze.remove_edge((randx2, height - 1), (randx2 + 1, height - 1))
    maze.draw()
    plt.show()




for int in range(1):
    do_maze()
    print(".")
print("done")