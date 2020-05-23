import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = ".")
@client.remove_command("Help")






@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Some Codin"))    
    print("Bot is ready")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Help", type="rich", description="")
    



@client.command()
@commands.has_any_role("Admin", "Moderator")
async def load(ctx, extension):
    client.load_extension("cogs.{}".format(extension))

@client.command()
@commands.has_any_role("Admin", "Moderator")
async def unload(ctx, extension):
    client.unload_extension("cogs.{}".format(extension))

@client.command(aliases=["move_everyone", "move_all_members", "move", "m"])
@commands.has_any_role("Admin", "Moderator")
async def move_all(ctx, *, channel: discord.VoiceChannel):
    for guild in client.guilds:
        for member in guild.members:
            if(member.status != discord.Status.offline):
                try:
                    await member.move_to(channel)
                except:
                    print("{} is not connected\n".format(member))

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.yellow()
        )
    embed.set_author(name="Help")
    embed.add_field(name=".help", value="Returns this message!", inline=False)
    embed.add_field(name=".move_all", value="Aliases are, move_everyone, move_all_members, move, and m. Give it a channel and it will move all members in voice to that specific channel.", inline=False)

    await ctx.send(embed=embed)
    
    



    

for filename in os.listdir("./cogs"):
    if(filename.endswith(".py")):
        client.load_extension("cogs.{}".format(filename[:-3]))


client.run("NzA4NzQ1OTAyNjkyNjMwNTYw.Xrb5qw.zxf9Sv8wSgXO7-afWXmz5w81l40")
