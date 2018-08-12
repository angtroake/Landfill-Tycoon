import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import csv
import random


#    STRUCTURE:     [(currentCordX, currentCoordY)]
LiveVehicles = []


def createVehicle():
    LiveVehicles.append([])



def getNewTarget():




def run():
    matrix = None

    with open("maps/pathfindingtestmap.csv") as csvmap:
        reader = csv.reader(csvmap)
        matrix = list(reader)
    

    grid = Grid(matrix = matrix)
    start = grid.node(1,4)
    end = grid.node(26,13)

    print(len(matrix))

    while(matrix[start.x][start.y] != '1'):
        start = grid.node(random.randint(0, len(matrix[0]))-1, random.randint(0, len(matrix))-1)
        

    finder = AStarFinder()
    path, runs = finder.find_path(start, end, grid)

    print("RUNS: ", runs, "path length: ", len(path))
    print(grid.grid_str(path=path, start=start, end=end))
    print(path[0])
    print(path[1])