import discord
from discord.ext import commands

class Waiting(commands.Cog):
    """This category is for people who are in the waiting list"""

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin", "Moderator")
    async def accept_all(self, ctx):
        """This command accepts all the people in the waiting list and turn them into students"""
        for role in self.client.guilds[0].roles:
            if(role.name.upper() == "WAITING"):
                roles = role.members
                for member in roles:
                    student = self.client.guilds[0].get_role(665958098627985450)
                    waiting = self.client.guilds[0].get_role(746862974295343216)
                    await member.remove_roles(waiting)
                    await member.add_roles(student)
                break

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin", "Moderator")
    async def accept(self, ctx, member: discord.Member):
        """This command accepts the certain person mentioned"""
        student = self.client.guilds[0].get_role(665958098627985450)
        waiting = self.client.guilds[0].get_role(746862974295343216)
        await member.remove_roles(waiting)
        await member.add_roles(student)
                
def setup(client):
    client.add_cog(Waiting(client))
