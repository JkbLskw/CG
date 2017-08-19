class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin # ursprungspunkt
        self.direction = direction.normalized() # richtung des vectors

    def __repr__(self):
        return 'Ray(%s, %s)' %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self, dist):
        return self.origin + self.direction.scale(dist)