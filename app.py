import random
import utils

# Setup map values
map_size = 16 # x*x size
initial_land = 0.5 # Proportion of land to total tiles
smoothing = 3
relief = 4
tribes = ['Vengir', 'Bardur', 'Oumaji'] # Tribes in map

# Setup game info
TRIBES_LIST = ['Xin-xi', 'Imperius', 'Bardur', 'Oumaji', 'Kickoo', 'Hoodrick', 'Luxidoor', 'Vengir', 'Zebasi',
               'Ai-mo', 'Quetzali', 'Yadakk', 'Aquarion', 'Elyrion', 'Polaris']
TERRAIN_TYPES = ['forest', 'fruit', 'game', 'ground', 'mountain']
SPECIAL_TERRAIN = ['crop', 'fish', 'metal', 'ocean', 'ruin', 'village', 'water', 'whale']

# Probability levels
HIGH = 2
MED_HIGH = 1.5
MED = 1
LOW_MED = 0.5
LOW = 0.1

BORDER_EXPANSION = 1 / 3

terrain_probs = {'water': {'Xin-xi': 0, 'Imperius': 0, 'Bardur': 0, 'Oumaji': 0, 'Kickoo': 0.4,
                           'Hoodrick': 0, 'Luxidoor': 0, 'Vengir': 0, 'Zebasi': 0, 'Ai-mo': 0,
                           'Quetzali': 0, 'Yadakk': 0, 'Aquarion': 0.3, 'Elyrion': 0},
                 'forest': {'Xin-xi': MED, 'Imperius': MED, 'Bardur': MED, 'Oumaji': LOW, 'Kickoo': MED,
                            'Hoodrick': MED_HIGH, 'Luxidoor': MED, 'Vengir': MED, 'Zebasi': LOW_MED, 'Ai-mo': MED,
                            'Quetzali': MED, 'Yadakk': LOW_MED, 'Aquarion': LOW_MED, 'Elyrion': MED},
                 'mountain': {'Xin-xi': MED_HIGH, 'Imperius': MED, 'Bardur': MED, 'Oumaji': MED, 'Kickoo': LOW_MED,
                              'Hoodrick': LOW_MED, 'Luxidoor': MED, 'Vengir': MED, 'Zebasi': LOW_MED, 'Ai-mo': MED_HIGH,
                              'Quetzali': MED, 'Yadakk': LOW_MED, 'Aquarion': MED, 'Elyrion': LOW_MED},
                 'metal': {'Xin-xi': MED, 'Imperius': MED, 'Bardur': MED, 'Oumaji': MED, 'Kickoo': MED,
                           'Hoodrick': MED, 'Luxidoor': MED, 'Vengir': HIGH, 'Zebasi': MED, 'Ai-mo': MED,
                           'Quetzali': LOW, 'Yadakk': MED, 'Aquarion': MED, 'Elyrion': MED},
                 'fruit': {'Xin-xi': MED, 'Imperius': MED, 'Bardur': MED_HIGH, 'Oumaji': MED, 'Kickoo': MED,
                           'Hoodrick': MED, 'Luxidoor': HIGH, 'Vengir': LOW, 'Zebasi': LOW_MED, 'Ai-mo': MED,
                           'Quetzali': HIGH, 'Yadakk': MED_HIGH, 'Aquarion': MED, 'Elyrion': MED},
                 'crop': {'Xin-xi': MED, 'Imperius': MED, 'Bardur': LOW, 'Oumaji': MED, 'Kickoo': MED,
                          'Hoodrick': MED, 'Luxidoor': MED, 'Vengir': MED, 'Zebasi': MED, 'Ai-mo': LOW,
                          'Quetzali': LOW, 'Yadakk': MED, 'Aquarion': MED, 'Elyrion': MED_HIGH},
                 'game': {'Xin-xi': MED, 'Imperius': MED, 'Bardur': HIGH, 'Oumaji': MED, 'Kickoo': MED,
                          'Hoodrick': MED, 'Luxidoor': LOW_MED, 'Vengir': LOW, 'Zebasi': MED, 'Ai-mo': MED,
                          'Quetzali': MED, 'Yadakk': MED, 'Aquarion': MED, 'Elyrion': MED},
                 'fish': {'Xin-xi': MED, 'Imperius': MED, 'Bardur': MED, 'Oumaji': MED, 'Kickoo': MED_HIGH,
                          'Hoodrick': MED, 'Luxidoor': MED, 'Vengir': LOW, 'Zebasi': MED, 'Ai-mo': MED,
                          'Quetzali': MED, 'Yadakk': MED, 'Aquarion': MED, 'Elyrion': MED},
                 'whale': {'Xin-xi': MED, 'Imperius': MED, 'Bardur': MED, 'Oumaji': MED, 'Kickoo': MED,
                           'Hoodrick': MED, 'Luxidoor': MED, 'Vengir': MED, 'Zebasi': MED, 'Ai-mo': MED,
                           'Quetzali': MED, 'Yadakk': MED, 'Aquarion': MED, 'Elyrion': MED}}

