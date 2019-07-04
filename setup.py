import discord
import requests
from discord.ext import commands

api_url = "https://api.coinmarketcap.com/v1/ticker/bitcoin/"
app_url = "https://maker.ifttt.com/trigger/bitcoin/with/key/bz7bCPAUZGqVtlhEoDItFy"
token = "NTk2Mjk1MDkxOTMzNDEzNDE2.XR3dOQ.9jeCsp5c6Mz-iYFGmEUSyzQ74RQ"

bot = commands.Bot(command_prefix='!', description='A bot that greets the user back.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)
@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)
@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, there!")
@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")
@bot.command()
async def bitcoin(ctx):
    await ctx.send(get_bitcoin())

def get_bitcoin():
    price = get_lastest_price()
    bitcoin = ("The current value of one Bitcoin in € is: " + str(round(price, 2)))
    return bitcoin

def get_lastest_price():
    
    latest_price = requests.get(api_url)
    price_json = latest_price.json()
    determined_price = float(price_json[0]['price_usd'])
    converted_amount = convert_curr(determined_price)
    return converted_amount

def convert_curr(price):

    curr_api_key = "f010a66855ed881bb49f"

    curr_api_url = ("http://free.currencyconverterapi.com/api/v5/convert?q=EUR_USD&compact=ultra&apiKey=" + curr_api_key)

    conversion_factor = requests.get(curr_api_url)

    factor = conversion_factor.json()

    calc_fac = (factor["EUR_USD"]- 1)

    eu_conv = (price * calc_fac)

    return float(price - eu_conv)

bot.run(token)