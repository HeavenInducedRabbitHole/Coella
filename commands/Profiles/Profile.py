import discord
from discord.ext import commands
import json


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.admin_ids = [942894031329955850]  # Add the IDs of the users who can give badges

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        if str(member.id) not in users:
            user = {
                "Username": member.name,
                "Bio": "This is a bio",
                "EmbedColor": "FFFFFF",
                "ProfileIcon": str(member.avatar.url),
                "Status": "I'm new here!",
                "Background": "This is my background",
                "Badges": [],
                "SocialLinks": {},
            }

            users[str(member.id)] = user

            with open("jsons/users.json", "w") as f:
                json.dump(users, f)
        else:
            user = users[str(member.id)]

        # Reload users from file after potentially updating it
        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        user = users.get(str(member.id), None)
        if user is None:
            await ctx.send("An error occurred while loading the user profile.")
            return

        embed = discord.Embed(title=f"{member.name}'s Profile",
                              description=user["Bio"],
                              color=int(user["EmbedColor"], 16))

        embed.set_thumbnail(url=user["ProfileIcon"])
        embed.set_image(url=user["Background"])

        embed.add_field(name="Status", value=user["Status"], inline=True)

        badges = ' '.join(
            [str(self.client.get_emoji(id)) for id in user["Badges"] if self.client.get_emoji(id) is not None])
        if badges:
            embed.add_field(name="Badges", value=badges, inline=False)
        else:
            embed.add_field(name="Badges", value="No Badges", inline=False)

        for social in user["SocialLinks"]:
            embed.add_field(name=social, value=user["SocialLinks"][social], inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def give_badge(self, ctx, member: discord.Member, badge_id: int):
        if ctx.author.id not in self.admin_ids:
            await ctx.send("You don't have permission to use this command.")
            return

        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        if str(member.id) not in users:
            await ctx.send("The specified user does not have a profile.")
            return

        users[str(member.id)]["Badges"].append(badge_id)

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)

        await ctx.send(f"Badge has been given to {member.name}")

    @commands.command()
    async def remove_badge(self, ctx, member: discord.Member, badge_id: int):
        if ctx.author.id not in self.admin_ids:
            await ctx.send("You don't have permission to use this command.")
            return

        with open("jsons/users.json", "r") as f:
            users = json.load(f)

        if str(member.id) not in users:
            await ctx.send("The specified user does not have a profile.")
            return

        try:
            users[str(member.id)]["Badges"].remove(badge_id)
        except ValueError:
            await ctx.send("The specified badge does not exist for this user.")
            return

        with open("jsons/users.json", "w") as f:
            json.dump(users, f)

        await ctx.send(f"Badge has been removed from {member.name}")


async def setup(client):
    await client.add_cog(Profile(client))
