import discord
import responses
from datetime import datetime
import json
import os

async def send_message(message, user_message, is_private):

    # Try to get response to message
    try:
        response, file = responses.handle_response(user_message, tagname=message.author.mention, username=message.author)

        if is_private:
            await message.author.send(response, file=file)
        else:
            await message.channel.send(response, file=file)

    # If something failed
    except Exception as e:
        print(e)

def run_discord_bot():
    if os.path.isfile('tokens.json'):
        token_path = 'tokens.json'
    else:
        token_path = '../tokens.json'

    with open(token_path) as json_file:
        tokens = json.load(json_file)
    TOKEN = tokens['Testbot'] # Testbot, Logenbot
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):

        # Do nothing if it is from itself.
        if message.author == client.user:
            return
        
        username = str(message.author) # message.author.nick
        user_message = str(message.content)
        channel = str(message.channel)

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        message_log = f'{username} said: "{user_message}" ({channel}), {now}'

        print(message_log)
        with open("chatlog.txt", "a") as f:
            f.write(message_log + '\n')

        #Check if it is a private message, and send relevant information
        if len(user_message) > 0 and user_message[0] == '?':
            user_message = user_message[1:] 
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)