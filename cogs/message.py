import discord
from discord.ext import commands
import datetime

class Message(commands.Cog):
    """This category is for managing messages"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def user_messages(self, ctx, user: discord.Member, channel : discord.TextChannel, date_begin, date_stop=None):
        """This command checks all messages given by a user in a channel within a certain date"""
        worked, work = False, True
        if(work == False):
            await ctx.send('No Member Found')
        else:
            try:
                monthb, dayb, yearb = map(int, date_begin.split('/'))
                try:
                    months, days, years = map(int, date_stop.split('/'))
                    bef = datetime.datetime(years, months, days)
                except:
                    bef = None
                    date_stop = 'current'
                worked = True
            except:
                await ctx.send('You have entered a wrong date start or stop')
            if(worked == True):
                embed = discord.Embed(title='All Messages Sent By {}'.format(user.display_name), description='Dates from {} to {}'.format(date_begin, date_stop), color=discord.Color.teal())
                embed.set_author(name=user.display_name, icon_url=user.avatar_url)
                async for message in channel.history(after=datetime.datetime(yearb, monthb, dayb), before=bef, oldest_first=True):
                    if(message.author == user):
                        month, day, year = map(str, str(message.created_at).split(' ')[0].split('-'))
                        hour, minute, second = map(str, str(message.created_at).split(' ')[1].split(':'))
                        second = second.split('.')[0]
                        hour = str(int(hour) + 5)
                        if(hour > '12'):
                            hour = str(int(hour) - 12)
                            ti = 'P'
                            if(hour > '12'):
                                hour = str(int(hour) - 12)
                                ti = 'A'
                        else:
                            ti = 'A'
                        embed.add_field(name=message.content, value='{}/{}/{} {}:{}:{} {}M'.format(month, day, year, abs(hour), minute, second, ti), inline=False)
                await ctx.author.send('', embed=embed)
def setup(client):
    client.add_cog(Message(client))
