import discord
from discord.ext import commands

emojis = {}
def update_emojis():
    global embed1
    with open("emojis.txt") as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.split(" : ")
            name = line_split[0]
            emoji = line_split[1]
            username = line_split[2]
            title = "{} made by {}".format(name, username)
            emojis[title] = emoji
    embed1 = discord.Embed(title="Emojis", description="These are all of the emojis listed below", color=discord.Color.light_grey())
    for key, value in emojis.items():
        embed1.add_field(name=key, value=value, inline=False)

update_emojis()



class Emoji(commands.Cog):
    """This category holds emojis, a fun category used for recreational purposes"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def emoji(self, ctx, name = None, delete = False):
        global embed1
        """This command sends many emojis"""
        if(delete != False):
            await self.client.delete_message(ctx.message)
        sent = False
        if(name != None):
            name = name.lower()
        for key, value in emojis.items():
            if(name == key):
                await ctx.send(value)
                sent = True
        if(sent == False):
            await ctx.send("Sorry that is not one of the emojis listed. These are all of the emojis below", embed=embed1)

    @commands.command()
    async def add_emoji(self, ctx, emoji, *, name):
        """Add an emoji to the list of emojis. If you want to have a multi-space emoji, type it in quotes like this \": )\""""
        existing = False
        with open("emojis.txt") as f:
            for line in f.readlines():
                key = (line.split(" : "))[0]
                if(name.upper() == key.upper()):
                    await ctx.send("Sorry that name already exists")
                    existing = True
        if(existing == False):
            user = ctx.author.display_name
            with open("emojis.txt", "a") as f:
                f.write("\n{} : {} : {}".format(name.capitalize(), emoji, user))
            await ctx.send("An emoji has been added!")
            update_emojis()

def setup(client):
    client.add_cog(Emoji(client))
        
        
            
            
                
            
    
