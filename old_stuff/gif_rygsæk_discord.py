from PIL import Image, ImageDraw
import random
import json
import requests
from math import cos, sin, pi
import re

class mover:

    def __init__(self, box, file=None, url=None, position=None, velocity=None, gravity=True):
        
        # Settings
        self.gravity = gravity

        # Borders
        self.box_x1, self.box_y1, self.box_x2, self.box_y2 = box

        # The image, see if you have file path or url
        if file:
            self.object = Image.open(file).convert("RGBA")

        elif url:
            data = requests.get(url).content
            with open('img.png','wb') as f:
                f.write(data) 

            self.object = Image.open('img.png').convert("RGBA")

        else:
            raise Exception("No image found")
        
        self.size_x, self.size_y = self.object.size

        # Positions
        if position:
            self.y, self.y = position
        else:
            self.x = random.randint(self.box_x1, self.box_x2-self.size_x)
            self.y = random.randint(self.box_y1, self.box_y2-self.size_y)

        # Velocity
        if velocity:
            self.dx, self.dy = velocity
        else:
            if self.gravity:
                self.dx, self.dy = random.randint(-20,20), random.randint(-12,12)
            else:
                self.dx, self.dy = cos(random.uniform(0, 2*pi))*4, sin(random.uniform(0, 2*pi))*4
        
    def move(self):

        # Acceleration
        if self.gravity:
            self.dy += 0.175

        # Dampers
        if self.gravity:
            damp = 0.9
            damp_x = 0.97
        else:
            damp = 1
            damp_x = 1

        # Velocity (update position)
        self.x += self.dx
        self.y += self.dy

        # Walls:
        # Left
        if self.x <= self.box_x1:
            self.dx = -self.dx*damp

            self.x = self.box_x1

        # Right
        if self.x + self.size_x >= self.box_x2:
            self.dx = -self.dx*damp

            self.x = self.box_x2 - self.size_x

        # Bottom
        if self.y + self.size_y >= self.box_y2:
            self.dy = -self.dy*damp

            if self.gravity:
                self.dx = self.dx*damp_x # Damp x-speed as well

            self.y = self.box_y2 - self.size_y

        # Top
        if self.y <= self.box_y1:
            self.dy = -self.dy*damp

            self.y = self.box_y1            
    
    def coor(self):
        return round(self.x), round(self.y)
    
    def size(self):
        return self.size_x, self.size_y

    def img(self):
        return self.object

with open("hats.json", "r") as f:
    hat_list = json.load(f)

# Background image
canvas = Image.open("rygsækønsker.png").convert("RGBA")
cx, cy = canvas.size

# Settings
numbering = False

# Settings
total_frames = 1000

# The boxes
box1 = (8, 34, 375+8, 107+34)
box2 = (8, 185, 375+8, 105+185)

def bag_maker(input_string):

    # Get contents of parentheses
    contents = re.findall(r'\[(.*?)\]', input_string)

    # Check if you have the right number of boxes!
    if len(contents) not in [2, 3]:
        return """Something went wrong, try again. Your commando should look like:
        `bag_maker[names of hats in your bag separated by commas][names of hats you want][write "gravity" here if you want gravity. Omit the last parenthesis otherwise]`
        For example: `bag_maker[bulldog, bulldog, bulldog, bulldog][guld stjerne, glasstjerne][gravity]`.
        Note, you can abbreviate the hat names. The first valid one will just be found instead
        For example: `bag_maker[bull, bull, bull, bull][guld stjerne, glasst][gravity]`
        """, False

    # Get things from the parentheses
    names1, names2, *settings = contents
    names1 = names1.split(',')
    names2 = names2.split(',')

    # The objects
    objects = []
    frames = []
    not_found = []

    if "gravity" in str(settings):
        gravity = True
    else:
        gravity = False

    # Make the objects
    def object_adder(names, box, gravity):

        for object in names:

            # Find the correct image
            for key, item in hat_list.items():

                # Clean the string so you can search
                object_cleaned = object.replace(" ", "").lower()
                if object_cleaned in key:
                    objects.append(mover(box, url=item, gravity=gravity))
                    break
            else:
                not_found.append(object)
            
    # Assign the boxes
    object_adder(names1, box1, gravity)
    object_adder(names2, box2, gravity)

    # Make frames
    for t in range(total_frames):

        # Background
        final = Image.new("RGBA", canvas.size)
        final.paste(canvas, (0,0), canvas)

        # The objects
        for object in objects:
            final.paste(object.img(), object.coor(), object.img())
            object.move()

        # If you want the numbers
        if numbering:
            I1 = ImageDraw.Draw(final)
            I1.text((cx/2, cy/4), f"{t+1}/{total_frames}", fill=(0, 0, 0))

        # Add to frames
        frames.append(final)
        
    # Save image
    frame_one = frames[0]
    frame_one.save("HP_bytte_image.gif",
                format="GIF",
                append_images=frames,
                save_all=True,
                duration=50,
                loop=0)
    
    length = len(not_found)

    if length == 1:
        return f"The following thing was not found: {not_found[0]}", True
    elif length > 1:
        return f"The following things were not found: {', '.join(not_found)}", True
    else:
        return "Here is your GIF, enjoy ^^", True
