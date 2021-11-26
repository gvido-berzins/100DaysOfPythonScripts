# ** smol-snek.py ** #

from dotenv import load_dotenv
import os, discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


@client.event
async def on_message(message):
    await message.add_reaction(client.get_emoji(634696069137170441))

client.run(TOKEN)
