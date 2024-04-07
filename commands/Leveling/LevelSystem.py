import random

import discord
from discord.ext import commands
import json
import time


class LevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.user_cooldowns = {}

    async def update_data(self, users, user):
        if str(user.id) not in users:
            users[str(user.id)] = {}
            users[str(user.id)]['experience'] = 0
            users[str(user.id)]['level'] = 1

    async def add_experience(self, users, user, exp):
        users[str(user.id)]['experience'] += exp

    async def level_up(self, users, user, channel):
        experience = users[str(user.id)]['experience']
        lvl_start = users[str(user.id)]['level']
        lvl_end = int(experience ** (1 / 4))

        if lvl_start < lvl_end:
            await channel.send(f'{user.mention} has leveled up to level {lvl_end}')
            users[str(user.id)]['level'] = lvl_end

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            user_id = str(message.author.id)
            if user_id in self.user_cooldowns:
                if time.time() - self.user_cooldowns[user_id] < 60:
                    return
            self.user_cooldowns[user_id] = time.time()

            with open('jsons/level.json', 'r') as f:
                users = json.load(f)
            exptogive = random.randint(3, 5)
            await self.update_data(users, message.author)
            await self.add_experience(users, message.author, exptogive)
            await self.level_up(users, message.author, message.channel)

            with open('jsons/level.json', 'w') as f:
                json.dump(users, f)


async def setup(client):
    await client.add_cog(LevelSystem(client))
