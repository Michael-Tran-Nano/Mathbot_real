from PIL import Image
import random
import re


# Positions of the tiles
# Small plate
# positions = [(38, 271), (99, 271), (160, 271), (38, 332), (99, 332), (160, 332), (38, 393), (99, 393), (160, 393)]
# Big plate
positions = [(46, 280), (130, 280), (213, 280), (46, 364), (130, 364), (213, 364), (46, 447), (130, 447), (213, 447)]

def maker(numbers: str, context, randomplate=False, name='Null'):

    if randomplate == False:
        numbers = re.sub("\D", " ", numbers) # remove non-numbers
        numbers = numbers.split()

        # See if something is wrong
        if len(set(numbers)) != 9:
            if (len(numbers) != 9):
                return f"I could not find 9 numbers. I found {len(numbers)} numbers instead!", False
            else:
                for i in numbers:
                    if (numbers.count(i) > 1):
                        return f'You wrote the number "{i}" {numbers.count(i)} times. That does not make a valid plate...', False
                return "I could not find 9 unique numbers. Try again. For example: `bingo 1 2 3 4 5 6 7 8 9`. The valid numbers are in the range 1-42", False
        
        # Make to integers
        numbers = [int(x) for x in numbers]
    
    if randomplate:
        numbers = random.sample(range(1, 42), 9)

    canvas = Image.open("bingo/BINGOPLATTA.png").convert("RGB")
    
    for i, pos in enumerate(positions):
        try:
            x, y = pos
            tile = Image.open(f"bingo/{numbers[i]}.png").convert("RGBA")
            canvas.paste(tile, (x, y), tile)
        except FileNotFoundError:
            return f"I could not find hat number {numbers[i]}. Are you sure that is valid? The valid numbers are in the range 1-42", False
        
    tile.close()
    canvas.save('bingoplate.png')
    canvas.close()
    
    if numbers == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        return r"What an original choice of plate :face_with_hand_over_mouth: https://tenor.com/view/spongebob-meme-spongebob-spongebob-squarepants-squidward-how-original-gif-20004154", True
    if 69 in numbers:
        return r"https://tenor.com/view/lenny-eyebrow-flirt-smile-gif-5516050", True
    if 100 in numbers:
        return "You are cool, but sadly, your plate is invalid...", True
    
    # Make a log for normal plates
    with open("bingolog.txt", "a") as f:
        f.write(f"{name},{numbers},{randomplate}\n")

    if context != None:
        name = str(name)
        if (name in context.bingo_counter):
            context.bingo_counter[name] += 1
        else:
            context.bingo_counter[name] = 1
    
        if (context.bingo_counter[name] > 2):
            return f"This is at least your plate number {context.bingo_counter[name]} in this session. Are you really this indecisive? :rolling_eyes:", True

    return "Here is your bingo plate, enjoy!", True


  

