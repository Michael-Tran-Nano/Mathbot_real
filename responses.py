from mathquiz import answer, insertprice, pricelist
from quiz import quizanswer, quizanswers
import random
import discord
import re

def handle_response(message, tagname=None, username=None): # You get string and or file name

    p_message = message.lower() # make lower case

    if p_message == 'hello': # make more possible outcomes
        messages = [("Hey there!", None),
                    (f"Hello {tagname}", None),
                    ('Hello Logen member :D', None),
                    (f"Hello {tagname}, how are you doing today?", None),
                    (None, discord.File('fellow.gif')),
                    ("Hello let\'s dig a lot of maps today :bone: :map:", None),
                    (":wink:", None)]
        
        return random.choice(messages)
    
    elif p_message == 'gib motivation':
        return ":tada: :partying_face: :tada:", discord.File('proud.gif')
    
    elif p_message == '69':
        return "( ͡° ͜ʖ ͡°)", None
    
    elif p_message == 'hurray':
        return r'https://tenor.com/view/yay-sponge-bob-happy-celebration-job-gif-19821202', None

    elif p_message == 'time':

        with open('time.txt', 'r') as f:
            time = f.readline()

        return f'The time for next task at Ryttern is at XX:{int(time):02d}', None
    
    elif p_message == "bomb ryttern":
        return (":bomb: :bomb: :bomb:",
                discord.File(random.choice(['bomb1.gif', 'bomb2.gif'])))

    elif p_message.startswith('set time'):
        
        # Take the number from the string
        no = int(re.sub('[^0-9]', '', p_message))

        # Check if valid string
        if 0 <= no < 60:
            with open('time.txt', 'w') as f:
                f.write(str(no))
            return f'The new time has been set to XX:{no:02d}', None
        else:
            return f'\"{no}\" is not recognized as a valid time. Please use a number in the range 0-59', None

    # Math equation given
    elif p_message[0] == '!':
        
        # Add new price
        if p_message.startswith('!:'):
            
            # Check for permission
            if str(username) not in ['smartlatios', 'illogicalpuzzle']:
                return "You do not have permission to add prices >:D", None

            try:
                res = insertprice(p_message[2:])

                if isinstance(res, tuple):
                    hat, price = res
                    return f"{hat} has been added to the list with the price {price}", None

                elif isinstance(res, str):
                    return res, None
                
            except Exception as e:
                print(e)
                return "Something went wrong with adding a new hat :( Try again", None

        # Pricelist
        if p_message.startswith('!pricelist'):
            return pricelist(), None

        try:
            result = answer(p_message[1:])
            if isinstance(result, tuple):
                math, total = result
                return f'The answer is: {math} = {total}', None
            
            elif isinstance(result, str):
                return f'The hat <{result}> is not found in my price list. Please ask Kartoffel to update it. You can check all prices by using `!pricelist` (use % if you meant to ask about a quiz question)', None
            else:
                return "Something went wrong :( Try again", None
        except Exception as e:
            print(e)
            return "Something went wrong :( Try again", None
        
        # make something for the time

        # Answer quiz questions?

    # Quiz question
    elif p_message[0] == '%':
        
        # Get all questions and answers
        if p_message == r"%answers":
            return quizanswers(), None
        
        # Find answer to specific question
        result = quizanswer(p_message[1:])

        if isinstance(result, str):
            return f"The answer is: {result}", None
        elif isinstance(result, list):
            return f"Possible answers {result}", None
        else:
            return r"Answer to quiz not found :( Please ask Kartoffel to add it. You can also check all the answer by writing `%answers` (Use ! if you meant to send a math question instead)", None
    
    elif p_message == 'kartoffel':
        return r'https://tenor.com/view/potato-potatoes-tates-taties-yummy-gif-5444388407561106351', None