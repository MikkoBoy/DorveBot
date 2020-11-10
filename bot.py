import discord
import cfg
import random

client = discord.Client()

@client.event
async def on_ready():
  print("Logged in")
  game = discord.Game("with myself")
  await client.change_presence(activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('+help'):
        await message.channel.send('+choose ---- Erottele valinnat pilkulla (yks,kaks,kol) \n ei muuta :smiley:')

    if message.content.startswith('+choose '):
        testi = message.content[8:].split(',')
        try:
            await message.channel.send(random.choice(testi))
        except:
            await message.channel.send(':flushed:')
    # Wait for esimerkki, tsekkaa api
    # if message.content.startswith('+greet'):
    #     channel = message.channel
    #     await channel.send('Say hello!')

    #     def check(m):
    #         return m.content == 'hello' and m.channel == channel

    #     msg = await client.wait_for('message', check=check)
    #     await channel.send('Hello {.author}!'.format(msg))

client.run(cfg.token)