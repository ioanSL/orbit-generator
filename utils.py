import json

import numpy as np


def custom_fibonacci(n):
    initial_sequence = [2, 3]
    for i in range(n):
        initial_sequence.append(initial_sequence[-1] + initial_sequence[-2])

    return initial_sequence[2:]


def gen_metadata(meta_planet):
    with open("test/{}.json".format(meta_planet["name"]), "w") as metafile:
        string = json.dumps(meta_planet, indent=4)
        metafile.write(string)


def lum_perc(cos):
    u = np.log(1 + 5 * np.abs(cos)) / np.log(1 + 5)
    return u


def colorize(biome_list, c):

    A = np.zeros_like(c)
    A[c > 0.5] = ((c[c > 0.5] - 0.5) / 0.5) * 8000  # solid
    A[c < 0.5] = ((c[c < 0.5] - 0.5) / 0.5) * 12000  # liquid

    rgbref = np.zeros((len(c), 4))
    pond_tot = np.zeros_like(c)

    for biome in biome_list:
        ok = np.ones_like(pond_tot, dtype=np.bool)

        if biome["minA"] is not None:
            ok = ok & (A >= biome["minA"])
        if biome["maxA"] is not None:
            ok = ok & (A <= biome["maxA"])

        pond = np.ones_like(pond_tot)

        if biome["A"] is not None:
            pond[ok] *= np.exp(-(((A[ok] - biome["A"]) / biome["vA"]) ** 2))

        rgbref[ok, 0] += pond[ok] * biome["r"]
        rgbref[ok, 1] += pond[ok] * biome["g"]
        rgbref[ok, 2] += pond[ok] * biome["b"]
        rgbref[ok, 3] += pond[ok] * biome["ref"]

        pond_tot[ok] += pond[ok]

    rgbref[:, 0] /= 255 * pond_tot
    rgbref[:, 1] /= 255 * pond_tot
    rgbref[:, 2] /= 255 * pond_tot
    rgbref[:, 3] /= pond_tot

    return rgbref
