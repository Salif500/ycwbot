import discord
from discord.ext import commands

class Settings(commands.Cog):
    """This category is for changing settings for the servers or for commands"""

    def __init__(self, client):
        self.client = client
                
    @commands.command(aliases=["change_filter", "add_filter"])
    @commands.has_any_role("Admin", "Moderator")
    async def change_filtering(self, ctx, *, word):
        """Add a word to filter explicit content"""
        await ctx.channel.purge(limit=1)
        with open("settings/filter_content.txt", "a") as f:
            f.write("\n" + str(word))
        await ctx.send("A word was added to the list of explicit content")

    @commands.command(aliases=["remove_filter"])
    @commands.has_any_role("Admin", "Moderator")
    async def delete_filter(self, ctx, *, word):
        """Delete a filter word from the list of filters"""
        await ctx.channel.purge(limit=1)
        with open("settings/filter_content.txt", "r") as f:
            lines = f.readlines()
        with open("settings/filter_content.txt", "w") as f:
            for line in lines:
                if(line.strip("\n") != word):
                    f.write(line)
        await ctx.send("A word has been deleted")

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def all_filters(self, ctx):
        """DM's An Admin that gives the list of explicit content(ADMIN ONLY)"""
        with open('settings/filter_content.txt') as f:
            lines = f.readlines()
            lines = map(str.strip, lines)
        await ctx.author.send((', and '.join(lines)))

    @commands.command()
    @commands.has_any_role("Moderator")
    async def error_handling(self, ctx, switch):
        """A command that turns off or on error handling"""
        if(switch.lower() == "on" or switch.lower() == "off"):
            with open('settings/error_handling.txt', 'w') as f:
                f.write(switch.lower())


  
            

    

    

    

    
    


def setup(client):
    client.add_cog(Settings(client))
    
        
