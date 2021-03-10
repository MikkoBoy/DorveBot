import discord
import cfg
import requests
import openpyxl
import warnings
import random

#Ignoraa openpyxl style herjan:
#warnings.simplefilter("ignore")


# Todo:
# Alko hinnat
# Sijainti?
# Command: Imitoi / average kommentti == lukee viestihistorian ja muodostaa siitä keskiverto kommentin
# Iltasaatana
client = discord.Client()

#Alkon hinnaston lataaminen
try:
    res = requests.get('https://www.alko.fi/INTERSHOP/static/WFS/Alko-OnlineShop-Site/-/Alko-OnlineShop/fi_FI/Alkon%20Hinnasto%20Tekstitiedostona/alkon-hinnasto-tekstitiedostona.xlsx')
    res.raise_for_status()
    playFile = open('prod.xlsx', 'wb')
    for chunk in res.iter_content(100000):
      playFile.write(chunk)
    playFile.close()
    print("Excel ladattu")
except:
    print("Excelin lataus failas")

#Excel auki
wb = openpyxl.load_workbook('prod.xlsx')
sheet = wb.get_sheet_by_name('Alkon Hinnasto Tekstitiedostona')
ws2 = wb.create_sheet('New sheet')

def clean_workbook():
    #Siistii tilausvalikoiman pois taulukosta
    for row in sheet.values:
        if row[28] == "tilausvalikoima":
            continue
        ws2.append(row)
    del wb['Alkon Hinnasto Tekstitiedostona']
    ws2.title = "Otsikko"
    wb.save('new.xlsx')
    print("Tilausvalikoima poistettu")

clean_workbook()

@client.event
async def on_ready():
  print("Logged in")
  game = discord.Game("with myself | +help")
  await client.change_presence(activity=game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('+help'):
        await message.channel.send('+choose --- Erottele valinnat pilkulla (yks,kaks,kol) \n +alko --- Laita perään mitä haluut, jotkut synonyymit toimii esim punkku, viina, valkkari yms')

    if message.content.startswith('+choose '):
        testi = message.content[8:].split(',')
        try:
            await message.channel.send(random.choice(testi))
        except:
            await message.channel.send(':flushed:')
    
    if message.content.startswith('+alko'):
        user_input = message.content[6:]
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
        def find_row(string):
            rivit = []
            for row in ws2:
                for cell in row:
                    if cell.value == juoma:
                        rivit.append(cell.row)
            return rivit
        tulos = find_row(juoma)
        def product(tulos):
            rnd = str(random.choice(tulos))
            tuotenro = ws2['A' + rnd].value
            tuotenimi = ws2['B' + rnd].value
            tuotesivu = "https://www.alko.fi/tuotteet/"+ tuotenro
            return (tuotenimi + "\n" + tuotesivu)
        try:
            await message.channel.send(product(tulos))
        except:
            await message.channel.send(":flushed:")

    if message.content.startswith('lopetin juomisen') or message.content.startswith('lopetan juomisen') or message.content.startswith('en juo tänää'):
        await message.channel.send('En usko')

client.run(cfg.token)




    # Wait for esimerkki, tsekkaa api
    # if message.content.startswith('+greet'):
    #     channel = message.channel
    #     await channel.send('Say hello!')

    #     def check(m):
    #         return m.content == 'hello' and m.channel == channel

    #     msg = await client.wait_for('message', check=check)
    #     await channel.send('Hello {.author}!'.format(msg))