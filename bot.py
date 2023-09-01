import discord
import responses

async def send_message(message, user_message, is_private):
    try:
        response, file = responses.handle_response(user_message)

        # discord.File('red.png')

        if is_private:
            await message.author.send(response, file=file)
        else:
            await message.channel.send(response, file=file)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTE0Njc1MjAzMzQ5NjUxNDYyMw.GOSkwd.ignHOCUcNltTo64TraNtJY7BHU3PEzaGeqbbdQ'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:] 
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)