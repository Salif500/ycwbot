"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.
Written by Jared Newsom (AKA Jared M.F.)!"""
import discord
from discord.ext import commands


class Help(commands.Cog):
    """Its just literally this category of help"""
    def __init__(self,client):
        self.client = client




    @commands.command(pass_context=True)
    async def help(self,ctx,*cog):
        """Its literally this command."""
        if not cog:
            await ctx.send("You've been sent the help command!")
            """Cog listing.  What more?"""
            halp=discord.Embed(title='All Commands in this Bot',
                               description='Use `.help *category*` to find out more about them!',
                               color=discord.Color.gold())
            cogs_desc = ''
            for x in self.client.cogs:
                cogs_desc += ('{} - {}'.format(x,self.client.cogs[x].__doc__)+'\n\n')
            halp.add_field(name='Categories',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
            cmds_desc = ''
            for y in self.client.walk_commands():
                if not y.cog_name and not y.hidden:
                    cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n\n')
            halp.add_field(name='Miscellaneous',value=cmds_desc[0:len(cmds_desc)-1],inline=False)
            await ctx.message.author.send('',embed=halp)
        else:
            """Helps me remind you if you pass too many args."""
            if len(cog) > 1:
                halp = discord.Embed(title='Error!',description='That is way too many categories!',color=discord.Color.red())
                await ctx.message.author.send('',embed=halp)
            else:
                """Command listing within a cog."""
                found = False
                for x in self.client.cogs:
                    for y in cog:
                        if x == y:
                            halp=discord.Embed(title=cog[0]+' Commands',description=self.client.cogs[cog[0]].__doc__, color=discord.Color.blue())
                            for c in self.client.get_cog(y).get_commands():
                                if not c.hidden:
                                    halp.add_field(name=c.name,value=c.help,inline=False)
                            found = True
                if not found:
                    """Reminds you if that cog doesn't exist."""
                    halp = discord.Embed(title='Error!',description='What even is "'+cog[0]+'"?',color=discord.Color.red())
                await ctx.message.author.send('',embed=halp)
        
def setup(client):
    client.add_cog(Help(client))
