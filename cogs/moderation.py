import discord, datetime, calendar, pytz
from discord.ext import commands


class Moderation(commands.Cog):
  """This category is only for events and moderation. Most of this is just events but there are a few commands.(ADMIN ONLY)"""

  def __init__(self, client):
    self.client = client
    self.month = 0
    



  @commands.Cog.listener()
  async def on_command_completion(self, ctx):
    if(ctx.author.id != 708745902692630560):       
      message_author = ctx.author.display_name
      if isinstance(ctx.message.channel, discord.DMChannel):
        channel_name = 'a DM'
        guild = self.client.get_guild(648702233537413120)
      else:
        channel_name = ctx.message.channel.name  
        guild = ctx.message.guild  
      channel = discord.utils.get(guild.text_channels, name='commands')
      await channel.send("{} command sent by {} in {} channel".format(ctx.message.clean_content, message_author, channel_name))

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    with open('dynamic/error_handling.txt') as f:
      line = f.readline()
    if(line.rstrip().lower() == "on"):
      if("charmap" in str(error)):
        await ctx.send("I can't read that character you may have sent")
      elif("is not found" in str(error)):
        error_split = str(error).split('"')
        error_command = error_split[1]
        if('.' in error_command):
          pass
        else:
          await ctx.send("The command that you have entered is not a command. Please use the .help command to find out all commands.")
      elif("is a required argument that is missing" in str(error)):
        await ctx.send("You have not entered all the parameters. Use .help to find all the parameters. Then put the parameters in order like this\".command <parameter> <parameter> <parameter>\"")
      elif("You are missing at least one of" in str(error)):
        roles = str(error).split(": ")
        await ctx.send("You are not allowed to do this command. Only {} can use this".format(roles[1]))
      elif('Converting to "int" failed for parameter "numofpeople".' in str(error)):
        await ctx.send('You have put in a category in place of a number or you just put some random mumbo jumbo. If you want to put specify a category, you first have to put a number in front')
      elif('Converting to "int" failed for parameter' in str(error)):
        await ctx.send("That isn't a number.")
      elif('Member' in str(error)):
        if('not found' in str(error)):
          await ctx.send("That isn't a member, or that member isn't found")
      
      else:
        await ctx.send(error)
    else:
      raise error

      

  @commands.command()
  async def ccc(self, ctx):
    text_channels = [x.name for x in ctx.message.guild.text_channels]
    voice_channels = [x.name for x in ctx.message.guild.voice_channels]
    await ctx.send('Voice Channels: {}\n Text Channels: {}'.format(','.join(voice_channels), ','.join(text_channels)))     



  @commands.Cog.listener()
  async def on_member_join(self,member):
    channel = discord.utils.get(member.guild.text_channels, name='waiting')
    if(channel == None):
      channel = discord.utils.get(member.guild.text_channels, name='general-chat')
      if(channel == None):
        channel = discord.utils.get(member.guild.text_channels, name='general')
    await member.send('Welcome to YCW! You have just received the waiting room role for joining the server! GLHF! Please look at this document for our online workshop procedures: https://docs.google.com/document/d/1BnzQFY0t5ezTR8af6WL-kB44q6k4CLHh8_rbLCLCH3A/edit')
    await channel.send("Hello {}, welcome to YCW! How did you hear about us? If you want a tour of our discord server, please watch https://www.youtube.com/watch?v=TjndvG0hS_A. Feel free to explore our discord server and also check out https://ycwalameda.weebly.com".format(member.mention))
    if(member.id == 308027015863336960):
      try:
        role = discord.utils.get(member.guild.roles, name='Admin')
        await member.add_roles(role)
      except:
        print('addrole error')
    else:
      role = discord.utils.get(member.guild.roles, name='Waiting')
      await member.add_roles(role)      


  @commands.Cog.listener()
  async def on_member_remove(self, member):
    behalf = True
    async for entry in member.guild.audit_logs(limit=2, action=discord.AuditLogAction.ban):
      if(entry.target == member):
        behalf = False
    async for entry in member.guild.audit_logs(limit=2, action=discord.AuditLogAction.kick):
      if(entry.target == member):
        behalf = False
    if(behalf == True):
      await member.send("You've Left. Can you respond with a reason, like \"Not Interested\" or just type \"None\". Thanks for your feedback!")
      reply = await self.client.wait_for('message',  check=lambda message: message.author == member, timeout=300.0) 
      channel = self.client.get_channel(745033017759760455)
      await channel.send('{} has left. Reason: {}'.format(member.display_name, reply.content))
      
                

  @commands.command()
  @commands.has_any_role("Moderator")
  async def error_handling(self, ctx, switch):
    """A command that turns off or on error handling(ADMIN ONLY)"""
    if(switch.lower() == "on" or switch.lower() == "off"):
      with open('dynamic/error_handling.txt', 'w') as f:
        f.write(switch.lower())

  @commands.command()
  @commands.has_any_role("Admin", "Moderator")
  async def kick(self, ctx, member : discord.Member, *, reason):
    """Kicks a member given member"""
    await ctx.message.guild.kick(member, reason=reason)

  @commands.command()
  @commands.has_any_role("Admin", "Moderator")
  async def ban(self, ctx, member : discord.Member, delete_messages_by_x_amount_of_days:int=0):
    """Bans a member given member and deletes most recent messages by a certain amount of days"""
    await ctx.send('Do you have a reason to ban this member? Reply with no if no reason.')
    reason = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
    if(reason.content.lower() == 'no' or reason.content.lower() == 'none'):
      reason = None
    else:
      reason = reason.content
    await ctx.message.guild.ban(member, reason=reason, delete_message_days=delete_messages_by_x_amount_of_days)
        
  @commands.command()
  @commands.has_any_role("Admin", "Moderator") 
  async def find_dms(self, ctx, member:discord.Member):
    """finds a certain person's dm"""
    channel = await member.create_dm()
    messages = []
    async for message in channel.history():
      messages.append(message)
    messages2 = messages[:]
    string = '\n'.join([message.content for message in messages])
    string1 = ','.join([str(message2.created_at) for message2 in messages2])
    await ctx.author.send('```{}```'.format(string))
    await ctx.author.send(string1)
    
  

  @commands.command(aliases=['fct', 'time'])
  async def find_current_time(self, ctx, param='datetime'):
    tz = pytz.timezone('America/Los_Angeles')
    date_date = datetime.datetime.now(tz)
    if(param.lower() == 'datetime'):
      await ctx.send(date_date)
    elif(param.lower() == 'date'):
      dates = str(date_date).split(' ')[0].split('-')
      li = str(date_date).split(' ')[1].split(':')
      if(int(li[0]) > 12):
        hour = int(li[0]) - 12
        fc = 'PM'
      else:
        hour = int(li[0])
        fc = 'AM'
      await ctx.send('{}/{}/{} {}:{}:{} {}'.format(dates[1], dates[2], dates[0], hour, li[1], li[2], fc))
    elif(param.lower() == 'dayname'):
      dates = str(date_date).split(' ')[0].split('-')
      datec = f'{dates[2]} {dates[1]} {dates[0]}'
      await ctx.send(calendar.day_name[datetime.datetime.strptime(datec, '%d %m %Y').weekday()])

  @commands.command()
  async def delete_recent_message(self, ctx, member:discord.Member):
    channel = await member.create_dm()
    messages = await channel.history(limit=1).flatten()
    message = messages[0]
    await message.delete()

  @commands.command()
  @commands.has_any_role("Admin", "Moderator")
  async def send_to(self, ctx, member:discord.Member, *, message):
    await member.send(message)
    
  @commands.Cog.listener()
  async def on_ready(self):
    await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="some YCW vids. Subscribe to YCW!"))
    print("Bot is ready")

         

