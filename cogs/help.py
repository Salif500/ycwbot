"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.
Written by Jared Newsom (AKA Jared M.F.)!"""
import discord
from discord.ext import commands
import inspect


class Help(commands.Cog):
    """Pretty self-explanatory"""
    def __init__(self,client):
        self.client = client




    @commands.command(pass_context=True)
    async def help(self,ctx,cog='bobthebobthebob',page_num:int=None):
        """Prints help message"""
        if(cog == 'bobthebobthebob'): 
            """Cog listing.  What more?"""
            halp=discord.Embed(title='All Commands in this Bot',
                               description='Use `.help *category*` to find out more about them!',
                               color=discord.Color.gold())
            cogs_desc = ''
            for x in self.client.cogs:
                if(x == "Events"):
                    continue
                cogs_desc += ('**{}** - {}'.format(x,self.client.cogs[x].__doc__)+'\n')
            halp.add_field(name='__Categories:__',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
            #Not In Use
            """
            cmds_desc = ''
            for y in self.client.walk_commands():
                if not y.cog_name and not y.hidden:
                    brackets_left = " <"
                    brackets_right = ">"
                    command = self.client.get_command(str(y))
                    command_aliases = command.aliases
                    command_params_dict = command.clean_params
                    command_params = list(command_params_dict)
                    if not command_params:
                        command_params = ["None"]
                        brackets_left = " "
                        brackets_right = ""
                    if not command_aliases:
                       command_aliases = ["None"]                         
                    cmds_desc += ('{} - {}'.format(y.name,y.help)+'\nParameters:{}{}{}\nAliases: {}\n\n'.format(brackets_left, ('> <'.join(command_params)),brackets_right,(', '.join(command_aliases))))
            halp.add_field(name='Miscellaneous',value=cmds_desc[0:len(cmds_desc)-1],inline=False)"""
            await ctx.message.author.send('',embed=halp)
            
        else:
            """Helps me remind you if you pass too many args.\"""
            page_num_wrong = False
            if len(cog) > 1:
                halp = discord.Embed(title='Error!',description='That is way too many categories!',color=discord.Color.red())
                await ctx.message.author.send('',embed=halp)"""
            """Command listing within a cog."""
            found = False
            cog = cog.capitalize()
            for x in self.client.cogs:
                if x == cog:
                    halp=discord.Embed(title=cog+' Commands',description=self.client.cogs[cog].__doc__, color=discord.Color.blue())
                    if len(self.client.get_cog(cog).get_commands()) > 5:
                        counters = 0
                        if(page_num == 1 or page_num == None):
                            halp.set_footer(text='Page 1 of 2')
                            for c in self.client.get_cog(cog).get_commands():
                                counters += 1
                                if not c.hidden:
                                    brackets_left = " <"
                                    brackets_right = ">"
                                    cog_command = self.client.get_command(str(c))
                                    cog_command_aliases = cog_command.aliases
                                    cog_command_params_dict = cog_command.clean_params
                                    cog_command_params = list(cog_command_params_dict)
                                    if not cog_command_params:
                                        cog_command_params = ["None"]
                                        brackets_left = " "
                                        brackets_right = ""
                                    if not cog_command_aliases:
                                        cog_command_aliases = ["None"]
                                    halp.add_field(name=c.name,value=str(c.help) + "\nParameters:{}{}{}\nAliases: {}".format(brackets_left, ('> <'.join(cog_command_params)),brackets_right,(', '.join(cog_command_aliases))),inline=False)
                                if(counters == 5):
                                    break
                        elif(page_num == 2):
                            halp.set_footer(text='Page 2 of 2')
                            for c in self.client.get_cog(cog).get_commands():
                                counters += 1
                                if(counters > 5):
                                    if not c.hidden:
                                        brackets_left = " <"
                                        brackets_right = ">"
                                        cog_command = self.client.get_command(str(c))
                                        cog_command_aliases = cog_command.aliases
                                        cog_command_params_dict = cog_command.clean_params
                                        cog_command_params = list(cog_command_params_dict)
                                        if not cog_command_params:
                                            cog_command_params = ["None"]
                                            brackets_left = " "
                                            brackets_right = ""
                                        if not cog_command_aliases:
                                            cog_command_aliases = ["None"]
                                        halp.add_field(name=c.name,value=str(c.help) + "\nParameters:{}{}{}\nAliases: {}".format(brackets_left, ('> <'.join(cog_command_params)),brackets_right,(', '.join(cog_command_aliases))),inline=False)
                        else:
                            page_num_wrong = True
                            await ctx.send('Ya Got the Page Number Wrong')


                    else:
                        for c in self.client.get_cog(cog).get_commands():
                            if not c.hidden:
                                brackets_left = " <"
                                brackets_right = ">"
                                cog_command = self.client.get_command(str(c))
                                cog_command_aliases = cog_command.aliases
                                cog_command_params_dict = cog_command.clean_params
                                cog_command_params = list(cog_command_params_dict)
                                if not cog_command_params:
                                    cog_command_params = ["None"]
                                    brackets_left = " "
                                    brackets_right = ""
                                if not cog_command_aliases:
                                    cog_command_aliases = ["None"]
                                halp.add_field(name=c.name,value=str(c.help) + "\nParameters:{}{}{}\nAliases: {}".format(brackets_left, ('> <'.join(cog_command_params)),brackets_right,(', '.join(cog_command_aliases))),inline=False)
                    found = True
            if not found:
                """Reminds you if that cog doesn't exist."""
                halp = discord.Embed(title='Error!',description='What even is "'+cog+'"?',color=discord.Color.red())
            await ctx.message.author.send('',embed=halp)
        
def setup(client):
    client.add_cog(Help(client))
