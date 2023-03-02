# Si vous avez des problèmes avec noise, il y a des chances qu'il faille les microsoft C++ build tools
import math

import noise

import time

import numpy as np
#TODO : Tout modifier ici pour plutôt en faire des sprites et les mettre dans un groupe de sprites, ça facilitera beaucoup les collisions
def generate_terrain(w, h, type="flat"):
    # generate  random noise array with 0,1 values
    # 0 = air
    # 1 = rock
    noise_array = np.zeros((w, h))
    if type == "cave":
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

    elif type == "flat":
        for x in range(w):
            for y in range(h):
                if y > h // 2:
                    noise_array[x][y] = 1
                else:
                    noise_array[x][y] = 0

    elif type == "bumpy" or type == "mountainous" or type == "extreme":
        # Bumpy terrain is generally flat with vertical cliffs

        for x in range(w):
            # Increase the factor to make the cliffs more vertical
            factor = 10
            if type == "bumpy":
                factor = 100
            if type == "mountainous":
                factor = 500
            if type == "extreme":
                factor = 1500

            maxY = noise.pnoise2(x / 100, w/100, octaves=4, persistence=0.2, lacunarity=2.0, base=0)
            maxY *= factor
            maxY += h
            maxY /= (math.sin(x*math.pi/w)+1)
            maxY = int(maxY)
            for y in range(h):
                if y > maxY:
                    noise_array[x][y] = 1
                else:
                    noise_array[x][y] = 0

    return noise_array


'''
def neighbors(terrain, i, j, L, C):
    possible_neigbors = [(i + di, j + dj) for di in [-1, 0, 1] for dj in [-1, 0, 1]]
    return [terrain[i2][j2] for (i2, j2) in possible_neigbors
            if i2 >= 0 and j2 >= 0 and i2 < L and j2 < C]


def generate_terrain(L, C):
    noisegrid = [[noise.pnoise2(j / C, i / L) for j in range(C)] for i in range(L)]
    terrain = [[int(noisegrid[i][j] > 0.12) for j in range(C)] for i in range(L)]

    for i in range(L):
        for j in range(C):
            if terrain[i][j] == 0:
                nb = neighbors(terrain, i, j, L, C)
                if 1 in nb:
                    terrain[i][j] = 2

    return terrain
'''
