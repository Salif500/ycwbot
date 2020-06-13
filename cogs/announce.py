import discord
from discord.ext import commands

class Announcement(commands.Cog):
    """Its basically announcing text in a much cleaner way or just announcing text."""

    def __init__(self, client):
        self.client = client
        self.month = 0

    def number_to_month(self):
        """Converting a month number to a month name"""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.month = months[int(self.month) - 1]
            


    @commands.command(aliases=["ea", "assign"])
    @commands.has_any_role("Admin", "Moderator")
    async def embed_assign(self, ctx, channel, due, group,*, message):
        """Assign a thing at the end of the week as an embed by doing, .embed_assign <channel> <due date> <group> <message>"""
        
        if(channel == "assignments"):
            channel = 691079262475780157
        elif(channel == "bots"):
            channel = 708781411699654729
        date_list1 = str(ctx.message.created_at).split(" ")
        date_var = date_list1[0]
        date_list2 = date_var.split("-")
        year = date_list2[0]
        day = date_list2[2]
        self.month = date_list2[1]
        if(day[-1] == 1):
            day_suffix = "st"
        elif(day[-1] == 2):
            day_suffix = "nd"
        elif(day[-1] == 3):
            day_suffix = "rd"
        else:
            day_suffix = "th"
        if(day[0] == "0"):
            day = day[1:]
        if(group.lower() == "python"):
            color1 = discord.Color.gold()
        elif(group.lower() == "html"):
            color1 = discord.Color.red()
        messages = message.split("-")
        self.number_to_month()
        date = "{} {}{}, {}".format(self.month, day,day_suffix, year)
        embed1 = discord.Embed(title="{}".format(date), description="Homework for {} at {}".format(group.capitalize(),date), color=color1)
        if(group.lower() == "python"):
            for i in range(1, 4):
                embed1.add_field(name = "Homework for Python G{}".format(i), value=messages[i-1], inline=False)
                for guild in self.client.guilds:
                    for role in guild.roles:
                        if(str(role) == "Python G{}".format(i)):
                            await ctx.send("{}".format(role.mention))
        elif(group.lower() == "html"):
            for i in range(1,3):
                embed1.add_field(name = "Homework for HTML G{}".format(i), value=messages[i-1], inline=False)
                for guild in self.client.guilds:
                    for role in guild.roles:
                        if(str(role) == "HTML G{}".format(i)):
                            await ctx.send("{}".format(role.mention))
        embed1.add_field(name = "Due Date", value=due, inline=False)
        channel = self.client.get_channel(channel)     
        await channel.send('',embed=embed1)


def setup(client):
    client.add_cog(Announcement(client))
        
        
