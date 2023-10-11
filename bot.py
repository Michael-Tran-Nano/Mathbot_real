import discord
import responses

async def send_message(message, user_message, is_private):
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
    # TOKEN = 'MTE0NzE3MDk4NjkyODY0ODMzMw.GQmxzc.j4MfLM6aRxEu_74zfPqSzmNaQ7170NU1Tle6tk' # Testbot
    TOKEN = "MTE0Njc1MjAzMzQ5NjUxNDYyMw.GOSkwd.ignHOCUcNltTo64TraNtJY7BHU3PEzaGeqbbdQ" # Logen
    intents = discord.Intents.default()
    intents.message_content = True
    intents.dm_messages = True
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

        print(f'{username} said: "{user_message}" ({channel})')

        #Check if it is a private message, and send relevant information
        if user_message[0] == '?':
            user_message = user_message[1:] 
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)