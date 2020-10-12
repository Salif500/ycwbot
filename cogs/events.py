import discord
from discord.ext import commands
from discord.utils import get
import time

class Events(commands.Cog):
    """This category is only for events. No commands are in this category."""

    def __init__(self, client):
        self.client = client
        self.month = 0
        



    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        user_id = ctx.author.id
        if(ctx.author.id != 708745902692630560):       
            message_copy = ctx.message.content
            message_author = ctx.author.display_name
            if isinstance(ctx.message.channel, discord.DMChannel):
                channel_name = 'a DM'
            else:
                channel_name = ctx.message.channel.name    
            channel = self.client.get_channel(721506781112696854)
            await channel.send("{} command sent by {} in {} channel".format(ctx.message.clean_content, message_author, channel_name))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        with open('settings/error_handling.txt') as f:
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

    """@commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        member_id = "\n"
        guild = self.client.guilds[0]
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
                                    
        
            
                    
                

    @commands.Cog.listener()
    async def on_member_join(self,member):
        registered = False
        channel = self.client.get_channel(746863674324680815)
        await member.send('Welcome to YCW! You have just received the waiting room role for joining the server! GLHF! Please look at this document for our online workshop procedures: https://docs.google.com/document/d/1BnzQFY0t5ezTR8af6WL-kB44q6k4CLHh8_rbLCLCH3A/edit')
        await channel.send("Hello {}, welcome to YCW! How did you hear about us? If you want a tour of our discord server, please watch https://www.youtube.com/watch?v=TjndvG0hS_A. Feel free to explore our discord server and also check out https://ycwalameda.weebly.com".format(member.mention))
        if(member.id == 308027015863336960):
            try:
                role = discord.utils.get(member.guild.roles, name='Waiting')
                await member.add_roles(role)
            except:
                print('addrole error')
        else:
            role = discord.utils.get(member.guild.roles, name='Waiting')
            await member.add_roles(role)      


        
            

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        behalf = True
        async for entry in self.client.guilds[0].audit_logs(limit=2, action=discord.AuditLogAction.ban):
            if(entry.target == member):
                behalf = False
        async for entry in self.client.guilds[0].audit_logs(limit=2, action=discord.AuditLogAction.kick):
            if(entry.target == member):
                behalf = False
        if(behalf == True):
            await member.send("You've Left. Can you respond with a reason, like \"Not Interested\" or just type \"None\". Thanks for your feedback!")
            reply = await self.client.wait_for('message',  check=lambda message: message.author == member, timeout=300.0) 
            channel = self.client.get_channel(737393771624399049)
            await channel.send('{} has left. Reason: {}'.format(member.display_name, reply.content))
                              

        
            
                
            
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="some YCW vids. Subscribe to YCW!"))
        print("Bot is ready")

         

def setup(client):
    client.add_cog(Events(client))
