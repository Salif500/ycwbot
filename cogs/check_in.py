import discord
from discord.ext import commands


total = 0
class Checkin(commands.Cog):
    """Commands to use at the beginning of a workshop"""

    def __init__(self, client):
        """this is the init function for the class"""
        self.client = client
        self.month = 0
    
    @commands.command(aliases=["check", "Admin", "c", "check_in"])
    async def checkin(self, ctx):
        """Use this in the #checkin channel before every workshop"""
        found, found_role = False, False
        name = ctx.author.display_name
        user = ctx.author
        for role in user.roles:
            if(str(role) == "Python"):
                await ctx.send("Hello {}. Please Go To Python".format(name))
                found_role = True
            elif(str(role) == "Scratch"):
                await ctx.send("Hello {}. Please Go To Scratch".format(name))
                found_role = True
            elif(str(role) == "HTML"):
                await ctx.send("Hello {}. Please Go To HTML".format(name))
                found_role = True
        if(found_role == False):
            await ctx.send("Hello {}. Please Go to Living Room".format(name))
        created_at = str(ctx.message.created_at)
        with open("total.txt") as f:
            lines = f.readlines()
        large_date = created_at.split(" ")
        large_date = large_date[0]
        with open("total.txt", "w") as f:
            for line in lines:
                line_split = line.split(": ")
                if(line_split[0] == str(large_date)):
                    real_line = line.split(": ")
                    real_line = real_line[1]
                    real_line_list = real_line.split(" ")
                    real_number = real_line_list[0]
                    real_number = int(real_number) + 1
                    f.write("{}: {} people joined\n".format(large_date, real_number))
                    found = True
                else:
                    f.write(line)
            if(found == False):
                f.write("{}: 1 people joined\n".format(large_date))
                
        
        
    def number_to_month(self):
        """Converting a month number to a month name"""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.month = months[int(self.month) - 1]
            
                


    @commands.command(aliases=["find_data", "info"])
    @commands.has_any_role("Admin", "Moderator", "Tutor")
    #This checks if the user has the permission of Administrator
    async def data(self, ctx):
        """Prints all checkin data(ADMINS ONLY)"""
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
                
                               
    
        
                    
                
        
