"""
Simplified generator for just basic map terrain without tribes, villages, or resources
"""

import random
import utils

# Setup map values
map_size = 16 # x*x size
initial_land = 0.5 # Proportion of land to total tiles
smoothing = 3 # How many times to smooth landmass
relief = 4
tribes = ['Vengir', 'Bardur', 'Oumaji'] # Tribes in map

# Create initial world map array with tile objects
world_map = [{'type': 'ocean', 'above': None, 'troop': None, 'groundFlag': False} for i in range(map_size ** 2)]
# Type: type of terrain
# Above: resource on tile
# Troop: troop unit on tile
# GroundFlag: to be converted to land in smoothing process

# Randomly make landmasses
j = 0
while j < map_size ** 2 * initial_land:
    cell = random.randrange(0, map_size ** 2)
    if world_map[cell]['type'] == 'ocean':
        j += 1
        world_map[cell]['type'] = 'ground'

# Smooth out landmasses based on surrounding tile types
land_coefficient = (0.5 + relief) / 9

for i in range(smoothing):
    for cell in range(map_size ** 2):
        water_count = 0
        tile_count = 0
        neighbours = utils.round_(cell, 1, map_size)
        for i in range(len(neighbours)):
            if world_map[neighbours[i]]['type'] == 'ocean':
                water_count += 1
            tile_count += 1
        if water_count / tile_count <= land_coefficient:
            world_map[cell]['groundFlag'] = True
    for cell in range(map_size ** 2):
        if world_map[cell]['groundFlag']:
            world_map[cell]['groundFlag'] = False
            world_map[cell]['type'] = 'ground'
        else:
            world_map[cell]['type'] = 'ocean'

# Display options
# print(world_map)

# world_map_2d = [world_map[i * map_size:(i + 1) * map_size] for i in range(map_size)]
# for row in world_map_2d:
#     print(row)

for c in range(map_size ** 2):
    if c % map_size == 0:
        print()
    if world_map[c]['above'] == 'capital':
        print('0', end='')
        continue
    if world_map[c]['above'] == 'village':
        print('v', end='')
        continue
    if world_map[c]['above'] == 'ruin':
        print('r', end='')
        continue
    if world_map[c]['type'] == 'ocean':
        print('o', end='')
        continue
    if world_map[c]['type'] == 'ground':
        print('g', end='')
        continue
    if world_map[c]['type'] == 'forest':
        print('f', end='')
        continue
    if world_map[c]['type'] == 'mountain':
        print('m', end='')
        continue
    if world_map[c]['type'] == 'water':
        print('w', end='')
        continue
