import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
@commands.has_role("Admin")
async def load(ctx, extension):
    client.load_extension("cogs.{}".format(extension))

@client.command()
@commands.has_role("Admin")
async def unload(ctx, extension):
    client.unload_extension("cogs.{}".format(extension))



for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
        client.load_extension("cogs.{}".format(filename[:-3]))


client.run("NzA4NzQ1OTAyNjkyNjMwNTYw.Xrb5qw.zxf9Sv8wSgXO7-afWXmz5w81l40")
