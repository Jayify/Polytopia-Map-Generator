
let page = 'main';

let map_size = 16;

let tribes = ['Xin-Xi', 'Imperius', 'Bardur', 'Oumaji', 'Kickoo', 'Hoodrick', 'Luxidoor', 'Vengir', 'Zebasi',
    'Ai-Mo', 'Quetzali', 'Yadakk', 'Aquarion', 'Elyrion', 'Polaris'];
let terrain = ['forest', 'fruit', 'game', 'ground', 'mountain'];
let general_terrain = ['ocean', 'water'];

let assets = [];
for (let tribe of tribes) {
    assets[tribe] = [];
}
for (let g_t of general_terrain) {
    assets[g_t] = get_image("assets/" + g_t + ".png");
}
for (let tribe of tribes) {
    for (let terr of terrain) {
        assets[tribe][terr] = get_image("assets/Tribes/" + tribe + "/" + tribe + " " + terr + ".png");
    }
}

let imperius_capital = new Image();
imperius_capital.src = "assets/tribes/imperius_capital.png";

function switch_page(new_page) {
    document.getElementById("main").style.display='none';
    document.getElementById("faq").style.display='none';
    page = new_page;
    document.getElementById(new_page).style.display='block';
}

function get_image(src) {
    let image = new Image();
    image.src = src;
    return image;
}

function generate() {
    map_size = parseInt(document.getElementById("map_size").value);
    if (map_size < 5 || map_size !== Math.floor(map_size)) {
        document.getElementById("warning").innerText = 'Warning: Map size must be integer at least 5.';
        document.getElementById("warning").style.display='block';
        return;
    }

    let initial_land = parseFloat(document.getElementById("initial_land").value);
    if (initial_land < 0 || initial_land > 1) {
        document.getElementById("warning").innerText = 'Warning: Initial land must be float between 0 and 1.';
        document.getElementById("warning").style.display='block';
        return;
    }
    let smoothing = parseInt(document.getElementById("smoothing").value);
    if (smoothing < 0 || smoothing !== Math.floor(smoothing)) {
        document.getElementById("warning").innerText = 'Warning: Smoothing must be integer at least 0.';
        document.getElementById("warning").style.display='block';
        return;
    }
    let relief = parseInt(document.getElementById("relief").value);
    if (relief < 1 || relief > 8 || relief !== Math.floor(relief)) {
        document.getElementById("warning").innerText = 'Warning: Relief must be integer between 1 and 8.';
        document.getElementById("warning").style.display='block';
        return;
    }
    let land_coefficient = (0.5 + relief) / 9;
    let map = new Array(map_size);

    for (let i = 0; i < map_size; i++) {
        map[i] = new Array(map_size);
        for (let j = 0; j < map_size; j++)
            map[i][j] = {type: 'ocean', above: null, road: false, tribe: 'Xin-Xi'}
    }

    let i = 0;
    while (i < map_size**2 * initial_land) {
        let row = random_int(0, map_size - 1);
        let column = random_int(0, map_size - 1);
        if (map[row][column]['type'] === 'ocean') {
            i++;
            map[row][column]['type'] = 'ground';
        }
    }

    for (let i = 0; i < smoothing; i++) {
        for (let row = 0; row < map_size; row++) {
            for (let column = 0; column < map_size; column++) {
                let water_count = 0;
                let tile_count = 0;
                if (column > 0) {
                    if (row > 0) {
                        if (map[row - 1][column - 1]['type'] === 'ocean')
                            water_count++;
                        tile_count++;
                    }
                    if (row < map_size - 1) {
                        if (map[row + 1][column - 1]['type'] === 'ocean')
                            water_count++;
                        tile_count++;
                    }
                    if (map[row][column - 1]['type'] === 'ocean')
                        water_count++;
                    tile_count++;
                }
                if (column < map_size - 1) {
                    if (row > 0) {
                        if (map[row - 1][column + 1]['type'] === 'ocean')
                            water_count++;
                        tile_count++;
                    }
                    if (row < map_size - 1) {
                        if (map[row + 1][column + 1]['type'] === 'ocean')
                            water_count++;
                        tile_count++;
                    }
                    if (map[row][column + 1]['type'] === 'ocean')
                        water_count++;
                    tile_count++;
                }
                if (row > 0) {
                    if (map[row - 1][column]['type'] === 'ocean')
                        water_count++;
                    tile_count++;
                }
                if (row < map_size - 1) {
                    if (map[row + 1][column]['type'] === 'ocean')
                        water_count++;
                    tile_count++;
                }
                if (map[row][column]['type'] === 'ocean')
                    water_count++;
                tile_count++;

                if (water_count / tile_count < land_coefficient)
                    map[row][column]['road'] = true;
            }
        }
        for (let row = 0; row < map_size; row++) {
            for (let column = 0; column < map_size; column++) {
                if (map[row][column]['road'] === true) {
                    map[row][column]['road'] = false;
                    map[row][column]['type'] = 'ground';
                } else {
                    map[row][column]['type'] = 'ocean';
                }
            }
        }
    }

    for (let row = 0; row < map_size; row++) {
        for (let column = 0; column < map_size; column++) {
            if (map[row][column]['type'] === 'ocean') {
                if (column > 0) {
                    if (map[row][column - 1]['type'] === 'ground') {
                        map[row][column]['type'] = 'water';
                        continue;
                    }
                }
                if (column < map_size - 1) {
                    if (map[row][column + 1]['type'] === 'ground') {
                        map[row][column]['type'] = 'water';
                        continue;
                    }
                }
                if (row > 0) {
                    if (map[row - 1][column]['type'] === 'ground') {
                        map[row][column]['type'] = 'water';
                        continue;
                    }
                }
                if (row < map_size - 1) {
                    if (map[row + 1][column]['type'] === 'ground') {
                        map[row][column]['type'] = 'water';
                    }
                }
            }
        }
    }



    display_map(map);

    let text_output_check = document.getElementById("text_output_check").checked;
    if (text_output_check)
        print_map(map);
    else
        document.getElementById("text_display").style.display='none';
}

