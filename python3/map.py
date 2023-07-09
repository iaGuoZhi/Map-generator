import random
import os
import sys
import time

# - Lists of rectangles
SEA_BOX_SHAPES_1 = {
    1:{"x": 8, "y": 15},
    2:{"x": 12, "y": 9},
    3:{"x": 8, "y": 5},
    4:{"x": 10, "y": 13},
    5:{"x": 5, "y": 9},
}

RIVER_BOX_SHAPES_1 = {
    1:{"x": 3, "y": 2},
    2:{"x": 2, "y": 2},
    3:{"x": 4, "y": 2},
    4:{"x": 3, "y": 3},
}

TOWN_BOX_SHAPES_1 = {
    1:{"x": 3, "y": 3},
    2:{"x": 4, "y": 4},
    3:{"x": 2, "y": 2},
    4:{"x": 1, "y": 2},
    5:{"x": 2, "y": 2},
    6:{"x": 1, "y": 2},
}

MOUNTAIN_BOX_SHAPES_1 = {
    1:{"x": 5, "y": 5},
    2:{"x": 4, "y": 7},
    3:{"x": 8, "y": 9},
    4:{"x": 24, "y": 5},
}

MINERAL_BOX_SHAPES_1 = {
    1:{"x": 7, "y": 5},
    2:{"x": 3, "y": 5},
    3:{"x": 9, "y": 8},
    4:{"x": 5, "y": 6},
}

MAP_PARAMS = {
    # Determining the odds of rivers separating
    "river_separate_param" : 30,
    # Determining river number
    "river_number" : 10,
    # Determining river number random factor
    "river_number_random_param" : 3,
    # Determining sea number
    "side_sea_number" : 2,
    # Determining the odds of forest appearing
    "forest_param" : 6,
    # Determining the odds of field appearing
    "field_param" : 3,
    # Determining the scope of detecting town suitability
    "town_scope_param" : 1,
    # Determining the odds of towns building
    "town_build_param" : 666,
    # Determining mountain number
    "mountain_number" : 25,
    # Determining gold number
    "gold_number" : 10,
    # Determining iron number
    "iron_number" : 18,
    # Determining degree of curving
    "curve_corner_param" : 5,
    # Determining default language
    "default_language" : "cn",
}

GLOBAL_MAP_SYMBOLS = {
    "land": "^",
    "field": ".",
    "forest": "*",
    "water": " ",
    "town": "P",
    "gold" : "$",
    "iron" : "&",
    "mountain" : "M",
}

GLOBAL_TOOL_SYMBOLS = {
    "illegal": "?",
}

global global_map_language
global_map_language = MAP_PARAMS["default_language"]

