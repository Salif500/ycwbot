import discord
from discord.ext import commands
import os
import logging




client = commands.Bot(command_prefix = ".")
client.remove_command("help")

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.command()
async def add_suggestion(ctx, *, suggestion):
    """Use this to suggest a command"""
    with open("suggestions.txt", "a") as f:
        f.write("{} | {}\n".format(ctx.author.display_name, suggestion))
    user = client.get_user(308027015863336960)
    await user.send('Someone has added a suggestion')

@client.command()
@commands.has_any_role("Admin", "Moderator")
async def load(ctx, extension):
    """Loads the Cogs In. ADMIN ONLY"""
    client.load_extension("cogs.{}".format(extension))
    await ctx.send("Cog has been loaded in!")

@client.command()
@commands.has_any_role("Admin", "Moderator")
async def unload(ctx, extension):
    """Unloads the Cogs In. ADMIN ONLY"""
    client.unload_extension("cogs.{}".format(extension))
    await ctx.send("Cog has been unloaded!")

@client.command()
@commands.has_any_role("Admin", "Moderator")
async def check_logs(ctx):
    with open('discord.log', 'rb') as fp:
        await ctx.send('File:', file=discord.File(fp, 'discord_log.log'))

@client.command()
@commands.has_any_role("Moderator")
async def error_handling(ctx, switch):
    """A command that turns off or on error handling"""
    if(switch.lower() == "on" or switch.lower() == "off"):
        with open('settings/error_handling.txt', 'w') as f:
            f.write(switch.lower())


        

    




        

for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
        client.load_extension("cogs.{}".format(filename[:-3]))

client.run("NzA4NzQ1OTAyNjkyNjMwNTYw.Xrb5qw.zxf9Sv8wSgXO7-afWXmz5w81l40")
