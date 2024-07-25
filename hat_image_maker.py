import pandas as pd
from PIL import Image

# Dictionary for hats
file_path = 'hatgiver/hats.xlsx'
df = pd.read_excel(file_path)
hat_dicts = {}
order_no_to_hat_name = {}
for _, row in df.iterrows():
    hat_dicts[row['name'].lower()] = row.drop('name').to_dict()
    order_no_to_hat_name[row['order no']] = row['name'].lower()

# For animal types and their specifuc coordinates
head_coor_dict = {'dog':(155, 102), 'wolf':(148, 98), 'cat':(154, 105), 'bear':(153, 105)}
mouth_coor_dict = {'dog':(155, 102), 'wolf':(148, 100), 'cat':(151, 107), 'bear':(155, 108)}
belly_coor_dict = {'dog':(155, 102), 'wolf':(146, 100), 'cat':(154, 105), 'bear':(150, 101)}
body_coor_dicts = {'head': head_coor_dict, 'mouth': mouth_coor_dict, 'belly': belly_coor_dict}

def make_hat_image(dress_string): # add warnings
    instructions = string_to_instructions(dress_string)

    if 'type' in instructions and instructions['type'] in ['dog', 'cat', 'bear', 'wolf']:
        animal_type = instructions['type']
    else:
        animal_type = 'dog'

    canvas = Image.open(f"hatgiver/base_{animal_type}.png").convert("RGB")
    
    for body_part in ['head', 'mouth', 'belly']:
        if body_part in instructions:
            hat_name = instructions[body_part]

            # if order no is used
            if hat_name.isdigit() and int(hat_name) in order_no_to_hat_name:
                hat_name = order_no_to_hat_name[int(hat_name)]

            if hat_name in hat_dicts:
                hat_dict = hat_dicts[hat_name]
                x, y = hat_dict['x'], hat_dict['y']
                hat_type = hat_dict['place']
                img_no = hat_dict['image no']
                hat_placer(animal_type, img_no, hat_type, (x, y), canvas)
                # give an error for a wrong hat to a wrong type, or I don't care?
            else:
                raise KeyError(f'"{hat_name}" was not found in the list of hats. It has not yet been added, or you made a typo')

    canvas.save(f'ready_animal_with_hat.png')
    canvas.close()


abbrevs = {'h': 'head', 'm': 'mouth', 'b': 'belly', 'c': 'color', 't': 'type'}
def string_to_instructions(dress_string):
    components = dress_string.split(',')
    instructions = {} # color, type of animal, head, mouth, belly, make possible to save color

    for component in components:
        key, val = component.split(':') # find out what to do with faulty data
        key, val = key.strip(), val.strip()
        if key in abbrevs:
            key = abbrevs[key]

        # make a check that everything is a valid order, or not.
        instructions[key] = val

    return instructions


def hat_placer(animal_type, img_no, hat_type, hat_coor, canvas):
    x1, y1 = hat_coor
    hat = Image.open(f"hatgiver/hats/{img_no}.png").convert("RGBA").transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    x2, y2 = body_coor_dicts[hat_type][animal_type]
    canvas.paste(hat, (x1 + x2, y1 + y2), hat)
    hat.close()

def update_hat_dict():
    file_path = 'hatgiver/hats.xlsx'
    df = pd.read_excel(file_path)
    global hat_dicts
    global order_no_to_hat_name
    hat_dicts = {}
    order_no_to_hat_name = {}
    for _, row in df.iterrows():
        hat_dicts[row['name'].lower()] = row.drop('name').to_dict()
        order_no_to_hat_name[row['order no']] = row['name'].lower()


