import discord
from discord.ext import commands
import os
import logging


intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix = ".")
client.remove_command("help")

"""logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)"""

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

"""@client.command()
@commands.has_any_role("Moderator")
async def error_handling(ctx, switch):
    \"""A command that turns off or on error handling""\"
    if(switch.lower() == "on" or switch.lower() == "off"):
        with open('settings/error_handling.txt', 'w') as f:
            f.write(switch.lower())"""
            
@client.command()
@commands.has_any_role('Moderator')
async def person_by_id(ctx, num:int):
    """Gets a person by id"""
    await ctx.send(client.get_user(num).display_name)

@client.command()
@commands.has_any_role('Moderator')
async def message_by_id(ctx, num:int, specify=None):
    message = await ctx.channel.fetch_message(num)
    if(specify == None):
        await ctx.send(message.content)
    elif(specify == 'timestamp'):
        await ctx.send(message.created_at)
    elif(specify == 'channel'):
        await ctx.send(message.channel)

@client.command()
async def owner(ctx):
    await ctx.send('{}'.format(client.guilds[0].owner.display_name)
)        

@client.command()
@commands.has_any_role('Moderator', 'Admin', 'Tutor')
async def hi(ctx):
    emoji = discord.utils.get(client.guilds[0].emojis, name='saif')
    await emoji.delete()
    await ctx.send('hi')
    
for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
        client.load_extension("cogs.{}".format(filename[:-3]))
f = open('C:/Users/saifj/AppData/Local/Programs/Python/Python37/projects/saif projects/discord_bots/ycwbot_token.txt')
client.run(f"{f.readline()}")
