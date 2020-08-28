from dotenv import load_dotenv
import os
import discord
import asyncio
import apts

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        print("background task started")
        await self.wait_until_ready()
        print("ready")
        counter = 0
        channel = self.get_channel(747626115996319745)  # channel ID goes here
        words = []
        old_found_posts = apts.found_posts()
        print("before the while loop")
        while not self.is_closed():  # while(true)
            print("in while loop")
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(30)  # task runs every 30 seconds
            print("30 seconds passed")
            print(old_found_posts[0])

            new_found_posts = apts.found_posts()
            if new_found_posts[0] != old_found_posts[0]:
                print("new stuff in the list")
                old_post_title = old_found_posts[0].find('a', class_='result-title hdrlnk')
                old_post_title_id = old_post_title['data-id']
                for post in new_found_posts:
                    new_post_title = post.find('a', class_='result-title hdrlnk')
                    new_post_title_id = new_post_title['data-id']
                    new_post_link = new_post_title['href']
                    if new_post_title_id != old_post_title_id:
                        words.append(new_post_link)
                print(words)
                await channel.send(" ".join(words))
                old_found_posts = new_found_posts.copy()
            else:
                print("no new posts")


client = MyClient()
client.run(TOKEN)