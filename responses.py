from mathquiz import answer
import random
import discord
import re

def handle_response(message, name): # You get string and or file name

    p_message = message.lower() # make lower case

    if p_message == 'hello': # make more possible outcomes
        messages = [("Hey there!", None),
                    (f"Hello {name}", None),
                    ('Hello Logen member :D', None),
                    (f"Hello {name}, how are you doing today?", None),
                    (None, discord.File('fellow.gif')),
                    ("Hello let\'s dig a lot of maps today :bone: :map:", None),
                    (":wink:", None)]
        
        return messages[random.randint(0, len(messages) - 1)]
    
    if p_message == 'gib motivation':
        return ":tada: :partying_face: :tada:", discord.File('proud.gif')
    
    if p_message == '69':
        return "( ͡° ͜ʖ ͡°)", None
    
    if p_message == 'hurray':
        return r'https://tenor.com/view/yay-sponge-bob-happy-celebration-job-gif-19821202', None

    if p_message == 'time':

        with open('time.txt', 'r') as f:
            time = f.readline()

        return f'The time for next task at Ryttern is at XX:{int(time):02d}', None
    
    if p_message[:8] == 'set time':
        
        # Add only the numbers to the string
        no = re.sub('[^0-9]', '', p_message)

        # Check if valid string
        if 0 <= int(no) < 60:
            with open('time.txt', 'w') as f:
                f.write(no)
            return f'The new time has been set to XX:{no}', None
        
        else:
            return f'\"{no}\" is not recognized as a valid time. Please use a number in the range 0-59', None

    # Math equation given
    if p_message[0] == '!':

        try:
            result = answer(p_message[1:])
            if isinstance(result, tuple):
                math, total = result
                return f'The answer is: {math} = {total}', None
            
            elif isinstance(result, str):
                return f'The hat <{result}> is not found in my price list. Please ask Kartoffel to update it', None
            else:
                return "Something went wrong :( Try again", None
        except Exception:
            return "Something went wrong :( Try again", None
        
        # make something for the time

        # Answer quiz questions?
