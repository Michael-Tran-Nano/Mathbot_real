import discord
import responses
from datetime import datetime
import json
import os
import context_object
from collections import Counter
import aiohttp

async def send_message(message, user_message, context, is_private):

    # Try to get response to message
    try:
        response, file = responses.handle_response(message, user_message, context)

        if is_private:
            await message.author.send(response, file=file)
        else:
            await message.channel.send(response, file=file)

    # If something failed
    except Exception as e:
        print(e)


async def get_ref_image(message_obj):
    if message_obj.attachments:
        attachment = message_obj.attachments[0]  # Get the first attachment
    else:
        raise Exception("I could not see the image you wanted to send. Did you rememeber to add it?")
    
    if "png" not in attachment.url.lower():
        raise Exception("Please send an image in the .png format")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(attachment.url) as resp:

            if resp.status != 200:
                raise Exception("I could not read the image you sent. Something went wrong")
            
            content_length = resp.headers.get('Content-Length')
            if content_length is not None and int(content_length) > 1048 * 1048:
                raise Exception("The image you sent is too large. Please crop it to make it fit")
            data = await resp.read()
            with open("haystack.png", 'wb') as f:
                f.write(data)
                await message_obj.channel.send('Image loading successfully. Now I am going to scan it')


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

    # Pass around relevant things
    context = None

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        nonlocal context
        context = context_object.Context()
        try:
            with open("bingolog.txt") as f:
                names = [line.split(',')[0] for line in f.readlines()]
                context.bingo_counter = Counter(names)
        except Exception:
            print("Failed to read bingolog.txt")

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

        if '!save' in user_message:
            try:
                await get_ref_image(message)
            except Exception as e:
                await message.channel.send(e)
                return None

        #Check if it is a private message, and send relevant information
        if len(user_message) > 0 and user_message[0] == '?':
            user_message = user_message[1:] 
            await send_message(message, user_message, context, is_private=True)
        else:
            await send_message(message, user_message, context, is_private=False)
        
    client.run(TOKEN)