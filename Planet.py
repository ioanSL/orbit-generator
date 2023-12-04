import json
from random import sample

import numpy as np
from Biome import Biome
from Exo import Exo
from utils import custom_fibonacci

GALACTIC_CONSTANT = 680000


biome_deep_water = {
    "maxA": 0,
    "minA": None,
    "A": -6000,
    "vA": 3000,
    "T": 40,
    "vT": 30,
    "H": None,
    "vH": None,
    "r": 16,
    "g": 25,
    "b": 36,
    "ref": 0,
}
biome_median_water = {
    "maxA": 0,
    "minA": None,
    "A": -1000,
    "vA": 2000,
    "T": 40,
    "vT": 30,
    "H": None,
    "vH": None,
    "r": 16,
    "g": 25,
    "b": 36,
    "ref": 0.6,
}
biome_shallow_water = {
    "maxA": 0,
    "minA": None,
    "A": -100,
    "vA": 300,
    "T": 40,
    "vT": 30,
    "H": None,
    "vH": None,
    "r": 50,
    "g": 79,
    "b": 114,
    "ref": 0.6,
}

biome_ice = {
    "maxA": None,
    "minA": 0,
    "A": None,
    "vA": None,
    "T": -10,
    "vT": 5,
    "H": None,
    "vH": None,
    "r": 255,
    "g": 255,
    "b": 255,
    "ref": 0.6,
}
biome_water_ice = {
    "maxA": 0,
    "minA": None,
    "A": -500,
    "vA": 500,
    "T": -15,
    "vT": 5,
    "H": None,
    "vH": None,
    "r": 200,
    "g": 200,
    "b": 255,
    "ref": 0.6,
}

biome_cold_ice = {
    "maxA": None,
    "minA": 0,
    "A": None,
    "vA": None,
    "T": -40,
    "vT": 20,
    "H": None,
    "vH": None,
    "r": 255,
    "g": 255,
    "b": 255,
    "ref": 0.6,
}
biome_cold_water_ice = {
    "maxA": 0,
    "minA": None,
    "A": None,
    "vA": None,
    "T": -45,
    "vT": 20,
    "H": None,
    "vH": None,
    "r": 200,
    "g": 200,
    "b": 255,
    "ref": 0.6,
}

biome_tundra = {
    "maxA": None,
    "minA": 0,
    "A": 0,
    "vA": 2000,
    "T": -5,
    "vT": 5,
    "H": 0.5,
    "vH": 2,
    "r": 93,
    "g": 80,
    "b": 35,
    "ref": 0,
}

biome_boreal_forest = {
    "maxA": None,
    "minA": 0,
    "A": 500,
    "vA": 1500,
    "T": 5,
    "vT": 5,
    "H": 2,
    "vH": 2,
    "r": 12,
    "g": 63,
    "b": 7,
    "ref": 0,
}
biome_forest = {
    "maxA": None,
    "minA": 0,
    "A": 500,
    "vA": 1500,
    "T": 15,
    "vT": 5,
    "H": 2.5,
    "vH": 3,
    "r": 0,
    "g": 188,
    "b": 212,
    "ref": 0,
}

biome_cold_desert = {
    "maxA": None,
    "minA": 0,
    "A": 500,
    "vA": 1500,
    "T": 10,
    "vT": 7,
    "H": 0,
    "vH": 1,
    "r": 245,
    "g": 200,
    "b": 151,
    "ref": 0,
}
biome_warm_desert = {
    "maxA": None,
    "minA": 0,
    "A": 500,
    "vA": 1500,
    "T": 25,
    "vT": 7,
    "H": 0,
    "vH": 1,
    "r": 245,
    "g": 200,
    "b": 151,
    "ref": 0,
}

biome_savanah = {
    "maxA": None,
    "minA": 0,
    "A": 0,
    "vA": 2000,
    "T": 25,
    "vT": 5,
    "H": 1,
    "vH": 1.5,
    "r": 66,
    "g": 105,
    "b": 13,
    "ref": 0,
}
biome_humid_savanah = {
    "maxA": None,
    "minA": 0,
    "A": 0,
    "vA": 2000,
    "T": 25,
    "vT": 5,
    "H": 2,
    "vH": 1.5,
    "r": 53,
    "g": 112,
    "b": 46,
    "ref": 0,
}
biome_jungle = {
    "maxA": None,
    "minA": 0,
    "A": 500,
    "vA": 1000,
    "T": 25,
    "vT": 5,
    "H": 3,
    "vH": 1.5,
    "r": 5,
    "g": 50,
    "b": 5,
    "ref": 0,
}