general_probs = {'mountain': 0.15, 'forest': 0.4, 'fruit': 0.5, 'crop': 0.5,
                 'fish': 0.5, 'game': 0.5, 'whale': 0.4, 'metal': 0.5}

# Create initial world map 2D array with tile objects
world_map = [{'type': 'ocean', 'above': None, 'road': False, 'tribe': 'Xin-xi'} for i in range(map_size ** 2)]

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
            world_map[cell]['road'] = True
    for cell in range(map_size ** 2):
        if world_map[cell]['road']:
            world_map[cell]['road'] = False
            world_map[cell]['type'] = 'ground'
        else:
            world_map[cell]['type'] = 'ocean'

# Find possible capital locations
capital_cells = []
capital_map = {}
for tribe in tribes:
    for row in range(2, map_size - 2):
        for column in range(2, map_size - 2):
            if world_map[row * map_size + column]['type'] == 'ground':
                capital_map[row * map_size + column] = 0

# Place capitals
for tribe in tribes:
    max_ = 0
    for cell in capital_map:
        capital_map[cell] = map_size
        for capital_cell in capital_cells:
            capital_map[cell] = min(capital_map[cell], utils.distance(cell, capital_cell, map_size))
        max_ = max(max_, capital_map[cell])
    len_ = 0
    for cell in capital_map:
        if capital_map[cell] == max_:
            len_ += 1
    rand_cell = random.randrange(0, len_)
    for cell in capital_map.items():
        if cell[1] == max_:
            if rand_cell == 0:
                capital_cells.append(int(cell[0]))
            rand_cell -= 1
