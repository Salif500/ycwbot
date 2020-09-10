import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cogs/ycw-bot-042839cc90aa.json', scope)

gc = gspread.authorize(credentials)
wks = gc.open('YCW Submissions Form (Responses)').sheet1

class Submissions(commands.Cog):
    """Submissions cog"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role('Moderator', 'Admin')            
    async def responses(self, ctx):
        """Sends all data in a formatted way"""
        counter = 0
        brek = False
        sdict = wks.get_all_records()
        embed1 = discord.Embed(title='Responses', color = discord.Color.green())
        for element in sdict:
            for key, value in element.items():
                element[key] = value.rstrip().lstrip()
                if(value.rstrip().lstrip() == ''):
                    counter += 1
                if(counter == len(element)):
                    brek = True
                    break
            if(brek == True):
                break
            embed1.add_field(name='{} sent at {}'.format(element['Enter ONLY first name. Enter it EXACTLY like you do for all other submissions'], element['Timestamp']), value='Warmup/Project: {}\nLanguage: {}\nLink: {}'.format(element['Is this a warmup or a project?'], element['Which language are you submitting this for?'], element['Enter the repl.it join link(for projects) or share link(for warmups).']), inline=False)
        await ctx.send('', embed=embed1)

def setup(client):
    client.add_cog(Submissions(client))
