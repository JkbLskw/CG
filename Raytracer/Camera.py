from Color import Color
from Plane import Plane
from Triangle import Triangle
from Vector import Vector
from Spehre import Spehre
import math
from Ray import Ray

class Camera(object):

    pixelWidth = 0
    pixelHeight = 0
    LOWEST = 0.0001

    def __init__(self, e, c, up, wRes, hRes, aspectRatio, backgroundColor, objectList, image, light, fov, environmentColor, maxlevel=2):
        self.e = e
        self.c = c
        self.up = up
        self.f = (c - e).normalized()
        self.s = (self.f.cross(self.up)).normalized()
        self.u = (self.s.cross(self.f)).scale(-1)
        self.fov = fov
        self.alpha = self.fov / 2.0
        self.height = 2 * math.tan(self.alpha)
        self.width = aspectRatio * self.height #aspectratio * height

        self.wRes = wRes
        self.hRes = hRes
        self.pixelWidth = self.width / (self.wRes - 1)
        self.pixelHeight = self.height / (self.hRes - 1)

        self.backgroundColor = backgroundColor
        self.objectList = objectList
        self.image = image

        self.light = light
        self.environmentColor = environmentColor
        self.lightColor = self.light.color

        self.maxlevel = maxlevel

    # set the pixels
    def castRay(self, start_x=0, start_y=0, end_x=0, end_y=0, level = 1):
        count = 0
        for x in range(self.wRes):
            for y in range(self.hRes):
                #if x >= start_x and x < end_x and y >= start_y and y < end_y:
                    count += 1
                    ray = self.calcRay(x, y)
                    color = self.traceRay(level, ray)
                    rgb = color.colorRGB(color)
                    self.image.putpixel((x, y), rgb)

        return self.image

    # gibt naehestes object mit distanz zurueck
    def min(self, ray):
        minDist = float("inf")
        minObj = None
        for obj in self.objectList:
            hitDistance = obj.intersectionParameter(ray)
            if hitDistance:
                if hitDistance > 0 and hitDistance < minDist:
                    minDist = hitDistance
                    minObj = obj
        return (minObj, minDist)

    # rekursive methode zur farb- und reflexionsbestimmung
    def traceRay(self, level, ray):
        (minObj, minDist) = self.min(ray)
        if minDist > self.LOWEST and minDist < float("inf"): # wenn distanz zwischen niedrigster und weitester
            hitPoint = ray.origin + ray.direction.scale(minDist)
            hitPointNormale = minObj.normalAt(hitPoint)
            raylight = self.calcRayLight(ray.pointAtParameter(minDist))

            color = minObj.material.color # standard color of this object

            if not self.calcShadow(raylight, minObj):
                color = minObj.material.calculateColor(self.lightColor, self.environmentColor, minObj.material.color, raylight.direction, ray.direction, hitPointNormale, hitPoint) # color berechnung
            else:
                color = minObj.material.calculateAmbientColor(minObj.material.color, self.environmentColor, hitPoint) # color berechnung nur umgebungslicht

            if level >= self.maxlevel:# or isinstance(minObj, Plane): # abbruch der rekursion
                return color

            refRay = Ray(hitPoint, ray.direction.reflect(hitPointNormale))
            refColor = self.traceRay(level+1, refRay)

            red = color.x + (refColor.x * minObj.material.gloss)
            green = color.y + (refColor.y * minObj.material.gloss)
            blue = color.z + (refColor.z * minObj.material.gloss)
            return Color((red,green,blue))

        else:
            return self.backgroundColor

    # ray von cam zu punkt
    def calcRay(self,x,y):
        xComp = self.s.scale(x * self.pixelWidth - self.width / 2)
        yComp = self.u.scale(y * self.pixelHeight - self.height / 2)
        ray = Ray(self.e, self.f + xComp + yComp)
        return ray

    # ray von einem punkt zur lichtquelle
    def calcRayLight(self, origin):
        ray = Ray(origin, (self.light.point - origin))
        return ray

    # berechnet die schattierung
    def calcShadow(self, raylight, objConst):
        for obj in self.objectList:
            hit = obj.intersectionParameter(raylight)
            if hit:
                if hit > self.LOWEST:
                    return True
        return False

    def __repr__(self):
        return "Camera(e:%s, c:%s, up:%s, f:%s, s:%s, u:%s)" % (repr(self.e), repr(self.c), repr(self.up), repr(self.f), repr(self.s), repr(self.u))



