import discord
from discord.ext import commands
import discord.utils
import asyncio
from dotenv import load_dotenv
import os
from datetime import datetime
import dbcraigslist

# Contains functions for operating on the keyword list
import dbkeywords_list

# Pausing the thread
import time

# craigslist_notify_bot.py

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
url = 'https://denver.craigslist.org/search/zip?'
bot = commands.Bot(command_prefix='!')


@bot.command(name='hi')
async def show_words(ctx, arg):
    await ctx.send(arg)


@bot.command(name='list')
async def list_cmd(ctx):
    key_array = dbkeywords_list.fetch_keywords()
    msg = ', '.join(key_array)
    await ctx.send(msg)


@bot.command(name='cmd')
async def help_cmd(ctx):
    msg = "List of commands: \n" \
          "!help: returns a list of commands\n" \
          "!list: returns the list of keywords\n" \
          "!add **keyword**: add **keyword** to the list of items to search for\n" \
          "!del **keyword**: delete **keyword** from the list of items to search for"
    await ctx.send(msg)


@bot.command(name='add')
async def add_cmd(ctx, arg):
    dbkeywords_list.add_new_keywords([arg])
    msg = (arg, " added")
    await ctx.send(msg)


@bot.command(name='del')
async def add_cmd(ctx, arg):
    key_array = dbkeywords_list.fetch_keywords()
    if arg in key_array:
        dbkeywords_list.remove_keywords([arg])
        # turn into strings..
        msg = (arg, " deleted")
    else:
        msg = (arg, " was not found")
    await ctx.send(msg)


# help - all commands
# return list we're searching
# add/remove a word
# add/remove a list of words

# how to send to the channel without having a ctx

# can filter by miles now
# next set up a table matching channels to miles willing to travel and url to search for, and city + state
# during the first start, it should ask for values to be filled in
# during other starts, it should print out the values it has
# give a way to change those values

# eventually, each item will have max miles and max price

@bot.command(name='s')
async def start_search(ctx):
    await ctx.send("Starting search")
    old_time = datetime.now()
    print(old_time)
    while True:
        print("while loop")
        # Check if there are any new posts since old_time
        key_array = dbkeywords_list.fetch_keywords()
        new_posts = dbcraigslist.check_for_new_posts(url, old_time, key_array)
        # new_posts = dbcraigslist.check_distance(new_posts, "aurora colorado", 30)
        print("new posts? : ", new_posts)
        if len(new_posts) > 0:
            # Reset the time
            old_time = datetime.now()
            # New posts found!
            for post in new_posts:
                print("new post - ", post[0])
                msg = '{} {} {}'.format(post[1], post[2], post[0])
                await ctx.send(msg)
        await asyncio.sleep(300)  # task runs every 300 seconds
        # await ctx.send(datetime.now().strftime("%H:%M:%S"))


# class MyClient(discord.Client):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # create the background task and run it in the background
#         self.bg_task = self.loop.create_task(self.my_background_task())

@bot.event
async def on_ready():
    server = discord.utils.get(bot.guilds)
    print(server.id)
    # add a record with current server id if doesn't exist
    # check each column to see if it's null. If it is, prompt user to fill it
    dbkeywords_list.check_server_db(server)
    for channel in server.channels:
        if str(channel) == "bot":
            print("hi")
            # await channel.send('Hello! Reply with **!s** to begin search')
    # print('Logged in as')
    # print(self.user.name)


# async def my_background_task(self):
#     print("first entrance")
#     await self.wait_until_ready()
#     channel = self.get_channel(747626115996319745)  # channel ID goes here
#     print(channel)
#     # Grab the time at start of execution
#     old_time = datetime.datetime.now()
#     print(old_time)
#     while not self.is_closed():  # while(true)
#         print("while loop")
#         # Check if there are any new posts since old_time
#         new_posts = await dbcraigslist.check_for_new_posts(url, old_time)
#         print("new posts? : ", new_posts)
#         if len(new_posts) > 0:
#             # Reset the time
#             old_time = datetime.datetime.now()
#             # New posts found!
#             for post in new_posts:
#                 print("new post - ", post[0])
#                 await channel.send(post[1], post[2], post[0])
#         # await asyncio.sleep(300)  # task runs every 300 seconds
#         time.sleep(300)
#         await channel.send(datetime.now().strftime("%H:%M:%S"))


# client = MyClient()
# client.run(TOKEN)
bot.run(TOKEN)
