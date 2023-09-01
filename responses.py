from mathquiz import answer

def handle_response(message: str) -> str:

    p_message = message.lower() # make lower case

    if p_message == 'hello':
        return "Hey there!"
    
    if p_message == 'gib motivation':
        return "You can do it!!!"

    if p_message[0] == '!':

        try:
            result = answer(p_message[1:])
            if isinstance(result, int):
                return f'The answer is: {result}'
            elif isinstance(result, str):
                return f'The hat <{result}> is not found in my price list. Please ask Kartoffel to update it'
            else:
                return "Something went wrong :( Try again"
        except Exception:
            return "Something went wrong :( Try again"
        
        # make something for the time

        # Answer quiz questions?
