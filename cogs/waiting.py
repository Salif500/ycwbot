import discord
from discord.ext import commands
import json
class Waiting(commands.Cog):
    """Commands for handling Waiting Room(ADMIN ONLY)"""

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin", "Moderator")
    async def accept_all(self, ctx):
        """Accepts ALL members in waiting room(ADMINS ONLY)"""
        fin = open(f'dynamic/{ctx.message.guild.id}/cf/cfscores.json', encoding='utf8')
        scores = json.load(fin)
        fin.close()
        for student in self.client.guilds[0].get_role(746862974295343216).members:
            scores[student.id] = {'name' : f'{student.display_name}', 'current_points' : 0, 'total_points' : 0, 'QOTD' : 0, 'completed_challenges' : []}      
        f = open(f'dynamic/{ctx.message.guild.id}/cf/cfscores.json', 'w', encoding='utf8')
        json.dump(scores, f, indent=6)
        f.close()    
        for role in self.client.guilds[0].roles:
            if(role.name.upper() == "WAITING"):
                roles = role.members
                for member in roles:
                    student_role = self.client.guilds[0].get_role(665958098627985450)
                    waiting = self.client.guilds[0].get_role(746862974295343216)
                    await member.remove_roles(waiting)
                    await member.add_roles(student_role)
                break

    @commands.command(pass_context=True)
    @commands.has_any_role("Admin", "Moderator")
    async def accept(self, ctx, student: discord.Member):
        """Accepts a CERTAIN member in waiting room(ADMINS ONLY)"""
        fin = open(f'dynamic/{ctx.message.guild.id}/cf/cfscores.json', encoding='utf8')
        scores = json.load(fin)
        fin.close()
        scores[student.id] = {'name' : f'{student.display_name}', 'current_points' : 0, 'total_points' : 0, 'QOTD' : 0, 'completed_challenges' : []}
        f = open(f'dynamic/{ctx.message.guild.id}/cf/cfscores.json', 'w', encoding='utf8')
        json.dump(scores, f, indent=6)
        f.close()
        student_role = self.client.guilds[0].get_role(665958098627985450)
        waiting = self.client.guilds[0].get_role(746862974295343216)
        await student.remove_roles(waiting)
        await student.add_roles(student_role)
                
def setup(client):
    client.add_cog(Waiting(client))
