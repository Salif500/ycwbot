import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Some Codin"))    
    print("Bot is ready")


@client.command()
@commands.has_any_role("Admin", "Moderator")
async def load(ctx, extension):
    client.load_extension("cogs.{}".format(extension))

@client.command()
@commands.has_any_role("Admin", "Moderator")
async def unload(ctx, extension):
    client.unload_extension("cogs.{}".format(extension))

@client.command(aliases=["move_to_end", "end", "workshop_end", "e"])
@commands.has_any_role("Admin", "Moderator")
async def move_end(ctx, *, channel: discord.VoiceChannel):
    print(channel)
    for guild in client.guilds:
        for member in guild.members:
            if(member.status != discord.Status.offline):
                try:
                    await member.move_to(channel)
                except:
                    print("{} is not connected\n".format(member))

            
        



for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
        client.load_extension("cogs.{}".format(filename[:-3]))


client.run("NzA4NzQ1OTAyNjkyNjMwNTYw.Xrb5qw.zxf9Sv8wSgXO7-afWXmz5w81l40")
