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
url = "https://dotabot.creative-code.my.id/public/get-matches-player?id_player="

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

        average_gpm = df['gpm'].sum() / len(df)
        total_kill = df['kills'].sum()
        total_death = df['deaths'].sum()
        total_assist = df['assists'].sum()
        average_kda = total_kill+total_assist-total_death
        total_wins = df['result'].value_counts()['win']

        table = tabulate(df[['match_id', 'kills', 'deaths', 'assists', 'gpm', 'result', 'date']], headers='keys', tablefmt='fancy_grid')

        with open('table.txt', 'w', encoding="utf-8") as f:
            f.write(table)

        with open(image_path, 'rb') as f:
            file = discord.File(f, filename='table.txt')

        await ctx.send("Data Yang Diperoleh :")
        await ctx.send(file=file)
        await ctx.send(f"```Average GPM: {average_gpm}```")
        await ctx.send(f"```Average KDA: {average_kda}```")
        await ctx.send(f"```Jumlah Menang dalah 10 Game: {total_wins}```")

        m_distance = abs((average_gpm - 640) + (average_kda - 230))

        await ctx.send(f"```Manhattan Distance: {m_distance}```")

        if m_distance > 20 and m_distance <=60 and total_wins >= 5:
            await ctx.send(f"**Akun Ini Terindikasi Smurf**")
        elif m_distance < 20 and total_wins >=5:
            await ctx.send(f"**Akun Ini Terindikasi Smurf Rank Tinggi**")
        elif m_distance > 60:
            await ctx.send(f"**Akun Ini Bukan Smurf**")

    except discord.errors.HTTPException:
        await ctx.send('Terjadi kesalahan saat mengirim pesan. Mohon coba lagi.')

@input.error
async def input_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Mohon berikan input yang valid. Contoh: `!input <data>`')

bot.run('MTA5MzAwNTg4NDg2NDYxMDMxNA.GeQhHd.xcPX_yUPYYkL4q3RlT8wbVMOtAlnfMEyiGI_hI')
