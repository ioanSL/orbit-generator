from random import uniform

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from geometry import cos_vec, normal, reflection
from noise import background, double_perlin3D
from utils import colorize, lum_perc


class Exo:
    def __init__(self):
        self.res = 800
        self.radius = uniform(0.2, 0.5)

        self.multi_sampling = 1

        self.eps = 1 / (100 * self.res)

        self.atmos_size = 0.02
        self.atmos_color = (0.6, 0.851, 0.912)

        self.x, self.y = np.meshgrid(np.linspace(-0.5, 0.5, self.res), np.linspace(-0.5, 0.5, self.res))

        self.dx, self.dy = np.meshgrid(
            np.linspace(0, 1 / self.res, self.multi_sampling), np.linspace(0, 1 / self.res, self.multi_sampling)
        )

    def gen_rgbbase_and_normal(self, seed=69, rot=0, biome_list=None):
        if biome_list is None:
            # TODO: Throw some error but this case will never happen
            biome_list = []
        im_rgbref_base = np.zeros((self.res, self.res, self.multi_sampling, self.multi_sampling, 4))
        normal_base = np.zeros((self.res, self.res, self.multi_sampling, self.multi_sampling, 3))

        for i in tqdm(range(self.res)):
            for d1 in range(self.multi_sampling):
                for d2 in range(self.multi_sampling):

                    z2 = (
                        self.radius ** 2 - (self.x[i, :] + self.dx[d1, d2]) ** 2 - (self.y[i, :] + self.dy[d1, d2]) ** 2
                    )
                    ok = z2 >= 0

                    if np.any(ok):
                        x1, y1, z1 = (
                            (self.x[i, ok] + self.dx[d1, d2]),
                            (self.y[i, ok] + self.dy[d1, d2]),
                            np.sqrt(z2[ok]),
                        )

                        ox1, oz1 = x1, z1

                        x1, z1, = x1 * np.cos(rot) - z1 * np.sin(rot), x1 * np.sin(
                            rot
                        ) + z1 * np.cos(rot)

                        h = double_perlin3D(x1, y1, z1, seed=seed)

                        rgbref = colorize(biome_list, h)

                        dhdx = np.zeros_like(h)
                        dhdy = np.zeros_like(h)
                        dhdz = np.zeros_like(h)

                        dhdx[h > 0.5] = (
                            double_perlin3D(x1[h > 0.5] + self.eps, y1[h > 0.5], z1[h > 0.5], seed=seed) - h[h > 0.5]
                        ) / self.eps
                        dhdy[h > 0.5] = (
                            double_perlin3D(x1[h > 0.5], y1[h > 0.5] + self.eps, z1[h > 0.5], seed=seed) - h[h > 0.5]
                        ) / self.eps
                        dhdz[h > 0.5] = (
                            double_perlin3D(x1[h > 0.5], y1[h > 0.5], z1[h > 0.5] + self.eps, seed=seed) - h[h > 0.5]
                        ) / self.eps

                        norm = normal(ox1, y1, oz1, h, dhdx, dhdy, dhdz, A=0.05)

                        i_var = np.ones_like(h)

                        i_var[h > 0.5] = 0.5 + double_perlin3D(
                            x1[h > 0.5], y1[h > 0.5], z1[h > 0.5], a=20, d=5, persistance=0.8, seed=seed + 214
                        )

                        im_rgbref_base[i, ok, d1, d2, 0] = rgbref[:, 0] * i_var
                        im_rgbref_base[i, ok, d1, d2, 1] = rgbref[:, 1] * i_var
                        im_rgbref_base[i, ok, d1, d2, 2] = rgbref[:, 2] * i_var
                        im_rgbref_base[i, ok, d1, d2, 3] = rgbref[:, 3]

                        normal_base[i, ok, d1, d2, 0] = norm[0]
                        normal_base[i, ok, d1, d2, 1] = norm[1]
                        normal_base[i, ok, d1, d2, 2] = norm[2]

                    im_rgbref_base[i, ~ok, d1, d2, 0] = background(self.x[i, ~ok], self.y[i, ~ok])[0, :]
                    im_rgbref_base[i, ~ok, d1, d2, 1] = background(self.x[i, ~ok], self.y[i, ~ok])[1, :]
                    im_rgbref_base[i, ~ok, d1, d2, 2] = background(self.x[i, ~ok], self.y[i, ~ok])[2, :]

        return im_rgbref_base, normal_base

    def apply_illumination(self, im_rgbref_base, normal_base, ilum=(-0.2, 0, 1)):
        im = np.zeros((self.res, self.res, 3))
        for i in range(self.res):
            for d1 in range(self.multi_sampling):
                for d2 in range(self.multi_sampling):
                    z2 = (
                        self.radius ** 2 - (self.x[i, :] + self.dx[d1, d2]) ** 2 - (self.y[i, :] + self.dy[d1, d2]) ** 2
                    )
                    ok = z2 >= 0

                    if np.any(ok):
                        x1, y1, z1 = (
                            (self.x[i, ok] + self.dx[d1, d2]),
                            (self.y[i, ok] + self.dy[d1, d2]),
                            np.sqrt(z2[ok]),
                        )

                        cos1 = cos_vec(ilum, (x1, y1, z1))
                        norm = (
                            normal_base[i, ok, d1, d2, 0],
                            normal_base[i, ok, d1, d2, 1],
                            normal_base[i, ok, d1, d2, 2],
                        )
                        cos = np.maximum(cos_vec(ilum, norm), cos1 / 2)

                        refvec = reflection((0, 0, -1), norm)
                        refillum = np.where(cos1 >= 0, np.maximum(cos_vec(refvec, ilum), 0) ** 100, 0)

                        u = np.where(cos > 0, lum_perc(cos), 0) / self.multi_sampling ** 2
                        q = refillum * im_rgbref_base[i, ok, d1, d2, 3] / self.multi_sampling ** 2

                        r_sol = im_rgbref_base[i, ok, d1, d2, 0] * u + q
                        g_sol = im_rgbref_base[i, ok, d1, d2, 1] * u + q
                        b_sol = im_rgbref_base[i, ok, d1, d2, 2] * u + q

                        u = np.where(cos1 > 0, lum_perc(cos1), 0) / self.multi_sampling ** 2

                        im[i, ok, 0] += r_sol * u
                        im[i, ok, 1] += g_sol * u
                        im[i, ok, 2] += b_sol * u

                    xx1 = self.x[i, ~ok] + self.dx[d1, d2]
                    yy1 = self.y[i, ~ok] + self.dy[d1, d2]

                    atmos_dens = np.exp(-(np.sqrt(xx1 ** 2 + yy1 ** 2) - self.radius) / (self.atmos_size * self.radius))
                    atmos_illum = atmos_dens * (np.maximum(cos_vec(ilum, (xx1, yy1, 0)), 0))

                    im[i, ~ok, 0] += (
                        im_rgbref_base[i, ~ok, d1, d2, 0] + atmos_illum * self.atmos_color[0]
                    ) / self.multi_sampling ** 2
                    im[i, ~ok, 1] += (
                        im_rgbref_base[i, ~ok, d1, d2, 1] + atmos_illum * self.atmos_color[1]
                    ) / self.multi_sampling ** 2
                    im[i, ~ok, 2] += (
                        im_rgbref_base[i, ~ok, d1, d2, 2] + atmos_illum * self.atmos_color[2]
                    ) / self.multi_sampling ** 2

        np.clip(im, 0, 1, out=im)
        return im

    def gen_image(self, seed, rot, biome_list):
        a, b = self.gen_rgbbase_and_normal(seed=seed, rot=rot, biome_list=biome_list)
        im = self.apply_illumination(a, b)
        plt.axis("off")
        plt.imshow(im)
        plt.imsave("test/out" + str(seed) + ".png", im)
