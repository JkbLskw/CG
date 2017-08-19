from Vector import Vector


class Color(Vector):

    highest = 255
    colorV = Vector(0,0,0)
    def __init__(self, colorV):
        self.colorV = Vector.__init__(self, colorV[0], colorV[1], colorV[2])

    def colorRGB(self, vector):
        return (int(vector.x * self.highest), int(vector.y * self.highest), int(vector.z * self.highest))