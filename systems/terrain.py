# Si vous avez des problèmes avec noise, il y a des chances qu'il faille installer les microsoft C++ build tools
import math

import noise

import numpy as np


def generate_terrain(w, h, terrain_type="flat"):
    # generate  random noise array with 0,1 values
    # 0 = air
    # 1 = rock
    noise_array = np.zeros((w, h))
    if terrain_type == "cave":
        # Complex cave like structure
        for x in range(w):
            for y in range(h):
                # Octaves: precision of the noise
                # Persistence: higher = messiness of the noise/brokenness
                # Lacunarity: higher = more stuff

                noise_array[x][y] = noise.pnoise2(x / 100, y / 100, octaves=4, persistence=0.2, lacunarity=2.0,
                                                  repeatx=w, repeaty=h, base=0)
                if noise_array[x][y] < 0:
                    noise_array[x][y] = 1
                else:
                    noise_array[x][y] = 0

    elif terrain_type == "flat":
        for x in range(w):
            for y in range(h):
                if y > h // 2:
                    noise_array[x][y] = 1
                else:
                    noise_array[x][y] = 0

    elif terrain_type == "bumpy" or terrain_type == "mountainous" or terrain_type == "extreme":
        # Bumpy terrain is generally flat with vertical cliffs

        for x in range(w):
            # Increase the factor to make the cliffs more vertical
            factor = 10
            if terrain_type == "bumpy":
                factor = 100
            if terrain_type == "mountainous":
                factor = 500
            if terrain_type == "extreme":
                factor = 1500

            max_y = noise.pnoise2(x / 100, w / 100, octaves=4, persistence=0.2, lacunarity=2.0, base=0)
            max_y *= factor
            max_y += h
            max_y /= (math.sin(x * math.pi / w) + 1)
            max_y = int(max_y)
            for y in range(h):
                if y > max_y:
                    noise_array[x][y] = 1
                else:
                    noise_array[x][y] = 0

    return noise_array