biome_alpine_tundra = {
    "maxA": None,
    "minA": 0,
    "A": 3000,
    "vA": 1500,
    "T": 0,
    "vT": 5,
    "H": 0.5,
    "vH": 3,
    "r": 131,
    "g": 122,
    "b": 75,
    "ref": 0,
}
biome_high_moutain = {
    "maxA": None,
    "minA": 0,
    "A": 6000,
    "vA": 2000,
    "T": None,
    "vT": None,
    "H": None,
    "vH": None,
    "r": 114,
    "g": 97,
    "b": 71,
    "ref": 0,
}


class Planet(Exo):
    def __init__(self, seed):
        """
        Planet Constructor
        :param binary_radius: radius of the planet in python units
        :param composition_properties: composition {element_symbol: {proportion: percentage, density: g/cm^3}}
        """
        super().__init__()
        with open("assets/result.json") as elements:
            self.elements_dict = json.load(elements)
            self.chosen_elements = sample(self.elements_dict["elements"], 7)
            self.proportion = custom_fibonacci(len(self.chosen_elements))
            total_proportion = sum(self.proportion)

            for p in range(len(self.proportion)):
                self.proportion[p] = self.proportion[p] / total_proportion

        self.binary_radius = self.radius
        self.galactic_radius = self._calculate_galactic_radius()
        self.volume = self._calculate_volume()
        self.mass = self._calculate_mass()
        self.mass_is_unknown = False
        self.gravity = self._calculate_gravitation()
        self.seed = seed
        # TODO: Generate biomes according to design. Check Trello ticket Rules for Planet Generation
        self.biome_list = []
        self._generate_biome()
        #self.biome_list = [
        #    biome_water_ice,
        #    biome_cold_ice,
        #    biome_cold_water_ice,
        #    biome_tundra,
        #    biome_boreal_forest,
        #    biome_forest,
        #    biome_savanah,
        #    biome_humid_savanah,
        #    biome_alpine_tundra,
        #    biome_high_moutain,
        #    biome_warm_desert,
        #    biome_cold_desert,
        #    biome_jungle,
        #    biome_ice,
        #    biome_shallow_water,
        #    biome_median_water,
        #    biome_deep_water,
        #]

    def _generate_biome(self):
        altitude_start = -6000
        for i in range(len(self.chosen_elements)):
            B = Biome(self.chosen_elements[i], self.proportion[i])
            new_offset = B.set_altitude(altitude_start)
            altitude_start = new_offset
            self.biome_list.append(B.get_biome())

    def _search_for_element_properties(self, element_name: str) -> dict:
        for element_properties in self.elements_dict["elements"]:
            if element_name in element_properties.values():
                return element_properties

    def _calculate_volume(self):
        """
        volume = 4/3 * pi * radius^3
        result is given in Km^3
        """
        return (4 / 3) * np.pi * pow(self.galactic_radius, 3)

    def _calculate_galactic_radius(self):
        """
        planet_radius = binary_radius * 640000
        result is given in Km
        """
        return self.binary_radius * GALACTIC_CONSTANT

    def _calculate_gravitation(self):
        """
        g = G * m / r² where G = Newton's constant
        """
        if not self.mass_is_unknown:
            NEWTON_CONSTANT = 6.67408 * pow(10, -11)
            self.gravity = (NEWTON_CONSTANT * self.mass) / pow(self.galactic_radius, 2)
        else:
            self.gravity = np.inf
        return self.gravity

    def _calculate_mass(self):
        """
        mass = Volume[cm^3] * density[g/cm^3]
        """
        total_volume = 0
        for index in range(len(self.proportion)):
            if not self.chosen_elements[index]["density"]:
                self.mass_is_unknown = True
                total_volume = np.inf
                break

            total_volume += (self.volume * 100000 * self.proportion[index]) * self.chosen_elements[index]["density"]
        return total_volume / 1000000

    def get_attributes(self):
        metadata = []
        for index in range(len(self.chosen_elements)):
            metadata.append({"element": self.chosen_elements[index]["name"], "proportion": self.proportion[index]})
        return {
            "name": "Planet-{}".format(self.seed),
            "description": "Elemental planet formed mostly by hopes and dreams",
            "image": "IPFS_link",
            "attributes": {"elements": metadata, "planetary_mass": str(self.mass), "gravity_force": str(self.gravity)},
        }

    def generate_biome(self):
        """
        Function design to generate a random biome
        """
        for element_proportion in range(len(self.proportion)):
            self.biome_list[element_proportion]["r"] = self.chosen_elements[element_proportion]["rgb"][0]
            self.biome_list[element_proportion]["g"] = self.chosen_elements[element_proportion]["rgb"][1]
            self.biome_list[element_proportion]["b"] = self.chosen_elements[element_proportion]["rgb"][2]

        return self.get_attributes()


if __name__ == "__main__":
    P = Planet(983427862378)
    # generate_biome()
    print(P.get_attributes())
