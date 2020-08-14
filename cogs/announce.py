import discord
from discord.ext import commands

filename = "embeds.txt"
embeds = {}
with open(filename) as f:
    for line in f.readlines():
        line = line.split(" | ")
        user_id = line[0]
        embed_dict = line[1]
        embed_dict = eval(embed_dict)
        embeds[user_id] = embed_dict
        
def check_stop(check):
    if(check.content.lower() == "exit" or check.content.lower() == "stop"):
        return True
    else:
        return False        

class Announce(commands.Cog):
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
        """Assign a thing at the end of the week as an embed"""
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
        elif(group.lower() == "html"):
            for i in range(1,3):
                embed1.add_field(name = "Homework for HTML G{}".format(i), value=messages[i-1], inline=False)
        embed1.add_field(name = "Due Date", value=due, inline=False)
        channel = self.client.get_channel(channel)     
        await channel.send('',embed=embed1)

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def ping_students(self,ctx):
        channel = self.client.get_channel(691079262475780157)
        for guild in self.client.guilds:
            for role in guild.roles:
                if(str(role) == "Student"):
                    await channel.send("{}".format(role.mention))

    
            
    @commands.command()
    async def create_embed(self, ctx):
        """This function basically creates an embed that you can send. Type exit or stop to stop creating an embed."""
        worked = True
        title, desc, color, field_num, name, value, img, video, url = None, None, None, None, None, None, None, None, None
        await ctx.send("What is the title of your embed?")
        while title == None:
            title = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        if(check_stop(title) == True):
            await ctx.send("Your embed has stopped creating")
            return
        await ctx.send("What is the description of your embed?")
        while desc == None:
            desc = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        if(check_stop(desc) == True):
            await ctx.send("Your embed has stopped creating")
            return
        await ctx.send("What is the color of your embed?(Type an RGB tuple like (102, 234, 111) or None for none.)")
        while color == None:
            color = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        if(check_stop(color) == True):
            await ctx.send("Your embed has stopped creating")
            return
        await ctx.send("How many fields or sub titles do you want?")
        while field_num == None:
            field_num = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        if(check_stop(field_num) == True):
            await ctx.send("Your embed has stopped creating")
            return
        await ctx.send("Do you want an image? Type the url for yes or no for none.")
        while img == None:
            img = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        if(check_stop(img) == True):
            await ctx.send("Your embed has stopped creating")
            return
        await ctx.send("Do you want an video? Type the url for yes or no for none.")
        while video == None:
            video = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
        if(check_stop(video) == True):
            await ctx.send("Your embed has stopped creating")
            return
        if(color.content.upper() != "NONE" or "NO"):
            try:
                color = color.content.strip('()')
                color_list = color.split(",")
                num1 = color_list[0]
                num2 = color_list[1]
                num3 = color_list[2]
                color = discord.Color.from_rgb(int(num1), int(num2), int(num3))
            except:
                worked = False
                await ctx.send('You have sent a wrong color. Please Try Again')
        elif(color.content.upper() == "NONE"):
            color = None
        try:
            if(video.content.upper() != "NO" or video.content.upper() != "NONE"):
                url = video.content
            else:
                url = None
            embed1 = discord.Embed(title=title.content, description=desc.content, color=color, url=url)
            if(img.content.upper() != "NO" or img.content.upper() != "NONE"):
                embed1.set_image(url=img.content)
        except:
            worked = False
            await ctx.send("You have sent something wrong. Please Try Again")
        if(worked == True):
            try:
                field_num = int(field_num.content)
            except:
                await ctx.send("You have sent a wrong field number. Try again.")
            for i in range(field_num):
                name, value = None, None
                await ctx.send("What is the name of your field")
                while name == None:
                    name = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
                if(check_stop(title) == True):
                    await ctx.send("Your embed has stopped creating")
                    return
                await ctx.send("What is the description of your field")
                while value == None:
                    value = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
                if(check_stop(value) == True):
                    await ctx.send("Your embed has stopped creating")
                    return
                embed1.add_field(name=name.content,value=value.content,inline=False)
                embed1.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
            with open(filename) as f:
                lines = f.readlines()
                for line in lines:
                    liner = line.split(" | ")
                    if(ctx.author.id == int(liner[0])):
                        embed_dict = liner[1]
                        embed_dict_real = eval(embed_dict)
                        embed_num = 0
                        for element in embed_dict_real:
                            embed_num += 1
                        embed_num += 1
                        embed_dict_real["embed{}".format(embed_num)] = embed1.to_dict()
                    
            with open(filename, "w") as f:
                found = False
                for line in lines:
                    liner = line.split(" | ")
                    if(ctx.author.id == int(liner[0])):
                        found = True
                        f.write("{} | {}".format(str(ctx.author.id), embed_dict_real))
                    else:
                        f.write(line + "\n")
                if(found == False):
                    f.write("{} | {}".format(str(ctx.author.id), {"embed1" : embed1.to_dict()}))
            await ctx.send('everything has worked out. here is your embed', embed=embed1)

    @commands.command()
    async def display_embed(self, ctx, embed_num, channel = None):
        worked = False
        with open(filename) as f:
            for line in f.readlines():
                line = line.split(" | ")
                user_id = line[0]
                embed_dict = line[1]
                embed_dict = eval(embed_dict)
                embeds[user_id] = embed_dict
        try:
            embed_dictionary = embeds[str(ctx.author.id)]
            worked = True
        except:
            await ctx.send("Sorry, but you dont have any embeds.")
        if(worked == True):
            try:
                embed = embed_dictionary["embed{}".format(embed_num)]
            except:
                await ctx.send('Yo. Why you send some garbo numbers of embeds that ya dont even have.')
            embed = discord.Embed.from_dict(embed)
            if(channel == None):
                await ctx.send("", embed=embed)
            elif(channel != None):
                for guild in self.client.guilds:
                    try:
                        channel = discord.utils.get(guild.text_channels, name=channel)
                    except:
                        await ctx.send('You have sent a wrong channel name')
                await channel.send('',embed=embed)
            
            
        

        
                
                
                    
                        
                        
                        
            
                
            
                    
                
                
            
                            
                    
                
                
            
    
                
                
                    
        


def setup(client):
    client.add_cog(Announce(client))
        
        
