import discord
from discord.ext import commands, tasks


class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reminders = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("Reminder is ready")
        self.check_reminders.start()  # Start the background task

    @commands.command()
    async def remindme(self, ctx, time: int, *, message: str):
        reminder = {
            'time': time * 60,  # convert time to seconds
            'message': message,
            'ctx': ctx,
            'user_id': ctx.author.id
        }
        self.reminders.append(reminder)
        embed = discord.Embed(title="Reminder is set!",
                              description=f"Reminder set for {time} minute(s) from now!",
                              color=discord.Color.teal())
        await ctx.send(embed=embed)

    @tasks.loop(seconds=1)  # Loop every second
    async def check_reminders(self):
        for reminder in self.reminders:
            if reminder['time'] <= 0:
                ctx = reminder['ctx']

                embed = discord.Embed(title="Reminder!",
                                      description=f"<@{reminder['user_id']}> Your reminder: {reminder['message']}",
                                      color=discord.Color.teal())
                await ctx.send(embed=embed)
                self.reminders.remove(reminder)
            else:
                reminder['time'] -= 1


async def setup(client):
    await client.add_cog(Reminder(client))
