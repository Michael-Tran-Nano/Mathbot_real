from PIL import Image
import numpy as np
import json
import requests
from io import BytesIO
import pandas as pd
from hat_image_maker import make_hat_image, update_hat_dict

def identify_hat(hat_info_string):
    instructions = string_to_instructions(hat_info_string)

    if 'place' not in instructions or 'name' not in instructions:
        raise KeyError("specify the place and the name of the of hat") # attach image

    hat_name = instructions['name']
    if len(hat_name) < 3:
        raise KeyError('Please give a longer name. Have a length of at least 3')
    place = instructions['place']

    possible_hats =  get_possible_hats(hat_name)
    if len(possible_hats) == 0:
        raise KeyError('I could not find any possible hats with the name you gave. I do not have hat-information from after 22-07-24. Ask Kartoffel to update it')

    haystack = Image.open('haystack.png').convert("RGBA")
    r1, r2 = find_ref_in_image(haystack)

    for possible_hat in possible_hats:
        real_hat_name, url = possible_hat
        hat_image = get_image_from_url(url)
        result = find_needle_coors(hat_image, haystack, tolerance=0.9, ref_coor=(r1, r2))
        if result:
            x, y = result
            image_no = url.split("item/")[1].replace('.png', '')
            id = add_to_excel(real_hat_name, x, y, place, image_no)
            # add changes to the image with all hats.
            update_hat_dict()
            hat_image.save(f'hatgiver/hats/{image_no}.png')
            hat_image.close()
            haystack.close()
            make_hat_image(f"type:dog,{place}:{id}")
            return f"Image added with the name: {real_hat_name}, and id: {id}"
        hat_image.close()

    haystack.close()
    raise KeyError('I could not find any possible hats with the name you gave. I do not have hat-information from after 22-07-24. Ask Kartoffel to update it')

def string_to_instructions(hat_info_string): # maybe share with the other one
    components = hat_info_string.split(',')
    instructions = {} # color, type of animal, head, mouth, belly, make possible to save color

    for component in components:
        key, val = component.split(':') # find out what to do with faulty data
        key, val = key.strip(), val.strip()

        instructions[key] = val # It will be automatically be lower at a later time

    return instructions


with open("hatgiver/hats.json", "r") as f:
    hat_list = json.load(f)
def get_possible_hats(hat_name):
    return [(hat, url) for hat, url in hat_list.items() if hat_name.lower() in hat.lower()]


def find_ref_in_image(haystack):
    needle = Image.open('hatgiver/ref.png').convert("RGBA")
    r1, r2 = find_needle_coors(needle, haystack)
    needle.close()
    return (r1, r2)

def find_needle_coors(needle, haystack, tolerance=1, ref_coor=None):
    # Convert images to numpy arrays
    small_array = np.fliplr(np.array(needle)) if ref_coor else np.array(needle)
    large_array = np.array(haystack)

    # Get dimensions
    small_h, small_w, _ = small_array.shape
    large_h, large_w, _ = large_array.shape

    # Get target
    target = 0
    for j in range(small_h): #Maybe make shorter
        for i in range(small_w):
            small_pixel = small_array[j, i]
            if small_pixel[3] == 255:
                target += 1
    max_wrong = target * (1 - tolerance)

    x_max = min(ref_coor[0] + 100, large_w)  if ref_coor else large_w
    y_max = ref_coor[1] if ref_coor else large_h 

    # Iterate over each possible position
    for y in range(y_max - small_h + 1):
        for x in range(x_max - small_w + 1):
            result = sub_search(x, y, small_array, large_array, small_h, small_w, max_wrong, tolerance)

            if result and ref_coor:
                x1, x2 = result
                r1, r2 = ref_coor
                return x1 - r1, x2 - r2
            elif result:
                return result
    
    if ref_coor is None:
        raise KeyError('Reference could not be found. Did you remember to add it?') # Maybe give its own Exp and helping image

    return None


def sub_search(x, y, small_array, large_array, small_h, small_w, max_wrong, tolerance):
    match_count = 0
    compare_count = 0
    for j in range(small_h):
        for i in range(small_w):
            # Get the RGBA values of the current pixel in both images
            small_pixel = small_array[j, i]
            large_pixel = large_array[y + j, x + i]

            if small_pixel[3] == 255:  # Skip transparent
                compare_count += 1
                if np.array_equal(small_pixel, large_pixel):
                    match_count += 1
            
            if compare_count - match_count > max_wrong:
                return None

    # Check if the match count meets the tolerance threshold
    if compare_count > 0 and match_count / compare_count >= tolerance:
        return (x, y)
    
    return None


def get_image_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful and return image if yes
        if response.status_code == 200:
            return Image.open(BytesIO(response.content)).convert("RGBA")
        else:
            raise KeyError("I do not have access to the hat database right now. Try again later")
    except Exception as e:
        raise KeyError("I do not have access to the hat database right now. Try again later")


def add_to_excel(name, x, y, place, image_no):
    
    # Load the uploaded Excel file
    file_path = 'hatgiver/hats.xlsx'
    df = pd.read_excel(file_path, sheet_name='Ark1')

    image_no = int(image_no)
    id = len(df) + 1
    if image_no in list(df['image no']):
        raise KeyError(f'It seems like "{name}" has already been added. You cannot add it again!')

    # Define the new row data as a dictionary
    new_row = {
        'name': name,
        'x': x,
        'y': y,
        'place': place,
        'image no': image_no,
        'order no': id 
    }

    # Convert the new row data into a DataFrame
    new_row_df = pd.DataFrame([new_row])

    # Concatenate the new row DataFrame with the original DataFrame
    df = pd.concat([df, new_row_df], ignore_index=True)

    # Save the updated DataFrame back to the Excel file
    df.to_excel(file_path, sheet_name='Ark1', index=False)

    return id
