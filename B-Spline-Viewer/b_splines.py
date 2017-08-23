from Tkinter import *
from Canvas import *
import sys
import numpy as np

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue (color of control-points and polygon)

BCOLOR = "#000000" # black (color of bezier curve)
BWIDTH = 2 # width of bezier curve

controlpoints = []   # list of (control-)points
elementList = [] # list of elements (used by Canvas.delete(...))


def drawPoints():
    """ draw (control-)points """
    for p in controlpoints:
	    element = can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                  p[0]+HPSIZE, p[1]+HPSIZE,
                                  fill=CCOLOR, outline=CCOLOR)
	    elementList.append(element)


def drawPolygon():
    """ draw (control-)polygon conecting (control-)points """
    if len(controlpoints) > 1:
        for i in range(len(controlpoints)-1):
            element = can.create_line(controlpoints[i][0], controlpoints[i][1],
                                      controlpoints[i+1][0], controlpoints[i+1][1],
                                      fill=CCOLOR)
            elementList.append(element)

def calc_r(knotvector, t):
    temp_v_idx = 0
    for idx in range(0, len(knotvector) - 1):
        if knotvector[idx] <= t:
            temp_v_idx = idx

    print("r:", temp_v_idx)
    return temp_v_idx



def deboor(degree, controlpoints, knotvector, t):
    r = calc_r(knotvector, t)
    for j in range(0, degree):
        print("j:", j)
        i_range = r-degree+j+1
        for i in range(r, i_range):
            print("i:", i)

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)

    p = controlpoints # Kontrollpunkte
    degree = 4 # Grad der Kurve
    n = 4 # Anzahl der zu interpolierenden Punkte
    knotvector = [0,1,2,3,4,5,6,7,8,9] # Knotenvektor
    t = 1.0/4.0
    deboor(degree, p, knotvector, t)

    drawPoints()
    drawPolygon()



def clearAll():
    """ clear all (point list and canvas) """
    can.delete(*elementList)
    del controlpoints[:]


def mouseEvent(event):
    """ process mouse events """
    print "left mouse button clicked at ", event.x, event.y
    controlpoints.append([event.x, event.y])
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.bind("<Button-1>",mouseEvent)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="Clear", command=clearAll)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # start
    mw.mainloop()

