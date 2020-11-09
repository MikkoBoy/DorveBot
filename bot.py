import discord
import cfg

client = discord.Client()

@client.event
async def on_ready():
  print("Logged in")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('+hello'):
        await message.channel.send('Hello!')

client.run(cfg.token)