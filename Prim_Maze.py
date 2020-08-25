import sys, random
from PIL import Image

class Pass:
    #Holds information regarding the passage/walls between each Cell of the maze
    def __init__(self, source, destination):
        self.source = source #The source cell of the passage/wall
        self.destination = destination #The destination cell of the passage/wall
        self.passage = False #determines if its a wall or corridor, False = Wall, True = Passage

    def setPassage(self, value):
        self.passage = value

    def getPassage(self, value):
        return self.passage

class Cell:
    #Holds information regarding each point in the maze
    def __init__(self, index, top, right, bottom, left):
        self.visited = False #All cells begin unvisited
        self.top, self.right, self.bottom, self.left = None, None, None, None
        #Creates the Passage objects if there is any
        if top != None:
            self.top = Pass(index, top)
        if right != None:
            self.right = Pass(index, right)
        if bottom != None:
            self.bottom = Pass(index, bottom)
        if left != None:
            self.left = Pass(index, left)

    def setVisited(self, value):
        self.visited = value

    def getVisited(self):
        return self.visited

class MazeGenerator:
    #Creates Mazes using Prim's Algorithm and can output them as an image
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [] #Holds each cell in a single array

    #Creates all of the objects for the maze
    def createGrid(self):
        for i in range(self.width * self.height):
            top, right, bottom, left = None, None, None, None
            if i%self.width > 0:
                left = i-1
            if i%self.width < self.width-1:
                right = i+1
            if i >= self.width:
                top = i-self.width
            if i < self.width*(self.height-1):
                bottom = i+self.width
            self.grid.append(Cell(i, top, right, bottom, left))

    #Finds the paths using Prim's algorithm, randomly each time
    def createMaze(self):
        wallList = []
        start = random.randint(0, len(self.grid)-1)
        self.grid[start].setVisited(True)
        wallList = self.addWallsToList(start, wallList)
        while len(wallList) > 0:
            wallNum = random.randint(0, len(wallList)-1)
            if self.grid[wallList[wallNum].destination].getVisited() == False:
                self.grid[wallList[wallNum].destination].setVisited(True)
                wallList[wallNum].setPassage(True)
                wallList = self.addWallsToList(wallList[wallNum].destination, wallList)
            del wallList[wallNum]

    #Finds all newly discovered walls and adds them to the list
    def addWallsToList(self, index, wallList):
        if self.grid[index].top != None:
            wallList.append(self.grid[index].top)
        if self.grid[index].right != None:
            wallList.append(self.grid[index].right)
        if self.grid[index].bottom != None:
            wallList.append(self.grid[index].bottom)
        if self.grid[index].left != None:
            wallList.append(self.grid[index].left)
        return wallList

    #Turns the Maze into an image
    def displayMaze(self):
        im = Image.new("RGB", (2*self.width+1,2*self.height+1), "#000000")
        pixels = im.load()
        for cell in range(len(self.grid)):
            x = 2*(cell%self.width)+1
            y = 2*(cell/self.width)+1
            pixels[x,y] = (255,255,255)
            if self.grid[cell].top != None and self.grid[cell].top.passage == True:
                pixels[x,y-1] = (255,255,255)
            if self.grid[cell].right != None and self.grid[cell].right.passage == True:
                pixels[x+1,y] = (255,255,255)
            if self.grid[cell].bottom != None and self.grid[cell].bottom.passage == True:
                pixels[x,y+1] = (255,255,255)
            if self.grid[cell].left != None and self.grid[cell].left.passage == True:
                pixels[x-1,y] = (255,255,255)
        return(im)