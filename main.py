import secrets

from Planet import Planet
from utils import gen_metadata

if __name__ == "__main__":
    for _ in range(0, 1):
        seed = secrets.randbits(16)
        P = Planet(seed=seed)
        metadata = P.generate_biome()
        P.gen_image(seed=seed, rot=0, biome_list=P.biome_list)
        #gen_metadata(metadata)
