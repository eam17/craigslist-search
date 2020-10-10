import discord
import asyncio
from dotenv import load_dotenv
import os
import apts
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
keyarray = ["bike", "table", "ikea", "wood", "plane", "tool", "tools", "chisel", "chisels", "desk", "saw"]
url = 'https://denver.craigslist.org/search/zip?'

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)

    async def my_background_task(self):
        print("gonna wait..")
        await self.wait_until_ready()

        channel = self.get_channel(747626115996319745)  # channel ID goes here
        #await channel.send("starting search")
        #print("looking for old posts")
        old_found_posts = list(apts.find_posts_key(keyarray, url))
        print("before the while loop")
        while not self.is_closed():  # while(true)
            counter = 0
            words = []
            new_found_posts = list(apts.find_posts_key(keyarray, url))
            old_post_title = old_found_posts[0].find('a', class_='result-title hdrlnk')
            old_post_title_id = old_post_title['data-id']
            #print(old_found_posts[0].find('a', class_='result-title hdrlnk').text)
            #print(new_found_posts[0].find('a', class_='result-title hdrlnk').text)
            if new_found_posts[0].find('a', class_='result-title hdrlnk')['data-id'] != old_post_title_id:
                print("new stuff in the list")
                for post in new_found_posts:
                    new_post_title = post.find('a', class_='result-title hdrlnk')
                    new_post_title_id = new_post_title['data-id']
                    new_post_link = new_post_title['href']
                    if new_post_title_id != old_post_title_id:
                        print("if new_post_title_id != old_post_title_id:")
                        print(new_post_title_id)
                        print(new_post_title.text)
                        print(old_post_title_id)
                        print(old_post_title.text)
                        words.append(new_post_link)
                        post_hood = post.find('span', class_='result-hood').text
                        arr = new_post_title.text + post_hood + new_post_link
                        await channel.send(arr)
                        counter += 1
                    else:
                        break
                #print(words)
                #msg = " ".join(words).copy()
                #print(str(msg))
                #hi = "hi"
                #print(msg)
                #await channel.send(msg)
                # await channel.send("Found ", counter, " new posts --- ", datetime.now().strftime("%H:%M:%S"))
                old_found_posts = list(new_found_posts)
            print("Found ", counter, " new posts --- ", datetime.now().strftime("%H:%M:%S"))
            await asyncio.sleep(300)  # task runs every 300 seconds


client = MyClient()
client.run(TOKEN)
