import discord
from discord.ext import commands

class Submission(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Submission", "Add"])
    async def submit(self, ctx):
        name = discord.User.display_name
        await ctx.send(name)
        
            
            






def setup(client):
    client.add_cog(Submission(client))
