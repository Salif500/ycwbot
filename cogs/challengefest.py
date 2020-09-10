import discord
from discord.ext import commands
import json

class Challengefest(commands.Cog):
    """All ChallengeFest commands located here"""
    #Change docstring to link to our challengefest page
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role('Admin', 'Moderator')
    async def cfreseteverything(self, ctx):
        """Resets everything. DO NOT USE. Just DONT"""
        await ctx.send('Do you want to reset everything?')
        reply = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
        if(reply.content.lower() == 'yes'):
            scores = {}
            for student in self.client.guilds[0].get_role(665958098627985450).members:
              scores[student.id] = {'name' : f'{student.display_name}', 'current_points' : 0, 'total_points' : 0, 'completed_challenges' : []}      
            f = open('cf/cfscores.json', 'w', encoding='utf8')
            json.dump(scores, f, indent=6)
            f.close()
    

    
                

                            
            
    
            

def setup(client):
    client.add_cog(Challengefest(client))