function print_map(map) {
    let seen_grid = Array(map_size**2 * 4);
    for (let i = 0; i < map_size**2 * 4; i++) {
        seen_grid[i] = '-';
    }
    for (let i = 0; i < map_size**2; i++) {
        let row = Math.floor(i / map_size);
        let column = i % map_size;
        seen_grid[map_size - 1 + column - row + (column + row) * map_size * 2] = map[row][column]['type'][0];
    }
    let output = '';
    for (let i = 0; i < map_size * 2; i++) {
        output += seen_grid.slice(i * map_size * 2, (i + 1) * map_size * 2).join('');
        output += '\n'
    }

    document.getElementById("text_display").innerText = output;
    document.getElementById("text_display").style.display='block';
}

function display_map(map) {
    let graphic_display = document.getElementById("graphic_display");
    graphic_display.width = graphic_display.width;
    let canvas = graphic_display.getContext("2d");

    let tile_width = 1000 / map_size;
    let tile_height = 604 / map_size;

    for (let i = 0; i < map_size**2; i++) {
        let row = Math.floor(i / map_size);
        let column = i % map_size;
        let x = 500 - tile_width / 2 + (column - row) * tile_width / 2;
        let y = (column + row) * tile_height / 1908 * 606;
        let type = map[row][column]['type'];
        let tribe = map[row][column]['tribe'];
        if (general_terrain.includes(type)) {
            canvas.drawImage(assets[type], x, y, tile_width, tile_height);
        } else if (tribe) {
            canvas.drawImage(assets[tribe][type], x, y, tile_width, tile_height);
        }
    }
}

function random_int(min, max) {
    let rand = min + Math.random() * (max + 1 - min);
    return Math.floor(rand);
}

function toggle_tribe(tribe_check, tribe) {
    if (document.getElementById(tribe_check).checked)
        document.getElementById(tribe).style.display='block';
    else
        document.getElementById(tribe).style.display='none';
}