"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.
Written by Jared Newsom (AKA Jared M.F.)!"""
import discord
from discord.ext import commands
import math


class Help(commands.Cog):
    """Pretty self-explanatory"""
    def __init__(self,client):
        self.client = client

    
    

    def page_num(self, cog, num):
      counters = 0
      embeds = []
      cog_com = self.client.get_cog(cog).get_commands()
      if(self.client.get_cog(cog) == None):
        return None
      for i in range(num+1):
        halp=discord.Embed(title=cog+' Commands',description=self.client.cogs[cog].__doc__, color=discord.Color.blue())
        halp.set_footer(text='Page {} of {}'.format(i, int(math.ceil(len(cog_com)/5))))
        counters = 0
        for c in cog_com:
            counters += 1
            if(counters > (5*i)):
              break
            if(counters > 5*(i-1)):
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
        embeds.append(halp)
      return embeds
    


    @commands.command(pass_context=True)
    async def help(self,ctx,cog='____placeholder____',page_num:int=1):
      global halp
      """Prints help message"""
      if(cog == '____placeholder____'): 
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
          await ctx.message.author.send('',embed=halp)
          
      else:
        embeds = []
        found = False
        cog = cog.capitalize()
        for x in self.client.cogs:
            if x == cog:
                halp=discord.Embed(title=cog+' Commands',description=self.client.cogs[cog].__doc__, color=discord.Color.blue())
                embeds = self.page_num(cog, page_num)
                if(halp == None):
                  found == False
                else:
                  halp = embeds[page_num]
                  found = True
                
        if not found:
            """Reminds you if that cog doesn't exist."""
            halp = discord.Embed(title='Error!',description='What even is "'+cog+'"?',color=discord.Color.red())
        await ctx.message.author.send('',embed=halp)
        
def setup(client):
    client.add_cog(Help(client))
