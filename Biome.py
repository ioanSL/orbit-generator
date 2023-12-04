"""
This class represents a biome strongly related to the
element that it's contained and where it can be found in the planet.
"""
MIN_ALT = -6000
MAX_ALT = 3000


class Biome:
    def __init__(self, element_properties, proportion):
        self.biome = {
            "maxA": None,
            "minA": None,
            "A": None,
            "vA": None,
            "r": None,
            "g": None,
            "b": None,
            "ref": 0,
        }

        self.element = element_properties
        self.proportion = proportion
        self._set_biome_color()

    def _set_biome_color(self):
        self.biome["r"] = self.element["rgb"][0]
        self.biome["g"] = self.element["rgb"][1]
        self.biome["b"] = self.element["rgb"][2]

    def get_biome(self) -> dict:
        return self.biome

    def set_altitude(self, offset):
        maxA = (self.proportion * 9000) + offset
        self.biome["A"] = offset
        self.biome["vA"] = maxA
        # Lowest altitude
        return maxA


if __name__ == "__main__":
    B = Biome("Hydrogen", 0.5)
