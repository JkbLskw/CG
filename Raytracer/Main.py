import multiprocessing as mp
import threading

from multiprocessing import Process, Manager

from Camera import Camera
from Color import Color
from Light import Light
from Material import Material, CheckerBoardMaterial
from Plane import Plane
from Point import Point
from Vector import Vector
from Spehre import Spehre
from Triangle import Triangle
from PIL import Image
from Camera import Camera

WIDTH = 1600
HEIGHT = 900
output = mp.Queue()
image = Image.new('RGB', (WIDTH, HEIGHT))

def render(cam):
    return cam.castRay()

def main():
    e = Point(-3, 5.75, 3)
    c = Point(-2.25, 6, 1)
    up = Vector(0, 1, 0)
    fov = 45

    aspectRatio = WIDTH / HEIGHT

    light = Light(Point(30,30,10), Color((1,0.85,0.85)))

    white = Color((1,1,1))
    dark = Color((0.2,0.2,0.2))
    black = Color((0.1,0.1,0.1))
    dark_black = Color((0,0,0))
    gold = Color((0.831372,0.686274, 0.215686))
    red = Color((1,0,0))
    green = Color((0,1,0))
    blue = Color((0,0,1))
    yellow = Color((1,1,0))
    gray = Color((0.5,0.5,0.5))
    checkerBoard = CheckerBoardMaterial()

    backgroundColor = dark_black
    environmentColor = Color((0.5, 0.5, 0.5))

    sphere1 = Spehre(Point(3, 2, -10), 2, Material(white, gloss=0.05,specularComp=0.25, diffusComp=0.75))
    sphere2 = Spehre(Point(0, 5, -10), 2, Material(black, gloss=0.3))
    sphere3 = Spehre(Point(-3, 8, -10), 2, Material(white, gloss=0.05,specularComp=0.25, diffusComp=0.75))

    sphere4 = Spehre(Point(-3, 2, -10), 2, Material(white, gloss=0.05, specularComp=0.25, diffusComp=0.75))
    sphere5 = Spehre(Point(3, 8, -10), 2, Material(white, gloss=0.05, specularComp=0.25, diffusComp=0.75))

    triangle01= Triangle(Point(0,7,-10), Point(5,7,-10),Point(2.5,13.5,-15),   Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))
    triangle02 = Triangle(Point(0, 7, -20), Point(0, 7, -10), Point(2.5, 13.5, -15), Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))
    triangle03 = Triangle(Point(5, 7, -10), Point(5, 7, -20), Point(2.5, 13.5, -15),
                         Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))
    triangle04 = Triangle(Point(0, 7, -20), Point(5, 7, -20), Point(2.5, 13.5, -15),
                         Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))
    triangle11 = Triangle(Point(0, 7, -10), Point(5, 7, -10), Point(2.5, 0.5, -15),
                         Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))
    triangle12 = Triangle(Point(0, 7, -20), Point(0, 7, -10), Point(2.5, 0.5, -15),
                         Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))
    triangle13 = Triangle(Point(5, 7, -10), Point(5, 7, -20), Point(2.5, 0.5, -15),
                         Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))
    triangle14 = Triangle(Point(0, 7, -20), Point(5, 7, -20), Point(2.5, 0.5, -15),
                         Material(gold, gloss=0.15, specularComp=0.25, diffusComp=0.75))

    plane = Plane(Point(0,0,0), Vector(0,1,0), Material(checkerBoard, gloss=0.15))

    objectList = [triangle01,triangle02,triangle03,triangle04,triangle11,triangle12,triangle13,triangle14,plane]

    cams = []
    cam = Camera(e, c, up, WIDTH, HEIGHT, aspectRatio, backgroundColor, objectList, image, light, fov, environmentColor)
    cams.append(cam)

    pool = mp.Pool(processes=4)
    results = pool.map(render, cams)

    results[0].show()
    results[0].save('temp.png', 'png')

if __name__ =='__main__':
    main()