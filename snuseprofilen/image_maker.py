from PIL import Image
import json
from functools import reduce
from math import ceil

update_date = "27-07-24"

with open("snuseprofilen/hat_data.json", "r", encoding='utf-8') as f:
    hat_dict = json.load(f)

# For animal types and their specifuc coordinates
animals = {'dog', 'cat', 'bear', 'wolf'}
base_coor_dict =  {'dog':(160-19, 80-9), 'wolf':(160-21, 80-14), 'cat':(160-15, 80-11), 'bear':(160-23, 80-10)}
head_coor_dict =  {'dog': (11, 1), 'wolf': (12, 5), 'cat': (8, 6), 'bear': (13, 1)}
mouth_coor_dict = {'dog': (3, 5), 'wolf': (3, 11), 'cat': (2, 12), 'bear': (2, 10)}
belly_coor_dict = {'dog':(23, 4), 'wolf':(25, 10), 'cat':(19, 9), 'bear':(27, 2)}
dildo_coor_dict = {'dog':(23+17, 4+11), 'wolf':(25+16-1, 10+16), 'cat':(19+13-1, 9+9), 'bear':(27+21-1, 2+14)}
body_coor_dicts = {'head': head_coor_dict, 'mouth': mouth_coor_dict, 'belly': belly_coor_dict, 'dildo': dildo_coor_dict}
number_to_placement = {'1': 'head', '2': 'mouth', '12': 'dildo'}

possible_instruction_types = {'head', 'belly', 'mouth', 'animal', 'color', 'dildo'}
placements = ['dildo', 'head', 'mouth', 'belly']

standard_colors = {
    'red' : "#FF0000",
    'blue' : "#0000FF",
    'green' : "#00FF00",
    'white' : "#000000",
    'black' : "#404B50",
    'orange': "#FFA500",
    'purple': "#A020F0",
    'pink' : "#FF00FF",
    'yellow' : "#FFFF00",
    'brown' : "#7F3300",
    'gray': "#C0C0C0"
}

def make_hat_image(dress_string):
    gif = False
    messages = []
    instructions = [ins.strip() for ins in dress_string.split(',')]
    commands = {}

    for instruction in instructions:
        # Settings
        if instruction in animals:
            commands['animal'] = instruction
            continue
        elif instruction.startswith('#'):
            commands['color'] = instruction
            continue
        elif instruction in standard_colors:
            commands['color'] = standard_colors[instruction]
            continue
        elif instruction == 'gif':
            gif = True
            continue

        # Hats
        hat_info = instruction_to_hatinfo(instruction, messages)
        if hat_info is None:
            continue

        if hat_info['u'] == '1':
            placement = 'head'
        elif hat_info['u'] == '2':
            placement = 'mouth'
        elif hat_info['u'] == '11':
            messages.append(f'{instruction} is ignored because it is an object, and you cannot wear an object.')
            continue
        elif hat_info['u'] == '12':
            placement = 'dildo'
        else:
            placement = 'belly'
        
        if placement in commands:
            messages.append(f'"{instruction}" is ignored because it is in the {placement} position, but another hat is already placed there.')
        else:
            commands[placement] = hat_info

    if 'animal' not in commands:
        commands['animal'] = 'dog'

    if gif:
        make_gif_from_command(commands, messages)
    else:
        make_png_from_command(commands, messages)

    return messages, gif


def instruction_to_hatinfo(instruction, messages):
    if instruction in hat_dict:
        return hat_dict[instruction]

    # Find approximate
    for hat_dict_name in hat_dict.keys():
        if instruction in hat_dict_name:
            messages.append(f'The hat "{instruction}" was not found as a hat, "{hat_dict_name}" was used instead.')
            return hat_dict[hat_dict_name]

    messages.append(f'"{instruction}" was not found. Did you make a typo? It could also be a new hat that has not been added yet. Last update is from {update_date}. You can also write `!help` if you want to find the instructions.')
    return None

def make_png_from_command(commands, messages):
    animal = commands['animal']
    canvas = get_basic_animal_canvas(commands, messages)

    for placement in placements:
        if placement in commands:
            hat_info = commands[placement]
            hat_placer(animal, hat_info, canvas)

    canvas.save(f'snuseprofil.png')
    canvas.close()


