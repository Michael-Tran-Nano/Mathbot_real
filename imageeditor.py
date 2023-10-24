from PIL import Image
import random

# Positions of the tiles
positions = [(38, 271), (99, 271), (160, 271), (38, 332), (99, 332), (160, 332), (38, 393), (99, 393), (160, 393)]

def maker(numbers: str, randomplate=False, name='Null'):

    if randomplate == False:
        numbers = numbers.split()
        if len(set(numbers)) != 9:
            return "I could not find 9 unique numbers. Try again. For example: `bingo 1 2 3 4 5 6 7 8 9`. The valid numbers are in the range 1-42", False
        
        # Make to integers
        numbers = [int(x) for x in numbers]
    
    if randomplate:
        numbers = random.sample(range(1, 42), 9)

    canvas = Image.open("bingo/autumn_bingo_plate.png").convert("RGB")
    
    for i, pos in enumerate(positions):
        try:
            x, y = pos
            tile = Image.open(f"bingo/{numbers[i]}.png")
            canvas.paste(tile, (x, y))
        except FileNotFoundError:
            return f"I could not find hat number {numbers[i]}. Are you sure that is valid? The valid numbers are in the range 1-42", False
        
    tile.close()
    canvas.save('bingoplate.png')

    # Make a log
    with open("bingolog.txt", "a") as f:
        f.write(f"{name},{numbers},{randomplate}\n")

    return "Here is your bingo plate, enjoy!", True


  

