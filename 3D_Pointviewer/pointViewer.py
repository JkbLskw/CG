from tkinter import *
import sys
import random

import copy

import math

WIDTH = 400  # width of canvas
HEIGHT = 400  # height of canvas

HPSIZE = 1  # double of point size (must be integer)
COLOR = "#FF0000"  # rot

ALPHA = 10 * math.pi / 180 # Winkel fuer Drehung

pointList = []  # list of points (used by Canvas.delete(...))


def quit(root=None):
    """ quit programm """
    if root == None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw points """
    global pointList
    for item in can.find_all():
        can.delete(item)
    for point in scaleFrame(pointList):
        x, y = point
        print(point)
        can.create_oval(x - HPSIZE, y - HPSIZE, x + HPSIZE, y + HPSIZE, fill=COLOR, outline=COLOR)

def scaleFrame(scaledPoints):
    "Punkte an Bildschirmaufloesung anpassen"
    temp_points = [list(x) for x in scaledPoints]
    m = [[x[0] * WIDTH/2.0 + WIDTH/2,HEIGHT - (x[1] * HEIGHT/2.0 + HEIGHT/2.0)] for x in temp_points]
    return m

def rotYp():
    """ rotate counterclockwise around y axis """
    global ALPHA
    global pointList
    pointList = rotateMatrix(ALPHA, pointList)
    draw()


def rotYn():
    """ rotate clockwise around y axis """
    global ALPHA
    global pointList
    pointList = rotateMatrix(ALPHA, pointList)
    draw()

def moveBoundingBox(deltaValues, points):
    "Verschieben der Bounding Box durch Abzug der Delta Werte auf den jeweils x,y,z Werten"
    deltaX, deltaY, deltaZ = deltaValues
    print(points)
    temp_points = [list(x) for x in points]
    print(temp_points)
    movedX = [x[0] - deltaX for x in temp_points]
    movedY = [x[1] - deltaY for x in temp_points]
    movedZ = [x[2] - deltaZ for x in temp_points]

    return zip(movedX, movedY, movedZ)

def createBoundingBox(points):
    "Bounding Box erstellen indem die min und max Werte des Modells ausgerechnet werden"
    temp_points = [list(x) for x in points]

    # Min-Werte berechnen
    xMin = min([x[0] for x in temp_points])
    yMin = min([x[1] for x in temp_points])
    zMin = min([x[2] for x in temp_points])

    # Max-Werte berechnen
    xMax = max([x[0] for x in temp_points])
    yMax = max([x[1] for x in temp_points])
    zMax = max([x[2] for x in temp_points])

    return xMin, yMin, zMin, xMax, yMax, zMax

def calcDeltas(boundingBox):
    "Berechnen der Deltas, die zum verschieben der Bounding Box benoetigt werden"
    xMin, yMin, zMin, xMax, yMax, zMax = boundingBox

    deltaX = xMin + ((xMax - xMin) / 2)
    deltaY = yMin + ((yMax - yMin) / 2)
    deltaZ = zMin + ((zMax - zMin) / 2)

    return deltaX, deltaY, deltaZ

def scaleBoundingBox(movedPoints):
    "Skalieren der Bounding Box indem jeder x,y,z Wert durch den xMax oder yMax geteilt wird"
    temp_points = [list(x) for x in movedPoints]

    xMax = max([x[0] for x in temp_points])
    yMax = max([x[1] for x in temp_points])
    zMax = max([x[2] for x in temp_points])

    if xMax > yMax:
        div = xMax
    else:
        div = yMax

    return [[x[0] / div, x[1] / div, x[2] / div] for x in temp_points]

def rotateMatrix(alpha,scaledPoints):
    "Matrix zum Rotieren um die Y-Achse"
    temp_points = [list(x) for x in scaledPoints]
    return [[math.cos(alpha)*p[0] - math.sin(alpha)*p[2], p[1], math.sin(alpha) * p[0]+math.cos(alpha) * p[2]] for p in temp_points]

if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 2:
        sys.exit(-1)

    # Einlesen
    temp_points = copy.deepcopy([map(float, x.split()) for x in open(sys.argv[1]).readlines()])
    temp_points2 = copy.deepcopy(temp_points)

    # Bounding Box (verschieben zum Mittelpunkt, skalieren, anpassen an Auflösung)
    deltaValues = calcDeltas(createBoundingBox(temp_points))
    movedPoints = moveBoundingBox(deltaValues, temp_points2)
    scaledPoints = scaleBoundingBox(movedPoints)

    # Punkte setzen
    pointList = scaledPoints

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()
