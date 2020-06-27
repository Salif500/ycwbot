import discord
from discord.abc import PrivateChannel
from discord.ext import commands
import os
import time
import datetime

client = commands.Bot(command_prefix = ".")
client.remove_command("help")

month = 0

all_embed_settings = {}

def update_link_dict():
    with open("settings/embed_links.txt") as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.split(" : ")
            key = line_split[0]
            value = line_split[1]
            all_embed_settings[key] = value

update_link_dict()
        

        
@client.command()
@commands.has_any_role("Admin", "Moderator")
async def load(ctx, extension):
    """Loads the Cogs In. If you're a student, don't worry about it. Admins only"""
    client.load_extension("cogs.{}".format(extension))
    await ctx.send("Cog has been loaded in!")

@client.command()
@commands.has_any_role("Admin", "Moderator")
async def unload(ctx, extension):
    """Unloads the Cogs In. If you're a student, don't worry about it. Admins only"""
    client.unload_extension("cogs.{}".format(extension))
    await ctx.send("Cog has been unloaded!")

@client.command()
async def emoji(ctx, emoji = None):
    """This command sends many emojis"""
    global pos
    if(emoji == None):
        await ctx.send("\ \_ :grinning: _/\n        |\n       /\\")
    elif(emoji == "1"):
        await ctx.send("Nothing here yet")

        

    else:
        await ctx.send("No such number of this emoji")

@client.command()
async def embed_settings(ctx, setting):
    """Set a setting for if you automattically want to turn links into embeds"""
    if(setting.capitalize() == "True" or "False"):
        user_id = ctx.author.id
        with open("settings/embed_links.txt", "w") as f:
            f.write("{} : {}".format(user_id, str(setting)))
        update_link_dict()
        await ctx.send("Setting has been set to {}".format(setting))
    
            



    
    




for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
        client.load_extension("cogs.{}".format(filename[:-3]))

client.run("NzA4NzQ1OTAyNjkyNjMwNTYw.Xrb5qw.zxf9Sv8wSgXO7-afWXmz5w81l40")
