from PIL import Image
import json
import requests
from io import BytesIO
import os

def save_image_from_number(no_str):
    try:
        # Send a GET request to the URL
        response = requests.get(f"https://hundeparken.net/h5/game/gfx/item/{no_str}.png")
        
        # Check if the request was successful and return image if yes
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content)).convert("RGBA")
            image.save(f'hats/{no_str}.png')
            print(f"{no_str}.png saved")
    except Exception as e:
        print(e)


with open("hats_info.json", "r", encoding='utf-8') as f:
    hat_dicts = json.load(f)

for hat_dict in hat_dicts:
    if hat_dict['u'] == "11":
        continue

    for no in hat_dict['g'].split(','):
        path = f'hats/{no}.png'
        if os.path.exists(path):
            pass
        else:
            save_image_from_number(no)
    