# Function that creates the basic map, defines stuff like size, legend, positions on left/right side, ect
def initialize_map():
    global global_map
    global global_shapes
    global global_height
    global global_width
    global global_map_size
    global global_up_border
    global global_down_border
    global global_left_border
    global global_right_border
    global global_border_group
    global global_border
    global global_input_area_height
    global global_info_bar_width
    global global_name

    global_map = {}
    global_input_area_height = 3
    global_info_bar_width = 25
    size = os.get_terminal_size()
    global_height = size.lines - global_input_area_height
    global_width = size.columns - global_info_bar_width
    global_map_size = global_height * global_width
    for x in range(global_map_size):
        global_map[x] = GLOBAL_MAP_SYMBOLS["land"]
    global_border = [x for x in range(global_map_size) if (x // global_width in (0, global_height - 1)) or (x % global_width == 0) or ((x + 1) % global_width == 0)]
    global_up_border = [x for x in range(global_map_size) if (x // global_width == 0)]
    global_down_border = [x for x in range(global_map_size) if (x // global_width == global_height - 1)]
    global_left_border = [x for x in range(global_map_size) if (x % global_width == 0)]
    global_right_border = [x for x in range(global_map_size) if ((x + 0) % global_width == 0)]
    global_border_group = [global_up_border, global_down_border, global_left_border, global_right_border]
    global_name = random_name()

# Functions that name stuff
def random_name():
    if global_map_language == "cn":
        fp = random.choice(["东","南","西","北", "前", "后"])
        sp = random.choice(["秦","楚","齐","燕", "赵", "魏", "韩", "汉", "吴", "蜀", "越", "宋", "晋", "唐", "明", "元"])
        return (fp + sp).center(16)
    elif global_map_language == "en":
        sp = random.choice(["Torrhen Stark","Ronnel Arryn","Harren Hoare","Loren I Lannister", "Mern IX Gardener", "Argilac Durrandon", "Meria Martell"])
        return sp.center(18)

# Function return symbol meaning according to current language
def get_symbol_meaning():
    if global_map_language == "cn":
        symbol_meaning = [
            "^ = 陆地".ljust(17),
            ". = 耕地".ljust(17),
            "* = 森林".ljust(17),
            "  = 水域".ljust(17),
            "M = 山脉".ljust(17),
            "$ = 金矿".ljust(17),
            "& = 铁矿".ljust(17),
            "P = 城镇".ljust(17),
        ]
    elif global_map_language == "en":
        symbol_meaning = [
            "^ = Land".ljust(19),
            ". = Field".ljust(19),
            "* = Forest".ljust(19),
            "  = Water".ljust(19),
            "M = Mountain".ljust(19),
            "$ = Gold".ljust(19),
            "& = Iron".ljust(19),
            "P = Town".ljust(19),
        ]
    else:
        symbol_meaning = {}

    return symbol_meaning

def get_map_statistics():
    water_area_size = 0
    land_area_size = 0
    population = 0
    gold_reserves = 0
    iron_reserves = 0

    for x in global_map:
        if global_map[x] == GLOBAL_MAP_SYMBOLS["water"]:
            water_area_size += 1
        elif global_map[x] != GLOBAL_MAP_SYMBOLS["water"]:
            land_area_size += 1
            if global_map[x] == GLOBAL_MAP_SYMBOLS["town"]:
                population += 1
            elif global_map[x] == GLOBAL_MAP_SYMBOLS["gold"]:
                gold_reserves += 1
            elif global_map[x] == GLOBAL_MAP_SYMBOLS["iron"]:
                iron_reserves += 1
            else:
                pass
        else:
            pass

    if global_map_language == "cn":
        symbol_meaning = [
            ("陆地面积: %d" % land_area_size).ljust(15),
            ("水域面积: %d" % water_area_size).ljust(15),
            ("人口数量: %d" % population).ljust(15),
            ("金矿储备: %d" % gold_reserves).ljust(15),
            ("铁矿储备: %d" % iron_reserves).ljust(15),
        ]
    elif global_map_language == "en":
        symbol_meaning = [
            ("LAND AREA: %d" % land_area_size).ljust(19),
            ("WATER AREA: %d" % water_area_size).ljust(19),
            ("POPULATION: %d" % population).ljust(19),
            ("GOLD RESERVES: %d" % gold_reserves).ljust(19),
            ("IRON RESERVES: %d" % iron_reserves).ljust(19),
        ]
    else:
        symbol_meaning = []

    return symbol_meaning

# Function that creats the map introduction
def create_intro():
    global global_intro
    global_intro = {
        0: "   +--------------------+",
        1: "   | " + global_name + " |",
        2: "   +--------------------+"
    }
    n = 4
    # Print map statistics
    map_statistics = get_map_statistics()
    for i in map_statistics:
        global_intro[n] = "   | " + i + "|"
        n += 1

    # Print map symbol meaning
    n += 1
    symbol_meaning = get_symbol_meaning()
    for i in symbol_meaning:
        global_intro[n] = "   | " + i + "|"
        n += 1

    global_intro[global_height - 1] = "   +--------------------+"

# Function that places Box on x
def place_box(point, symbol):
    x = 0
    y = 0
    box = []
    while y != global_shapes[global_box]["y"]:
        while x != global_shapes[global_box]["x"]:
            if 0 <= point + y * global_width +x < global_map_size:
                box.append(point + y * global_width + x)
            x += 1
        y += 1
        x = 0
    for x in box:
        if global_map[x] == GLOBAL_MAP_SYMBOLS["land"] or global_map[x] == GLOBAL_MAP_SYMBOLS["field"] or global_map[x] == GLOBAL_MAP_SYMBOLS["forest"]:
            global_map[x] = symbol

def pick_locations(begin, end):
   local_begin_row = begin // global_width
   local_begin_column = begin - local_begin_row * global_width
   local_end_row = end // global_width
   local_end_column = end - local_end_row * global_width

   if min(local_begin_row, local_end_row) + 1 >= max(local_begin_row, local_end_row) and min(local_begin_column, local_end_column) +1 >= max(local_begin_column, local_end_column):
       return
   # Randomly separate rivers
   if random.randint(0, MAP_PARAMS["river_separate_param"]) == 1:
       return

   local_mid_row = random.randint(min(local_begin_row, local_end_row), max(local_begin_row, local_end_row))
   local_mid_column = random.randint(min(local_begin_column, local_end_column), max(local_begin_column, local_end_column))
   local_mid = local_mid_row * global_width + local_mid_column
   if not local_mid in global_points:
       global_points.append(local_mid)
   pick_locations(begin, local_mid)
   pick_locations(local_mid, end)

# Function that design which locations to place box
def design_locations(geo_type):
    global global_points
    global_points = []
    local_i = 0
    if geo_type == "river":
        for local_i in range(MAP_PARAMS["river_number"] + MAP_PARAMS["river_number_random_param"]):
            point_a = random.choice(global_border)
            point_b = random.choice(global_border)
            global_points.append(point_a)
            global_points.append(point_b)
            pick_locations(point_a, point_b)
        return global_points
    elif geo_type == "sea":
        for local_i in range(MAP_PARAMS["side_sea_number"]):
            # Actually, only left and up border and build sea, as box is built towards right and down orientation
            for x in range(4):
                point_a = random.choice(global_border_group[x])
                point_b = random.choice(global_border_group[x])
                global_points.append(point_a)
                global_points.append(point_b)
                pick_locations(point_a, point_b)
        return global_points
    elif geo_type == "forest":
        for local_i in global_map:
            if global_map[local_i] == GLOBAL_MAP_SYMBOLS["land"]:
                if random.randint(0, MAP_PARAMS["forest_param"]) == 1:
                    global_points.append(local_i)
        return global_points
    elif geo_type == "field":
        for local_i in global_map:
            if global_map[local_i] == GLOBAL_MAP_SYMBOLS["land"]:
                if random.randint(0, MAP_PARAMS["field_param"]) == 1:
                    global_points.append(local_i)
        return global_points
    # Town should built near water, mineral
    elif geo_type == "town":
        for local_i in global_map:
            town_suitability = 0
            for y in range(0 - MAP_PARAMS["town_scope_param"], MAP_PARAMS["town_scope_param"] + 1):
                for x in range(0 - MAP_PARAMS["town_scope_param"], MAP_PARAMS["town_scope_param"] + 1):
                    side_point = local_i + y * global_width + x
                    try:
                        side_symbol = global_map[side_point]
                    except:
                        side_symbol = GLOBAL_MAP_SYMBOLS["water"]

                    if side_symbol == GLOBAL_MAP_SYMBOLS["water"]:
                        town_suitability += random.randint(30, 130)
                    elif side_symbol == GLOBAL_MAP_SYMBOLS["gold"]:
                        town_suitability += random.randint(20, 160)
                    elif side_symbol == GLOBAL_MAP_SYMBOLS["iron"]:
                        town_suitability += random.randint(40, 130)
                    elif side_symbol == GLOBAL_MAP_SYMBOLS["mountain"]:
                        town_suitability += random.randint(20, 60)
                    elif side_symbol == GLOBAL_MAP_SYMBOLS["forest"]:
                        town_suitability += random.randint(20, 80)
                    elif side_symbol == GLOBAL_MAP_SYMBOLS["field"]:
                        town_suitability += random.randint(0, 120)
                    else:
                        town_suitability += random.randint(0, 100)

            if town_suitability >= MAP_PARAMS["town_build_param"]:
                global_points.append(local_i)
        return global_points
    elif geo_type == "mountain":
        for local_i in range(MAP_PARAMS["mountain_number"]):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    elif geo_type == "gold":
        for local_i in range(MAP_PARAMS["gold_number"]):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    elif geo_type == "iron":
        for local_i in range(MAP_PARAMS["iron_number"]):
            point_a = random.randint(0, global_map_size - 1)
            global_points.append(point_a)
        return global_points
    else:
        return None

# Function that smooths out long corners
def curve_corners(symbol):
    t = 0
    while t <= MAP_PARAMS["curve_corner_param"]:
        t += 1
        for i in global_map:
            if  global_map[i] == symbol:
                rectangle_sides = 0
                # - U
                x = i - global_width
                try:
                    up_symbol = global_map[x]
                except:
                    up_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if up_symbol != symbol:
                    rectangle_sides += 1
                # - U
                # - D
                x = i + global_width
                try:
                    down_symbol = global_map[x]
                except:
                    down_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if down_symbol != symbol:
                    rectangle_sides += 1
                # - D
                # - L
                if i in global_left_border:
                    pass
                else:
                    x = i - 1
                    try:
                        left_symbol = global_map[x]
                    except:
                        left_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                    if down_symbol != symbol:
                        rectangle_sides += 1
                # - L
                # - R
                if i + 1 in global_right_border:
                    pass
                else:
                    x = i + 1
                    try:
                        right_symbol = global_map[x]
                    except:
                        right_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                    if down_symbol != symbol:
                        rectangle_sides += 1
                # -R
                if rectangle_sides == 4:
                    global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                elif rectangle_sides == 1 and t <= MAP_PARAMS["curve_corner_param"]:
                    if random.randint(0, 50) == 1:
                        global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                elif rectangle_sides == 2 and t <= MAP_PARAMS["curve_corner_param"]:
                    if random.randint(0, 3) != 1:
                        global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                elif rectangle_sides == 3 and t <= MAP_PARAMS["curve_corner_param"]:
                    if random.randint(0, 5) != 1:
                        global_map[i] = GLOBAL_MAP_SYMBOLS["land"]
                else:
                    pass

# Function that replaces the outline of the rectangles with ascii art
def outline_border(symbol):
    for i in global_map:
        if global_map[i] == symbol:
            rectangle_sides = {"U": 0, "D": 0, "L": 0, "R": 0}
            # - U
            x = i - global_width
            try:
                up_symbol = global_map[x]
            except:
                up_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
            if up_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                rectangle_sides["U"] = 1
            # - U
            # - D
            x = i + global_width
            try:
                down_symbol = global_map[x]
            except:
                down_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
            if down_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                rectangle_sides["D"] = 1
            # - D
            # - L
            if i in global_left_border:
                rectangle_sides["L"] = 0
            else:
                x = i - 1
                try:
                    left_symbol = global_map[x]
                except:
                    left_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if left_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                    rectangle_sides["L"] = 1
            # - L
            # - R
            if i + 1 in global_right_border:
                rectangle_sides["R"] = 0
            else:
                x = i + 1
                try:
                    right_symbol = global_map[x]
                except:
                    right_symbol = GLOBAL_TOOL_SYMBOLS["illegal"]
                if right_symbol == GLOBAL_MAP_SYMBOLS["land"]:
                    rectangle_sides["R"] = 1
            # - R
            if rectangle_sides["U"] == 1 and rectangle_sides["D"] == 1 and rectangle_sides["R"] == 1:
                global_map[i] = ">"
            elif rectangle_sides["U"] == 1 and rectangle_sides["D"] == 1 and rectangle_sides["L"] == 1:
                global_map[i] = "<"
            elif rectangle_sides["U"] == 1 and rectangle_sides["R"] == 1 and rectangle_sides["L"] == 1:
                global_map[i] = "^"
            elif rectangle_sides["R"] == 1 and rectangle_sides["D"] == 1 and rectangle_sides["L"] == 1:
                global_map[i] = "v"
            elif (rectangle_sides["U"] == 1 and rectangle_sides["L"] == 1) or (rectangle_sides["D"] == 1 and rectangle_sides["R"] == 1):
                global_map[i] = "/"
            elif (rectangle_sides["U"] == 1 and rectangle_sides["R"] == 1) or (rectangle_sides["D"] == 1 and rectangle_sides["L"] == 1):
                global_map[i] = u"\u005C"
            elif rectangle_sides["U"] == 1:
                global_map[i] = u"\u203E"
            elif rectangle_sides["D"] == 1:
                global_map[i] = "_"
            elif rectangle_sides["L"] == 1 or rectangle_sides["R"] == 1:
                global_map[i] = "|"
            else:
                pass

def build_water():
    build_sea()
    build_river()
    outline_border(GLOBAL_MAP_SYMBOLS["water"])

def build_river():
    global global_box
    global global_shapes
    global_shapes = RIVER_BOX_SHAPES_1
    points = design_locations("river")
    points.sort()
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["water"])

def build_sea():
    global global_box
    global global_shapes
    global_shapes = SEA_BOX_SHAPES_1
    points = design_locations("sea")
    points.sort()
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["water"])

def build_forest():
    global global_box
    points = design_locations("forest")
    for x in points:
        global_map[x] = GLOBAL_MAP_SYMBOLS["forest"]

def build_field():
    global global_box
    points = design_locations("field")
    for x in points:
        global_map[x] = GLOBAL_MAP_SYMBOLS["field"]

def build_towns():
    global global_box
    global global_shapes
    global_shapes = TOWN_BOX_SHAPES_1
    points = design_locations("town")
    points.sort()
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["town"])

def build_mountains():
    global global_box
    global global_shapes
    global_shapes = MOUNTAIN_BOX_SHAPES_1
    points = design_locations("mountain")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["mountain"])
    curve_corners(GLOBAL_MAP_SYMBOLS["mountain"])

def build_mineral():
    global global_box
    global global_shapes
    global_shapes = MINERAL_BOX_SHAPES_1
    points = design_locations("gold")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["gold"])
    curve_corners(GLOBAL_MAP_SYMBOLS["gold"])
    points = design_locations("iron")
    for x in points:
        global_box = random.choice(list(global_shapes.keys()))
        place_box(x, GLOBAL_MAP_SYMBOLS["iron"])
    curve_corners(GLOBAL_MAP_SYMBOLS["iron"])

def user_input():
    global global_map_language
    print("Regenerate(1) Set map language(2)")
    cmd = input(">")
    while cmd != "1":
        if cmd == "2":
            print("Input language: Chinese(cn), English(en)")
            language = input(">")
            print(language)
            if language == "cn":
                global_map_language = "cn"
            elif language == "en":
                global_map_language = "en"
            else:
                pass

        print("Regenerate(1) Set map language(2)")
        cmd = input(">")

# Function that prints the map to the console
def print_map():
    c = 0
    x = 0
    i = 0
    for i in range(global_height):
        for x in range(global_width):
            print(global_map[c], end = "")
            x += 1
            c += 1
        try:
            print(global_intro[i])
        except:
            print("   |                    |")
        x = 1
        i += 1

def save_map_to_file():
    timestamp = time.strftime("%Y-%m-%dT%H:%M%SZ")
    file_name = "output/" + global_name.strip() + "_" + timestamp + ".txt"
    original_stdout = sys.stdout
    with open(file_name, 'w') as output_file:
        sys.stdout = output_file
        print_map()
        sys.stdout = original_stdout

# Main loop
while True:
    user_input()
    initialize_map()
    build_water()
    build_mountains()
    build_mineral()
    build_forest()
    build_field()
    build_towns()
    create_intro()
    print_map()
    save_map_to_file()
    print("")
