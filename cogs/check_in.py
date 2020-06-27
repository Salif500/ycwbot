import discord
from discord.ext import commands
import json

total = 0
class Checkin(commands.Cog):
    """This is the check in category for commands that are related to the beginning of the workshop"""

    def __init__(self, client):
        """this is the init function for the class"""
        self.client = client
        self.month = 0
    
    @commands.command(aliases=["check", "Admin", "c", "check_in"])
    async def checkin(self, ctx):
        """this function checks in the user, while adding information to the database"""
        global total
        name = ctx.author.display_name
        user = ctx.author
        for role in user.roles:
            if(str(role) == "Python G1"):
                await ctx.send("Hello {}. Please Go To Advanced Group".format(name))
            elif(str(role) == "Python G2"):
                await ctx.send("Hello {}. Please Go To Intermediate Group".format(name))
            elif(str(role) == "Python G3"):
                await ctx.send("Hello {}. Please Go To Beginner Group".format(name))
            elif(str(role) == "HTML G1"):
                await ctx.send("Hello {}. Please Go To Intermediate Group".format(name))
            elif(str(role) == "HTML G2"):
                await ctx.send("Hello {}. Please Go To Beginner Group".format(name))
        total += 1
        
    def number_to_month(self):
        """Converting a month number to a month name"""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.month = months[int(self.month) - 1]
            
                

    @commands.command(aliases=["clear_cache", "final"])
    @commands.has_any_role("Admin", "Moderator")
    async def clear_members(self, ctx):
        """This function adds the total members joined to the database and clears the current variable. Admins Only"""
        global total
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
        self.number_to_month()
        with open("total.txt", "a") as file_object:
            file_object.write("{} {}{}, {}: {} members joined\n".format(self.month, day,day_suffix, year, total))
        total = 0
        await ctx.send("Data sent to Database")

    @commands.command(aliases=["find_data", "info"])
    @commands.has_any_role("Admin", "Moderator", "Tutor")
    #This checks if the user has the permission of Administrator
    async def data(self, ctx):
        """this tells the user the members joined each week. Admins and Tutors Only"""
        global total
        with open("total.txt") as file_object:
            lines = file_object.readlines()
            for line in lines:
                try:
                    await ctx.send("\n" + line)
                except:
                    print("Empty message")
                
def setup(client):
    client.add_cog(Checkin(client))
                
                               
    
        
                    
                
        
