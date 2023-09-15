from PIL import Image # Make it possible to extract statistics
import random

positions = [(38, 271), (99, 271), (160, 271), (38, 332), (99, 332), (160, 332), (38, 393), (99, 393), (160, 393)]

def maker(numbers, randomplate=False): #get a string with numbers

    if randomplate == False:
        numbers = numbers.split()
        if len(set(numbers)) != 9:
            return "I could not find 9 unique numbers. Try again. For example: `bingo 1 2 3 4 5 6 7 8 9`. The valid numbers are in the range 1-42", False
    
    if randomplate:
        numbers = random.sample(range(1, 42), 9)

    canvas = Image.open("bingo/birthday_bingo.png").convert("RGB")
    
    for i, pos in enumerate(positions):
        try:
            x, y = pos
            tile = Image.open(f"bingo/{numbers[i]}.png")
            canvas.paste(tile, (x, y))
        except Exception:
            return f"I could not find hat number {numbers[i]}. Are you sure that is valid? The valid numbers are in the range 1-42", False
        
    tile.close()
    canvas.save('bingoplate.png')

    return "Here is your bingo plate, enjoy!", True


  
