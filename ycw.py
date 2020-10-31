import discord, os, keep_alive, json
from discord.ext import commands



keep_alive.keep_alive()

'''
1.)Find each instance of opening dynamic folder in CF and Poll
	a.)Replace it with dynamic/{}_{} and add .format(ctx.message.guild.name)
'''

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix = ".")
client.remove_command("help")

"""logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)"""




@client.event
async def on_guild_join(guild):
  """Triggers when the bot joins another guild"""
  print('Bot is joined')
  print(guild.name)
  parent_dir = os.getcwd()
  path = os.path.join('{}/dynamic'.format(parent_dir), str(guild.id))
  os.mkdir(path)
  os.mkdir(os.path.join(path, 'cf'))
  os.mkdir(os.path.join(path, 'polls')) 
  f = open(f'dynamic/{str(guild.id)}/cf/cfscores.json', 'w')
  f.write('{}')
  f.close()
  f = open(f'dynamic/{str(guild.id)}/cf/cfchal.json', 'w')
  f.write('{}')
  f.close()
  f = open(f'dynamic/{str(guild.id)}/polls/polls.json', 'w')
  f.write('{}')
  f.close()
  fin = open('name.json')
  names = json.load(fin)
  fin.close()
  fout = open('name.json', 'w')
  names[guild.name] = guild.id
  json.dump(names, fout, indent=6)
  fout.close()

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
async def clr_rct(ctx, link):
  link_li = link.split('/')
  channel = await client.fetch_channel(int(link_li[5]))
  message = await channel.fetch_message(link_li[6])
  for reaction in message.reactions:
    if(str(reaction) == '\U0001f44d'):
      await reaction.clear()

'''
@client.command()
@commands.has_any_role("Admin", "Moderator")
async def check_logs(ctx):
    with open('discord.log', 'rb') as fp:
        await ctx.send('File:', file=discord.File(fp, 'discord_log.log'))
'''

"""@client.command()
@commands.has_any_role("Moderator")
async def error_handling(ctx, switch):
    \"""A command that turns off or on error handling""\"
    if(switch.lower() == "on" or switch.lower() == "off"):
        with open('settings/error_handling.txt', 'w') as f:
            f.write(switch.lower())"""

@client.command()
@commands.has_any_role("Moderator")
async def give_me_admin(ctx):
  await ctx.author.remove_roles(ctx.message.guild.get_role(648703163242905600))
            

    
for filename in os.listdir("./cogs"):
  if(filename.endswith(".py")):
    client.load_extension("cogs.{}".format(filename[:-3]))
f = open('ycwbot_token.txt')
client.run(f"{f.readline()}")
