# bot.py
import os

import apts

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#client = discord.Client()
bot = commands.Bot(command_prefix='!')

#@client.event
#async def on_ready():
    #print(f'{client.user} has connected to Discord!')
    #client.channels.get(676145120910901293/747626115996319745).send('Text')

@bot.command()
async def test(ctx, keyword):
    posts_list = apts.find_posts_key(keyword)
    words = list()
    for item in posts_list:
        words.append(item[0])
        words.append(item[1])
    #await ctx.send('I heard you! {0} Keyword: {1}'.format(ctx.author, keyword))
    await ctx.send(" ".join(words))

#client.run(TOKEN)
bot.run(TOKEN)