import discord
import cfg
import random

# Todo:
# Alko funktionaalisuus jos onnistuu
#   Hinnasto löytyy excel filuna, päivittyy päivittäin
#       Botti hakis filun netist ja lukis sielt datan
#       Tai sit staattinen kerran ladattu filu, joka vois päivittyä botin käynnistykses (varmaa parempi)

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



# import openpyxl
# import warnings
# import random
# #Ignoraa openpyxl style herjan:
# warnings.simplefilter("ignore")

# wb = openpyxl.load_workbook('prod.xlsx')
# sheet = wb.get_sheet_by_name('Alkon Hinnasto Tekstitiedostona')
# alue = sheet['I5':'I15000']

# # for cell in viinit:
# #   if cell[0].value == 'punaviinit':
# #     print(cell[0].value)
# juoma = 'oluet'
# def find_row(viini):
#   #kato tota iter_rows hommaa viel se kai nopeempi jotenki
#   rivit = []
#   for row in alue:
#     for cell in row:
#       if cell.value == juoma:
#         rivit.append(cell.row)
#   return rivit

# tulos = find_row(juoma)

# def product(tulos):
#   tuotenimi = sheet['B' + str(random.choice(tulos))].value
#   print(tuotenimi)
  


# product(tulos)