def make_gif_from_command(commands, messages):
    animal = commands['animal']
    canvas = get_basic_animal_canvas(commands, messages)

    animations = {}
    for placement in placements: 
        if placement in commands:
            hat_info = commands[placement]
            if hat_info['a'] != 0:
                animations[placement] = {'rate': hat_info['a'], 'frame_count': len(hat_info['g'].split(','))}

    if len(animations) == 0:
        duration = 1
        frame_count = 1
    elif len(animations) == 1:
        ani_dict = next(iter(animations.values()))
        duration = get_duration(ani_dict['rate'])
        frame_count = ani_dict['frame_count']
    else:
        durations = [get_duration(ani_dict['rate']) for ani_dict in animations.values()]
        frame_counts = [ani_dict['frame_count'] for ani_dict in animations.values()]
        duration = int(sum(durations) / len(durations))
        messages.append("WARNING: More than 1 hat with animation used. The average framerate of each animated hat is used. This may give some unnatural animation speed for the hats.")
        
        # Making sure that animation cycles matches up
        frame_count_max = max(frame_counts)
        if all(frame_count_max % x == 0 for x in frame_counts):
            frame_count = frame_count_max
        else:
            frame_count = reduce(lambda x, y: x * y, frame_counts)

    frames = []
    for i in range(frame_count):
        canvas_frame = canvas.copy()
        for placement in placements:
            if placement in commands:
                hat_info = commands[placement]
                hat_placer(animal, hat_info, canvas_frame, frame_no=i)
        frames.append(canvas_frame)
    frame_one = frames[0]
    frame_one.save(f'snuseprofil.gif', format="GIF", append_images=frames,
                   save_all=True, duration=duration, loop=0)
    
    canvas.close()
    for frame in frames:
        frame.close()


def get_duration(rate):
    return 10000/rate - rate 


def get_basic_animal_canvas(commands, messages):
    canvas = Image.open(f"snuseprofilen/base.png").convert("RGBA")
    animal = commands['animal']
    animal_img = Image.open(f"snuseprofilen/{animal}.png").convert("RGBA")
    if 'color' in commands:
        rgb_color = hex_to_rgb(commands['color'], messages)
        recolor_animal(rgb_color, animal_img)

    x, y = base_coor_dict[animal]
    canvas.paste(animal_img, (x, y), animal_img)
    animal_img.close()
    return canvas


def recolor_animal(rgb_color, animal_img):

    img_data = animal_img.getdata()

    fur_color = (*rgb_color, 255)
    shadow_color = (*[ceil(x * 0.7) - 1 for x in rgb_color], 255)

    new_data = []
    for pixel in img_data:
        if pixel == (255, 255, 255, 255):
            new_data.append(fur_color)
        elif pixel == (178, 178, 178, 255):
            new_data.append(shadow_color)
        else:
            new_data.append(pixel)
    
    animal_img.putdata(new_data)


def hex_to_rgb(hex_color, messages):
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    
    try:
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)
    except Exception:
        messages.append(f"I could not convert #{hex_color} into a color. Did you type it correctly?")
        return (255, 255, 255)
    
    return (red, green, blue)


def hat_placer(animal, hat_info, canvas,frame_no=0):
    placement = number_to_placement.get(hat_info['u'], 'belly')
    frames = hat_info['g'].split(',')
    img_no = frames[frame_no % len(frames)]
    base_x, base_y = base_coor_dict[animal]
    place_x, place_y = body_coor_dicts[placement][animal]
    hat_x, hat_y = hat_info['x'], hat_info['y']

    hat = Image.open(f"snuseprofilen/hats/{img_no}.png").convert("RGBA")
    if placement == 'dildo':
        crop_dildo(hat)
    x, y = base_x + place_x + hat_x, base_y + place_y + hat_y
    canvas.paste(hat, (x, y), hat)
    hat.close()


def crop_dildo(dildo):
    width, height = dildo.size
    pixels = dildo.load()
    left_side_width = width // 2

    for x in range(left_side_width):
        for y in range(height):
            pixels[x, y] = (0, 0, 0, 0)