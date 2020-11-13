import discord
import cfg
import openpyxl
import warnings
import random

# #Ignoraa openpyxl style herjan:
#warnings.simplefilter("ignore")

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
    
    if message.content.startswith('+alko'):
        wb = openpyxl.load_workbook('prod.xlsx')
        sheet = wb.get_sheet_by_name('Alkon Hinnasto Tekstitiedostona')
        alue = sheet['I5':'I15000']
        user_input = message.content[6:]
        print(user_input)
        juoma = user_input

        if user_input == "viini":
            juoma = random.choice(["punaviinit", "valkoviinit", "Jälkiruokaviinit, väkevöidyt ja muut viinit", "roseeviinit"])
        elif user_input == "väkevät":
            juoma = random.choice(["vodkat ja viinat", "Ginit ja maustetut viinat", "Brandyt, Armanjakit ja Calvadosit", "viskit", "konjakit", "rommit"])
        elif user_input == "mieto" or user_input == "miedot":
            juoma = random.choice(["oluet", "siiderit", "juomasekoitukset"])
        elif user_input == "punkku" or user_input == "puna" or user_input == "punaviini":
            juoma = "punaviinit"
        elif user_input == "viina" or user_input == "votka" or user_input == "vodka":
            juoma = "vodkat ja viinat"
        elif user_input == "valkkari" or user_input == "valko" or user_input =="valkoviini":
            juoma = "valkoviinit"
        else:
            juoma = user_input
        print(juoma)
        def find_row(string):
            rivit = []
            for row in alue:
                for cell in row:
                    if cell.value == juoma:
                        rivit.append(cell.row)
            return rivit
        tulos = find_row(juoma)
        def product(tulos):
            rnd = str(random.choice(tulos))
            tuotenro = sheet['A' + rnd].value
            tuotenimi = sheet['B' + rnd].value
            tuotesivu = "https://www.alko.fi/tuotteet/"+ tuotenro
            return (tuotenimi + "\n" + tuotesivu)
        await message.channel.send(product(tulos))



client.run(cfg.token)




    # Wait for esimerkki, tsekkaa api
    # if message.content.startswith('+greet'):
    #     channel = message.channel
    #     await channel.send('Say hello!')

    #     def check(m):
    #         return m.content == 'hello' and m.channel == channel

    #     msg = await client.wait_for('message', check=check)
    #     await channel.send('Hello {.author}!'.format(msg))