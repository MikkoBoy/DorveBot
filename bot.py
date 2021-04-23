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
    # Muuttujia
    juoma = ""
    properties = []
    # Funktioita
    # käyttäjän syötteestä juomatyyppi, tän vois siistiä joskus järkevämmäks
    def get_product_type(str):
        if str == "viini":
            product_type = random.choice(["punaviinit", "valkoviinit", "Jälkiruokaviinit, väkevöidyt ja muut viinit", "roseeviinit"])
        elif str == "väkevät":
            product_type = random.choice(["vodkat ja viinat", "Ginit ja maustetut viinat", "Brandyt, Armanjakit ja Calvadosit", "viskit", "konjakit", "rommit"])
        elif str == "mieto" or str == "miedot":
            product_type = random.choice(["oluet", "siiderit", "juomasekoitukset"])
        elif str == "punkku" or str == "puna" or str == "punaviini":
            product_type = "punaviinit"
        elif str == "viina" or str == "votka" or str == "vodka":
            product_type = "vodkat ja viinat"
        elif str == "valkkari" or str == "valko" or str =="valkoviini":
            product_type = "valkoviinit"
        else:
            product_type = str
        return product_type
    
    # Kaikki rivit, joissa käyttäjän haluama juomatyyppi
    def find_rows():
        rivit = []
        final_rivit = []
        for row in ws2:
            for cell in row:
                if cell.value == juoma:
                    rivit.append(cell.row)
        # jos on hinta haarukkaa niin nää seuraavat
        # muussa tapauksessa ylempi rivi palautetaan
        if len(properties) == 2:
            for i in range(len(rivit)):
                rivi_numero = str(rivit[i])
                if float(ws2['E' + rivi_numero].value) < float(properties[1]):
                    final_rivit.append(int(rivi_numero))
            return final_rivit
        elif len(properties) == 3:
            for i in range(len(rivit)):
                rivi_numero = str(rivit[i])
                if float(ws2['E' + rivi_numero].value) > float(properties[1]) and float(ws2['E' + rivi_numero].value) < float(properties[2]):
                    final_rivit.append(int(rivi_numero))
            return final_rivit
        else:
            return rivit

    # Tää ajetaan find_rows():in riveillä, pyöräytetään randomilla arraysta ja vertaillaan se excelin vastaavaan rivinumeroon
    # Kun rivi on tiedossa se voidaan leipoa linkkiin ja palauttaa viestinä nimen kera
    def find_product(arr):
        rnd = str(random.choice(arr))
        tuotenro = ws2['A' + rnd].value
        tuotenimi = ws2['B' + rnd].value
        tuotekoko = ws2['D' + rnd].value
        tuotehinta = ws2['E' + rnd].value
        tuotesivu = "https://www.alko.fi/tuotteet/"+ tuotenro
        return (tuotenimi + "\n" + tuotekoko + ", "+ tuotehinta + "€" +"\n" + tuotesivu)


    ######                     ######
    ######  Message funktiot   ######
    ######                     ###### 
    if message.author == client.user:
        return
    # help
    if message.content.startswith('+help'):
        await message.channel.send('+choose --- Erottele valinnat pilkulla (yks,kaks,kol) \n +alko --- Laita perään mitä haluut, jotkut synonyymit toimii esim punkku, viina, valkkari yms')
    # +choose funktio, splittaa messagen pilkuista arrayks, josta randomilla valitaan yks
    if message.content.startswith('+choose '):
        user_choices = message.content[8:].split(',')
        try:
            await message.channel.send(random.choice(user_choices))
        except:
            await message.channel.send(':flushed:')
    
    # Alkon katalogin tonkiminen randomi pullolle
    if message.content.startswith('+alko'):
        user_input = message.content[6:]
        # Tähän vois jatkossa tehä jonku syötteen tarkistuksen, nyt menee tällee
        if ',' in user_input:
            properties = user_input[0:].split(',')
            if '-' in properties[1]:
                properties += properties[1].split('-')
                properties.pop(1)
        else:
            properties.append(user_input)
        
        juoma = get_product_type(properties[0])
        juoma_rivit = find_rows()
        try:
            await message.channel.send(find_product(juoma_rivit))
        except:
            await message.channel.send(":flushed:")


client.run(cfg.token)




    # Wait for esimerkki, tsekkaa api
    # if message.content.startswith('+greet'):
    #     channel = message.channel
    #     await channel.send('Say hello!')

    #     def check(m):
    #         return m.content == 'hello' and m.channel == channel

    #     msg = await client.wait_for('message', check=check)
    #     await channel.send('Hello {.author}!'.format(msg))