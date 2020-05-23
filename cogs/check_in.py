import discord
from discord.ext import commands
import json

total = 0
class Check_In(commands.Cog):

    def __init__(self, client):
        """this is the init function for the class"""
        self.client = client
    
    @commands.command(aliases=["check", "Admin", "c", "checkin"])
    async def check_in(self, ctx):
        """this function checks in the user, while adding information to the database"""
        global total
        user = ctx.author
        list1 = str(user).split("#")
        name = list1[0]
        for role in user.roles:
            if(str(role) == "Python G1"):
                await ctx.send("Hello {}. Please Go To Advanced Group".format(name))
            elif(str(role) == "Python G2"):
                await ctx.send("Hello {}. Please Go To Intermediate Group".format(name))
            elif(str(role) == "Python G3"):
                await ctx.send("Hello {}. Please Go To Beginner Group".format(name))
            elif(str(role) == "HTML G1"):
                await ctx.send("Hello {}. Please Go To Beginner Group".format(name))
            elif(str(role) == "HTML G2"):
                await ctx.send("Hello {}. Please Go To Beginner Group".format(name))
        total += 1
                

    @commands.command(aliases=["clear_cache", "final"])
    @commands.has_any_role("Admin", "Moderator")
    async def clear_members(self, ctx):
        """:This function adds the total members joined to the database and clears the current variable"""
        global total
        date = str(ctx.message.created_at).split(" ")
        print(ctx.message.created_at)
        print(date)
        print(date[0])
        with open("total.txt", "a") as file_object:
            file_object.write("{}: {} members joined\n".format(date[0], total))
        total = 0
        await ctx.send("Data sent to Database")

    @commands.command(aliases=["find_data", "info"])
    @commands.has_any_role("Admin", "Moderator", "Tutor")
    #This checks if the user has the permission of Administrator
    async def data(self, ctx):
        global total
        """:this tells the user the members joined each week"""
        with open("total.txt") as file_object:
            lines = file_object.readlines()
            for line in lines:
                try:
                    await ctx.send("\n" + line)
                except:
                    print("Empty message")
                
def setup(client):
    client.add_cog(Check_In(client))
                
                               
    
        
                    
                
        
