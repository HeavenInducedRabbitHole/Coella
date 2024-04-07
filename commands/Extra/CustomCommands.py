import discord
from discord.ext import commands
import json
import os
from datetime import datetime

class CustomCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.commands_file = 'jsons/customcommands.json'
        self.load_commands()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Custom Commands can be found")

    def load_commands(self):
        if os.path.exists(self.commands_file):
            try:
                with open(self.commands_file, 'r') as f:
                    self.commands = json.load(f)
            except Exception as e:
                print(f"Error loading commands: {e}")
                self.commands = {}
        else:
            self.commands = {}

    def save_commands(self):
        try:
            with open(self.commands_file, 'w') as f:
                json.dump(self.commands, f)
        except Exception as e:
            print(f"Error saving commands: {e}")

    @commands.command(brief="Add a new command", help="Usage: !add_command <name> <response>")
    async def add_command(self, ctx, name, *, response):
        name = name.lower()
        self.commands[name] = response
        self.save_commands()
        await ctx.send(f"Command `{name}` added.")

    @commands.command(brief="Remove a command", help="Usage: !remove_command <name>")
    async def remove_command(self, ctx, name):
        name = name.lower()
        if name in self.commands:
            del self.commands[name]
            self.save_commands()
            await ctx.send(f"Command `{name}` removed.")
        else:
            await ctx.send(f"No command named `{name}` found.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        ctx = await self.client.get_context(message)

        # If the message is a command, ignore it
        if ctx.command is not None:
            return



        # Load prefix from prefixes.json
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        guild_id = str(message.guild.id) if message.guild else 'DM'
        prefix = prefixes.get(guild_id)  # Use 's!' as the default prefix

        if not message.content.startswith(prefix):
            return

        cmd_name = message.content[len(prefix):].strip().lower()

        if cmd_name in self.commands:
            response = self.commands[cmd_name]

            # Add support for more variables
            response = response.replace('{user}', message.author.name)
            response = response.replace('{time}', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Change time format

            # Handle server-specific variables
            if message.guild:
                response = response.replace('{channel}', message.channel.name)
                response = response.replace('{member_count}', str(message.guild.member_count))
                response = response.replace('{role_count}', str(len(message.guild.roles)))
                response = response.replace('{author_roles}', ', '.join([role.name for role in message.author.roles]))
                server_name = message.guild.name
            else:  # If the command is called from a DM
                response = response.replace('{channel}', 'DM')
                response = response.replace('{member_count}', 'N/A')
                response = response.replace('{role_count}', 'N/A')
                response = response.replace('{author_roles}', 'N/A')
                server_name = 'DM'

            response = response.replace('{server}', server_name)

            # Handle avatar differently
            if '{avatar}' in response:
                embed = discord.Embed()
                embed.set_image(url=str(message.author.avatar.url))
                await message.channel.send(response.replace('{avatar}', ''), embed=embed)
            else:
                await message.channel.send(response)

        await self.client.process_commands(message)


async def setup(client):
    await client.add_cog(CustomCommands(client))
