import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = ".")
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Some Codin"))    
    print("Bot is ready")
    

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




for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
        client.load_extension("cogs.{}".format(filename[:-3]))


client.run("NzA4NzQ1OTAyNjkyNjMwNTYw.Xrb5qw.zxf9Sv8wSgXO7-afWXmz5w81l40")
