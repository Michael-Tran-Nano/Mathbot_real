from mathquiz import answer
import random
import discord

def handle_response(message, name): # You get string and or file name

    p_message = message.lower() # make lower case

    if p_message == 'hello': # make more possible outcomes
        messages = ["Hey there!", f"Hello {name}", 'Hello Logen member :D', f"Hello {name}, how are you doing today?"]
        return messages[random.randint(0, len(messages) - 1)], None
    
    if p_message == 'gib motivation':
        return ":tada: :partying_face: :tada:", discord.File('proud.gif')

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
