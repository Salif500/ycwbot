import discord
from discord.ext import commands
import json


class Check_In(commands.Cog):

    def __init__(self, client):
        """:this is the init function for the class"""
        self.client = client
        total = 0
        
        

    @commands.command(aliases=["check", "Admin", "c", "checkin"])
    async def check_in(self, ctx):
        """:this function checks in the user, while adding information to the database"""
        user_id = ctx.message.author.id
        with open("check_in.txt") as file_object:
            array = file_object.readlines()
            await ctx.send(str(len(array)))
            user_id2 = array[0]
            group2 = array[1]
            if(user_id == user_id2):
                await ctx.send("Hello! Your Group is {}.".format(group2))
                total += 1

    @commands.command(aliases=["workshop_end", "end_workshop"])
    @commands.has_role("Admin")
    async def end(self, date):
        """:This function adds the total members joined to the database and clears the current variable"""
        with open(filename2, "a") as file_object:
            file_object.write("{}:{} members joined\n".format(date, total))
        total = 0

    @commands.command(aliases=["find_data", "info"])
    @commands.has_role("Admin")
    #This checks if the user has the permission of Administrator
    async def data(self, ctx):
        """:this tells the user the members joined each week"""
        with open("total.txt") as file_object:
            for line in file_object:
                await ctx.send(file_object.readline())
                
    @commands.command()
    async def test(self, ctx):
      await ctx.send("{}".format(ctx.message.author.id))

def setup(client):
    client.add_cog(Check_In(client))
                
                               
    
        
                    
                
        
