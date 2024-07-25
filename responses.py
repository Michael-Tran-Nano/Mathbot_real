#from mathquiz import answer, insertprice, pricelist
# from quiz import quizanswer, quizanswers
from vb_quiz import vb_answer, vb_answers
from imageeditor import maker
from hat_image_maker import make_hat_image
# from gif_rygsæk_discord import bag_maker
import random
import discord
# import re
from new_hats import identify_hat

def handle_response(message_obj, user_message, context): # You get string and or file name
    tagname = message_obj.author.mention,
    username = message_obj.author

    # Make lower case to simplify recognition
    p_message = user_message.lower()

    # VB question
    if p_message[0] == '%':
        # Get all questions and answers
        if p_message == r"%answers":
            return vb_answers(), None
        
        # Find answer to specific question
        return vb_answer(p_message[1:]), None

    # # Quiz question
    # if p_message[0] == '%':
        
    #     # Get all questions and answers
    #     if p_message == r"%answers":
    #         return quizanswers(), None
        
    #     # Find answer to specific question
    #     return quizanswer(p_message[1:]), None
    
    # Make bingo plates
    elif p_message.startswith('bingo '):
        if 'random' in p_message:
            #message, success = maker('', randomplate=True, name=username)
            return "The random function is still turned off, and it will not be turned on again :angry:... Use a random generator yourself or something...", discord.File('bingo/howto.png')
        else:
            user_message, success = maker(p_message[len('bingo'):], context, name=username)

        if success: # Bingo plate made
            return user_message, discord.File('bingoplate.png')
        else: # No bingo plate made
            return user_message, discord.File('bingo/howto.png')
        
    # Make a dressed up animal image
    elif p_message[0] == '!':
        p_message = p_message.replace('=', ':')

        # Save new hat
        if p_message.startswith('!save,'):
            try:
                response = identify_hat(p_message[len('!save,'):])
                return response, discord.File('ready_animal_with_hat.png') # add a proper image
            except KeyError as e:
                return e, None # Attach guide
            except Exception as e:
                print(e)
                return "Something went wrong, try to check your response gain", None # Make helping image

        # make image
        try:
            make_hat_image(p_message[1:])
            return "Here is your image. Enjoy", discord.File('ready_animal_with_hat.png') # Maybe give differnet possible responses
        except KeyError as e:
            return e, None
        except Exception:
            return "Something went wrong, try to check your response gain", None # Make helping image

    # # Math equation given
    # elif p_message[0] == '!':
        
    #     # Add new price
    #     if p_message.startswith('!:'):
    #         try:
    #             return insertprice(p_message[2:], str(username)), None
                            
    #         except Exception:
    #             return "Something went wrong with adding a new hat :( Try again", None

    #     # Pricelist
    #     if p_message.startswith('!pricelist'):
    #         return pricelist(), None

    #     # Try to answer math question
    #     try:
    #         return answer(p_message[1:]), None
    #     except Exception as e:
    #         print(e)
    #         return "Something went wrong :( Try again", None

    # elif p_message.startswith('bag_maker'):
    #     try:
    #         message, success = bag_maker(p_message[len('bag_maker'):])
    #         if success:
    #             return message, discord.File('HP_bytte_image.gif')
    #         else: 
    #             return message, None

    #     except Exception as e:
    #         print(e)
    #         return "Something went wrong :( Try again", None

    # elif p_message == 'time':
    #     with open('time.txt', 'r') as f:
    #         time = f.readline()

    #     return f'The time for next task at Ryttern is at XX:{int(time):02d}', None

    # elif p_message.startswith('set time'):
        
    #     # Take the number from the string
    #     no = int(re.sub('[^0-9]', '', p_message))

    #     # Check if valid string
    #     if 0 <= no < 60:
    #         with open('time.txt', 'w') as f:
    #             f.write(str(no))
    #         return f'The new time has been set to XX:{no:02d}', None
    #     else:
    #         return f'\"{no}\" is not recognized as a valid time. Please use a number in the range 0-59', None

    # The rest are simply funny chat responses
    elif p_message == 'hello':
        messages = [("Hey there!", None),
                    (f"Hello {tagname}", None),
                    ('Hello Logen member :D', None),
                    (f"Hello {tagname}, how are you doing today?", None),
                    (None, discord.File('images/fellow.gif')),
                    ("Hello let\'s dig a lot of maps today :bone: :map:", None),
                    (":wink:", None)]
        
        return random.choice(messages)

    elif p_message == 'kartoffel':
        return r'https://tenor.com/view/potato-potatoes-tates-taties-yummy-gif-5444388407561106351', None
    
    elif p_message == 'gib motivation':
        return ":tada: :partying_face: :tada:", discord.File('images/proud.gif')
    
    elif p_message == '69':
        return "( ͡° ͜ʖ ͡°)", None
    
    elif p_message == 'hurray':
        return r'https://tenor.com/view/yay-sponge-bob-happy-celebration-job-gif-19821202', None
    
    elif p_message == "bomb ryttern":
        return (":bomb: :bomb: :bomb:",
                discord.File(random.choice(['images/bomb1.gif', 'images/bomb2.gif'])))