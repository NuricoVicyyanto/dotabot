import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot sudah siap.')

@bot.command()
async def input(ctx, *, input_data):
    try:
        await ctx.send(f'Data yang Anda masukkan: {input_data}')
    except discord.errors.HTTPException:
        await ctx.send('Terjadi kesalahan saat mengirim pesan. Mohon coba lagi.')

@input.error
async def input_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Mohon berikan input yang valid. Contoh: `!input <data>`')

bot.run('MTA5MzAwNTg4NDg2NDYxMDMxNA.GeQhHd.xcPX_yUPYYkL4q3RlT8wbVMOtAlnfMEyiGI_hI')
