import os
import shutil

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from Planet import Planet

fig = plt.figure()

N_seconds = 10
FPS = 60

N_frame = FPS * N_seconds

phi = np.linspace(0, 2 * np.pi, N_frame)

ims = []

os.mkdir("temp")
seed = 111
P = Planet(seed=seed)
metadata = P.generate_biome()
for i in tqdm(range(N_frame)):
    P.gen_image(seed=seed, rot=phi[i], biome_list=P.biome_list)

os.system(
    "ffmpeg -r " + str(FPS) + " -f image2 -s 1024x1024 -i temp/out%d.png -vcodec libx264 -crf 25 "
    "-pix_fmt yuv420p test.mp4"
)

shutil.rmtree("temp")
