import discord
import os
from discord.ext import commands

units_py = {}
units_html = {}
    
class Video(commands.Cog):
    """This is the Video category for accessing any videos that you want through discord."""

    def __init__(self, client):
        self.client = client

    def update_files_py(self):
        for filename in os.listdir("./units_py"):
            with open("units_py/{}".format(filename)) as f:
                unit = {}
                unit_name = str(filename[:-4])
                lines = f.readlines()
            for line in lines:
                video = line.split(" : ")
                name = video[0]
                link = video[1]
                
                unit[name] = link
            units_py[unit_name] = unit

    def update_files_html(self):
        for filename in os.listdir("./units_html"):
            with open("units_html/{}".format(filename)) as f:
                unit = {}
                unit_name = str(filename[:-4])
                lines = f.readlines()
            for line in lines:
                video = line.split(" : ")
                name = video[0]
                link = video[1]

                unit[name] = link
            units_html[unit_name] = unit    
            
    @commands.command(aliases=["get_all_vids", "list_vid", "all_videos"])
    async def all_vids(self, ctx, group, unit_num):
        """Get all the videos of the given group"""
        user = ctx.author
        self.update_files_py()
        self.update_files_html()
        if(group.lower() == "python"):
            try:
                dictionary = units_py["unit{}".format(unit_num)]
                embed1 = discord.Embed(title="Unit {} Videos".format(unit_num), description="All videos in unit {}, the list of videos might be outdated.".format(unit_num), color=discord.Color.gold())
                for key, value1 in dictionary.items():
                    embed1.add_field(name=key, value=value1, inline=False)
                await user.send('', embed=embed1)
            except:
                await ctx.send("That unit isn't there yet, or you misspelled it")
        elif(group.lower() == "html"):
            try:
                dictionary = units_html["unit{}".format(unit_num)]
                embed1 = discord.Embed(title="Unit {} Videos".format(unit_num), description="All videos in unit {}, the list of videos might be outdated.".format(unit_num), color=discord.Color.red())
                for key, value1 in dictionary.items():
                    embed1.add_field(name=key, value=value1, inline=False)
                await user.send('', embed=embed1)
            except:
                await ctx.send("That unit isn't there yet, or you misspelled it")
        else:
            await ctx.send("Sorry that group isn't there.")

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def add_vid(self, ctx, group, unit_num, link, *, video):
        """This command is to add a video to a unit, or create a unit if its non existing. Parameters: <group> <unit_num> <link> <video>"""
        global existing
        existing = False
        if(group.lower() == "python"):
            for filename in os.listdir("./units_py"):
                if("unit{}.txt".format(unit_num) == str(filename)):
                    existing = True
            if existing:
                with open("units_py/unit{}.txt".format(unit_num), "a") as f:
                    f.write("{} : {}\n".format(video, link))   
            elif not existing:
                print('Not existing')
                with open("units_py/unit{}.txt".format(unit_num), "x") as f:
                    f.write("{} : {}\n".format(video, link))
            await ctx.send("A new video has been added")
            self.update_files_py()
        elif(group.lower() == "html"):
            for filename in os.listdir("./units_html"):
                if("unit{}.txt".format(unit_num) == str(filename)):
                    existing = True
            if existing:
                with open("units_html/unit{}.txt".format(unit_num), "a") as f:
                    f.write("{} : {}\n".format(video, link))   
            elif not existing:
                print('Not existing')
                with open("units_html/unit{}.txt".format(unit_num), "w") as f:
                    f.write("{} : {}\n".format(video, link))
            await ctx.send("A new video has been added")
            self.update_files_py()
                    
        


def setup(client):
    client.add_cog(Video(client))

