import discord
from discord.ext import commands
import requests
from tabulate import tabulate
import pandas as pd
from discord import File

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
url = "https://dotabot.mitrajamurbondowoso.com/public/get-matches-player?id_player="

image_path = 'table.txt'

@bot.event
async def on_ready():
    print(f'Bot siap')

@bot.command()
async def input(ctx, *, input_data):
    try:
        await ctx.send(f'Data yang Anda masukkan: {input_data}')
        response = requests.get(url + input_data)
        data_json = response.json()
        df = pd.DataFrame(data_json['matches'])
        df['result'] = df['details'].apply(lambda x: x['result'])
        df['date'] = df['details'].apply(lambda x: x['date'])
        df['kills'] = df['details'].apply(lambda x: x['kills'])
        df['deaths'] = df['details'].apply(lambda x: x['deaths'])
        df['assists'] = df['details'].apply(lambda x: x['assists'])
        df['gpm'] = df['details'].apply(lambda x: x['gpm'])
        table = tabulate(df[['match_id', 'kills', 'deaths', 'assists', 'gpm', 'result', 'date']], headers='keys', tablefmt='fancy_grid')

        with open('table.txt', 'w', encoding="utf-8") as f:
            f.write(table)

        with open(image_path, 'rb') as f:
            file = discord.File(f, filename='table.txt')

        await ctx.send("Data Yang Diperoleh :")
        await ctx.send(file=file)
    except discord.errors.HTTPException:
        await ctx.send('Terjadi kesalahan saat mengirim pesan. Mohon coba lagi.')

@input.error
async def input_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Mohon berikan input yang valid. Contoh: `!input <data>`')

bot.run('MTA5MzAwNTg4NDg2NDYxMDMxNA.GeQhHd.xcPX_yUPYYkL4q3RlT8wbVMOtAlnfMEyiGI_hI')