for i in range(len(capital_cells)):
    world_map[(capital_cells[i] // map_size) * map_size + (capital_cells[i] % map_size)]['above'] = 'capital'
    world_map[(capital_cells[i] // map_size) * map_size + (capital_cells[i] % map_size)]['tribe'] = tribes[i]

# Expand tribe's territory
done_tiles = []
active_tiles = []
for i in range(len(capital_cells)):
    done_tiles.append(capital_cells[i])
    active_tiles.append([capital_cells[i]])
while len(done_tiles) != map_size ** 2:
    for i in range(len(tribes)):
        if len(active_tiles[i]) and tribes[i] != 'Polaris':
            rand_number = random.randrange(0, len(active_tiles[i]))
            rand_cell = active_tiles[i][rand_number]
            neighbours = utils.circle(rand_cell, 1, map_size)
            valid_neighbours = list(filter(lambda tile: tile not in done_tiles and
                                                   world_map[tile]['type'] != 'water', neighbours))
            if not len(valid_neighbours):
                valid_neighbours = list(filter(lambda tile: tile not in done_tiles, neighbours))
            if len(valid_neighbours):
                new_rand_number = random.randrange(0, len(valid_neighbours))
                new_rand_cell = valid_neighbours[new_rand_number]
                world_map[new_rand_cell]['tribe'] = tribes[i]
                active_tiles[i].append(new_rand_cell)
                done_tiles.append(new_rand_cell)
            else:
                active_tiles[i].remove(rand_cell)

# Assign tile types based on tribe probabilities
for cell in range(map_size**2):
    if world_map[cell]['type'] == 'ground' and world_map[cell]['above'] is None:
        rand = random.random()
        if rand < general_probs['forest'] * terrain_probs['forest'][world_map[cell]['tribe']]:
            world_map[cell]['type'] = 'forest'
        elif rand > 1 - general_probs['mountain'] * terrain_probs['mountain'][world_map[cell]['tribe']]:
            world_map[cell]['type'] = 'mountain'
        rand = random.random()
        if rand < terrain_probs['water'][world_map[cell]['tribe']]:
            world_map[cell]['type'] = 'ocean'

# Generate villages
village_map = []
for cell in range(map_size**2):
    row = cell // map_size
    column = cell % map_size
    if world_map[cell]['type'] == 'ocean' or world_map[cell]['type'] == 'mountain':
        village_map.append(-1)
    elif row == 0 or row == map_size - 1 or column == 0 or column == map_size - 1:
        village_map.append(-1)
    else:
        village_map.append(0)

land_like_terrain = ['ground', 'forest', 'mountain']
for cell in range(map_size**2):
    if world_map[cell]['type'] == 'ocean':
        for neighbour in utils.plus_sign(cell, map_size):
            if world_map[neighbour]['type'] in land_like_terrain:
                world_map[cell]['type'] = 'water'
                break

village_count = 0
for capital in capital_cells:
    village_map[capital] = 3
    for cell in utils.circle(capital, 1, map_size):
        village_map[cell] = max(village_map[cell], 2)
    for cell in utils.circle(capital, 2, map_size):
        village_map[cell] = max(village_map[cell], 1)

while 0 in village_map:
    new_village = random.choice(list(filter(lambda tile: True if village_map[tile] == 0 else False,
                                            list(range(len(village_map))))))
    village_map[new_village] = 3
    for cell in utils.circle(new_village, 1, map_size):
        village_map[cell] = max(village_map[cell], 2)
    for cell in utils.circle(new_village, 2, map_size):
        village_map[cell] = max(village_map[cell], 1)
    village_count += 1

def proc(cell_, probability):
    return (village_map[cell_] == 2 and random.random() < probability) or\
           (village_map[cell_] == 1 and random.random() < probability * BORDER_EXPANSION)

# Add resources to map
for cell in range(map_size**2):
    if world_map[cell]['type'] == 'ground':
        fruit = general_probs['fruit'] * terrain_probs['fruit'][world_map[cell]['tribe']]
        crop = general_probs['crop'] * terrain_probs['crop'][world_map[cell]['tribe']]
        if world_map[cell]['above'] != 'capital':
            if village_map[cell] == 3:
                world_map[cell]['above'] = 'village'
            elif proc(cell, fruit * (1 - crop / 2)):
                world_map[cell]['above'] = 'fruit'
            elif proc(cell, crop * (1 - fruit / 2)):
                world_map[cell]['above'] = 'crop'
    elif world_map[cell]['type'] == 'forest':
        if world_map[cell]['above'] != 'capital':
            if village_map[cell] == 3:
                world_map[cell]['type'] = 'ground'
                world_map[cell]['above'] = 'village'
            elif proc(cell, general_probs['game'] * terrain_probs['game'][world_map[cell]['tribe']]):
                world_map[cell]['above'] = 'game'
    elif world_map[cell]['type'] == 'water':
        if proc(cell, general_probs['fish'] * terrain_probs['fish'][world_map[cell]['tribe']]):
            world_map[cell]['above'] = 'fish'
    elif world_map[cell]['type'] == 'ocean':
        if proc(cell, general_probs['whale'] * terrain_probs['whale'][world_map[cell]['tribe']]):
            world_map[cell]['above'] = 'whale'
    elif world_map[cell]['type'] == 'mountain':
        if proc(cell, general_probs['metal'] * terrain_probs['metal'][world_map[cell]['tribe']]):
            world_map[cell]['above'] = 'metal'

# Add ruins
ruins_number = round(map_size**2/40)
water_ruins_number = round(ruins_number/3)
ruins_count = 0
water_ruins_count = 0
while ruins_count < ruins_number:
    ruin = random.choice(list(filter(lambda tile: True if village_map[tile] in (-1, 0, 1) else False,
                                            list(range(len(village_map))))))
    terrain = world_map[ruin]['type'];
    if terrain != 'water' and (water_ruins_count < water_ruins_number or terrain != 'ocean'):
        world_map[ruin]['above'] = 'ruin'  # actually there can be both ruin and resource on a single tile
        # but only ruin is displayed; as it is just a map generator it doesn't matter
        if terrain == 'ocean':
            water_ruins_count += 1
        for cell in utils.circle(ruin, 1, map_size):
            village_map[cell] = max(village_map[cell], 2)
        ruins_count += 1


def check_resources(resource, capital):
    resources_ = 0
    for neighbour_ in utils.circle(capital, 1, map_size):
        if world_map[neighbour_]['above'] == resource:
            resources_ += 1
    return resources_


def post_generate(resource, underneath, quantity, capital):
    resources_ = check_resources(resource, capital)
    while resources_ < quantity:
        pos_ = random.randrange(0, 8)
        territory_ = utils.circle(capital, 1, map_size)
        world_map[territory_[pos_]]['type'] = underneath
        world_map[territory_[pos_]]['above'] = resource
        for neighbour_ in utils.plus_sign(territory[pos_], map_size):
            if world_map[neighbour_]['type'] == 'ocean':
                world_map[neighbour_]['type'] = 'water'
        resources_ = check_resources(resource, capital)

# Check tribe capitals have correct starting resources
for capital in capital_cells:
    if world_map[capital]['tribe'] == 'Imperius':
        post_generate('fruit', 'ground', 2, capital)
    elif world_map[capital]['tribe'] == 'Bardur':
        post_generate('game', 'forest', 2, capital)
    elif world_map[capital]['tribe'] == 'Kickoo':
        resources = check_resources('fish', capital)
        while resources < 2:
            pos = random.randrange(0, 4)
            territory = utils.plus_sign(capital, map_size)
            world_map[territory[pos]]['type'] = 'water'
            world_map[territory[pos]]['above'] = 'fish'
            for neighbour in utils.plus_sign(territory[pos], map_size):
                if world_map[neighbour]['type'] == 'water':
                    world_map[neighbour]['type'] = 'ocean'
                    for double_neighbour in utils.plus_sign(neighbour, map_size):
                        if world_map[double_neighbour]['type'] != 'water' and world_map[double_neighbour]['type'] != 'ocean':
                            world_map[neighbour]['type'] = 'water'
                            break
            resources = check_resources('fish', capital)
        break
    elif world_map[capital]['tribe'] == 'Zebasi':
        post_generate('crop', 'ground', 1, capital)
    elif world_map[capital]['tribe'] == 'Elyrion':
        post_generate('game', 'forest', 2, capital)
    elif world_map[capital]['tribe'] == 'Polaris':
        for neighbour in utils.circle(capital, 1, map_size):
            world_map[neighbour]['tribe'] = 'Polaris'

# Display options
print(world_map)

# for c in range(map_size ** 2):
#     if c % map_size == 0:
#         print()
#     if world_map[c]['above'] == 'capital':
#         print('0', end='')
#         continue
#     if world_map[c]['above'] == 'village':
#         print('v', end='')
#         continue
#     if world_map[c]['above'] == 'ruin':
#         print('r', end='')
#         continue
#     if world_map[c]['type'] == 'ocean':
#         print('o', end='')
#         continue
#     if world_map[c]['type'] == 'ground':
#         print('g', end='')
#         continue
#     if world_map[c]['type'] == 'forest':
#         print('f', end='')
#         continue
#     if world_map[c]['type'] == 'mountain':
#         print('m', end='')
#         continue
#     if world_map[c]['type'] == 'water':
#         print('w', end='')
#         continue
