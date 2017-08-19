import math


class Vector(object):

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __mul__(self, c):
        return Vector(self.x * c, self.y * c, self.z * c)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    # Gerichtet reflektiertes Licht
    def reflect(self, other):
        return self - (other * 2) * (self.dot(other))

    # multipl. von Farbvektoren
    def mulVecs(self, other):
        first = self.x * other.x
        second = self.y * other.y
        third = self.z * other.z
        return Vector(first, second, third)

    # Kreuzprodukt
    def cross(self, other):
        x = (self.y * other.z) - (self.z * other.y)
        y = (self.z * other.x) - (self.x * other.z)
        z = (self.x * other.y) - (self.y * other.x)
        return Vector(x,y,z)

    # dividieren durch skalar
    def div(self, c):
        x = self.x / c
        y = self.y / c
        z = self.z / c
        return Vector(x, y, z)

    # multiplizieren mit skalar
    def scale(self, c):
        return Vector(self.x * c, self.y * c, self.z * c)

    # normalize eines vektors
    def normalized(self):
        n = self.norm() # laenge berechnen
        return Vector(self.x / n, self.y / n, self.z / n) # durch laenge dividieren

    # laenge berechnen
    def norm(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))

    def leng(self):
        l = math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))
        return l

    # skalarprodukt berechnen
    def dot(self, other):
        return float(self.x * other.x + self.y * other.y + self.z * other.z)

    def __repr__(self):
        return "Vector(x:%s, y:%s, z:%s)" % (self.x, self.y, self.z)