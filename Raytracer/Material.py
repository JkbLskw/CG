from Color import Color
from Vector import Vector


class Material(object):
    def __init__(self, color, ambientComp = 1, diffusComp = 0.8, specularComp = 0.2, specularN=64, gloss=0.75):
        self.color = color
        self.ambientComp = ambientComp
        self.diffusComp = diffusComp
        self.specularComp = specularComp
        self.specularN = specularN
        self.gloss = gloss

    def calculateAmbientColor(self, objColor, environmentColor, point = None):

        if isinstance(objColor, CheckerBoardMaterial):
            objColor = objColor.baseColorAt(point)# wenn obj instance von CheckerBoardMaterial: color = baseColorAt

        ambient_vector = objColor.scale(self.ambientComp); # object_color * ambientComp(skalare groesse)

        # berechnung vektor mal vektor (nur bei Farbe)
        first = environmentColor.x * ambient_vector.x
        second = environmentColor.y * ambient_vector.y
        third = environmentColor.z * ambient_vector.z
        v = (first, second, third)
        return Color(v)

    def calculateDiffusColor(self, objColor, lightColor, raylight_direction, hitPointNormale):
        diff_vector = objColor.scale(self.diffusComp) # berechnung object_color * diffusComp(skalare groesse)

        scalar = raylight_direction.dot(hitPointNormale) # scalarprodukt von lichtstrahl und normale des getroffenen punktes

        if scalar >= 0:
            # berechnung vektor mal vektor (nur bei Farbe)
            first = lightColor.x * diff_vector.x
            second = lightColor.y * diff_vector.y
            third = lightColor.z * diff_vector.z
            v = Vector(first, second, third)
            v = v.scale(scalar)
            return Color((v.x, v.y, v.z))
        else:
            return Color((0, 0, 0))

    def calculateSpecularColor(self, objColor, lightColor, ray_direction, raylight_direction, hitPointNormale):
        specular_vector = objColor.scale(self.specularComp) # object_color * specularComp(skalare groesse)

        lightray = (raylight_direction - hitPointNormale.scale((raylight_direction.dot(hitPointNormale))).scale(2)) * (-1) # lightray = R - (N * (R x N)) * 2 * -1
        scalar = lightray.dot(ray_direction.scale(-1)) # scalar lightray mit raydirection (umgedreht)

        if scalar >= 0:
            # berechnung vektor mal vektor (nur bei Farbe)
            first = lightColor.x * specular_vector.x
            second = lightColor.y * specular_vector.y
            third = lightColor.z * specular_vector.z
            v = Vector(first, second, third)
            v = v.scale(scalar ** self.specularN) # multiplizieren des Farbvektors mit der scalaren groeße ** körnung der oberfläche
            return Color((v.x, v.y, v.z))
        else:
            return Color((0, 0, 0))

    def calculateColor(self, lightColor, environmentColor, objColor, raylight_direction, ray_direction, hitPointNormale, point = None):

        if isinstance(objColor, CheckerBoardMaterial):
            objColor = objColor.baseColorAt(point) # wenn obj instance von CheckerBoardMaterial: color = baseColorAt

        ambientColor = self.calculateAmbientColor(objColor, environmentColor)
        diffColor = self.calculateDiffusColor(objColor, lightColor, raylight_direction,hitPointNormale)
        specularColor = self.calculateSpecularColor(objColor, lightColor, ray_direction, raylight_direction, hitPointNormale)

        result_color_vector = ambientColor + specularColor + diffColor # sum farbwerte
        return Color((result_color_vector.x, result_color_vector.y, result_color_vector.z))

class CheckerBoardMaterial(object):
    def __init__(self):
        self.baseColor = Color((1,1,1)) #white
        self.otherColor = Color((0,0,0)) #black
        self.ambientComp = 1.0
        self.diffusComp = 0.6
        self.specularComp = 0.4
        self.checkSize = 2.5

    def baseColorAt(self, p):
        v = Vector(p.x, p.y, p.z)
        v = v.scale((1.0 / self.checkSize))
        if (int(abs(v.x) + 0.5) + int(abs(v.y) + 0.5) + int(abs(v.z) + 0.5)) % 2:
            return self.otherColor
        return self.baseColor