def setup(client):
    client.add_cog(Moderation(client))
























    """@commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        member_id = "\n"
        guild = ctx.message.guild
        defeaned_channel = self.client.get_channel(731661820510863431)
        if(after.channel != None and before.channel != None):
            if(after.self_deaf == True and after.channel.name != "defeaned"):
                with open("settings/defeaned_cache.txt", "a") as f:
                    f.write("\n{} | {}".format(member.id, before.channel.name))
                await member.move_to(defeaned_channel)
            elif(after.self_deaf == False):
                with open("settings/defeaned_cache.txt") as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.split(" | ")
                        member_id = line[0]
                        if(member_id.rstrip().lstrip() == str(member.id)):
                            channel_name = line[1]
                            channel = discord.utils.get(guild.voice_channels, name=channel_name)
                            await member.move_to(channel)
                        
                with open("settings/defeaned_cache.txt", "w") as f:
                    for line in lines:
                        line_list = line.split(" | ")
                        member_id = line_list[0]
                        if(member_id.rstrip().lstrip() != str(member.id)):
                            f.write("\n" + line)
            else:
                pass"""
                        
        
            

        

    """@commands.Cog.listener()
    async def on_message(self, message):
        if(message.content.startswith('https://cdn.discordapp.com/attachments')):
            await message.delete()      
            first_message = message
            global first_letter
            global second_letter
            first_letter = None
            second_letter = None
            if(message.author.id != 708745902692630560):
                filter_content = []
                channel = message.channel
                with open("settings/filter_content.txt") as f:
                    for line in f.readlines():
                        filter_content.append(line)
                for element in filter_content:
                    if(element in message.content):
                        asterisks = []
                        try:
                            first_letter = element[0]
                            second_letter = element[1]
                        except:
                            pass
                        if(first_letter and second_letter != None):
                            length = len(message.content)
                            for i in range(1, length-2):
                                asterisks.append("*")
                            await channel.purge(limit=1)
                            if(element == 'tenor.com' or element == 'giphy.com'):
                                await channel.send("{}, We do not allow tenor/giphy links due to an influx of spamming with these gifs.".format(message.author.mention))
                            else:
                                await channel.send("The word {}{}\{} is not allowed. Please ask an Admin if this is a mistake".format(first_letter, second_letter, (''.join(asterisks))))
            if(message.content.startswith("question: ")):
                for guild in self.client.guilds:
                    for role in guild.roles:
                        if(str(role) == "Admin" or str(role) == "Tutor" ):
                            for member in role.members:
                                if(member.status != discord.Status.offline):
                                    await member.send('Hey {}. {} has asked a question. He said \"{}\" in the channel "{}". Respond here if you want to respond or just wait till 60 seconds are over.'.format(member.mention, message.author.display_name, message.content, message.channel))
                                    reply = None
                                    reply = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == member)
                                    if(reply != None):
                                        await first_message.channel.send("{}. Your question has been replied by {} who says, {}".format(first_message.author.display_name, reply.author.display_name, reply.content))"""
                                    
        