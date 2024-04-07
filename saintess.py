import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
import json
import logging

logging.basicConfig(level=logging.DEBUG)


def get_server_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

        return prefix[str(message.guild.id)]


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True  # Enable the GUILD_MESSAGES intent
intents.message_content = True  # Enable the privileged message content intent

client = commands.Bot(command_prefix="s!", help_command=None, intents=intents)
status = cycle([discord.Status.online, discord.Status.idle, discord.Status.dnd, discord.Status.invisible])
activity = cycle([discord.Game(name="Game 1"), discord.Streaming(name="Stream 1", url="http://twitch.tv/streamer"),
                  discord.Activity(type=discord.ActivityType.listening, name="Song 1"),
                  discord.Activity(type=discord.ActivityType.watching, name="Movie 1")])

bot_status = cycle(["Serving Velatu-Sama", "Walking around the Evellia Empire", "Playing board games with a goddess"])


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=next(status), activity=next(activity))


@client.event
async def on_ready():
    print(f'Lets have fun Velatu-Sama!')
    change_status.start()


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = "s!"

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)


@client.command()
async def setprefix(ctx, *, newprefix: str):
    with open("prefixes.json", "r") as f:
        prefix = json.load(f)

    prefix[str(ctx.guild.id)] = newprefix

    with open("prefixes.json", "w") as f:
        json.dump(prefix, f, indent=4)

        await ctx.send(f"Prefix has been set to {newprefix}")


async def load():
    for root, dirs, files in os.walk("./commands"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)  # get full path of files
                relative_path = path.replace("\\", "/")[2:-3]  # convert the file path to a module import path
                module_name = relative_path.replace("/", ".")
                await client.load_extension(module_name)



async def main():
    async with client:
        await load()
        await client.start("")


asyncio.run(main())
