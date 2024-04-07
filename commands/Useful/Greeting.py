import discord
import json
from discord.ext import commands


class Greeting(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.greeting_channel_id = None
        self.greeting_message = None
        self.load_greetings()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Greeting can be found")

    def load_greetings(self):
        try:
            with open('jsons/greetings.json', 'r') as f:
                greetings = json.load(f)
            channel_id = greetings.get('channel_id')
            guild_id = greetings.get('guild_id')
            if channel_id is not None and guild_id is not None:  # Add this check
                self.greeting_channel_id = int(channel_id)
                self.greeting_guild_id = int(guild_id)
                self.greeting_message = greetings.get('message')
        except FileNotFoundError:
            # If the file doesn't exist, don't load anything.
            pass

    # Setting up a greeting
    @commands.command()
    async def greeting(self, ctx, channel_id: int, *, description):
        self.greeting_channel_id = channel_id
        self.greeting_message = description
        self.greeting_guild_id = ctx.guild.id  # save the server ID
        greetings = {
            'channel_id': str(channel_id),
            'message': description,
            'guild_id': str(ctx.guild.id),  # store the server ID
        }
        with open('jsons/greetings.json', 'w') as f:
            json.dump(greetings, f)

        print(f"Greeting channel: {self.greeting_channel_id}")
        print(f"Greeting message: {self.greeting_message}")
        print(f"Greeting guild: {self.greeting_guild_id}")

        await ctx.send("Greeting set successfully!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.greeting_channel_id and self.greeting_message and member.guild.id == self.greeting_guild_id:
            channel = self.client.get_channel(self.greeting_channel_id)
            if channel:
                await channel.send(f'Welcome {member.mention}! {self.greeting_message}')
            else:
                print(f"Could not find channel with id {self.greeting_channel_id}")
        else:
            print("No greeting channel or message set or the member joined another guild")


async def setup(client):
    await client.add_cog(Greeting(client))
