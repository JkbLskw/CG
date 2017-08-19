from Vector import Vector


class Point(object):

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def __add__(self, vector):
        x = self.x + vector.x
        y = self.y + vector.y
        z = self.z + vector.z
        return Point(x, y, z)

    def __repr__(self):
        return "Point(x:%s, y=%s, z=%s)" % (self.x, self.y, self.z)
