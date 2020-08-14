import discord
from discord.ext import commands
import time

class Events(commands.Cog):
    """This category is only for events. No commands are in this category. Some features of the category are that if you do \"question: your question\", it will give your question to all tutors. If you defean, you will automagically be put to the defeaned channel, and if you undefean you get moved back. """

    def __init__(self, client):
        self.client = client
        self.month = 0
        

    def number_to_month(self):
        """Converting a month number to a month name"""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.month = months[int(self.month) - 1]

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        global month, pos
        user_id = ctx.author.id
        if(ctx.author.id != 708745902692630560):       
            message_copy = ctx.message.content
            message_author = ctx.author.display_name
            
            message_time_list = str(ctx.message.created_at).split(" ")
            message_var = message_time_list[0]
            message_time_list2 = message_var.split("-")
            year = message_time_list2[0]
            self.month = message_time_list2[1]
            self.number_to_month()
            day = message_time_list2[2]
            if(day[-1] == 1):
                day_suffix = "st"
            elif(day[-1] == 2):
                day_suffix = "nd"
            elif(day[-1] == 3):
                day_suffix = "rd"
            else:
                day_suffix = "th"
            
            channel = self.client.get_channel(721506781112696854)
            await channel.send("{} command sent by {} at {} {}{}, {}".format(ctx.message.clean_content, message_author, self.month, day, day_suffix, year))

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
                        
        
            

        

    @commands.Cog.listener()
    async def on_message(self, message):
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
                                        await first_message.channel.send("{}. Your question has been replied by {} who says, {}".format(first_message.author.display_name, reply.author.display_name, reply.content))
                                    
        
            
                    
                

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if(member.id != 308027015863336960):
            registered = False
            channel = self.client.get_channel(648705311963611147)
            await member.send('Welcome to YCW! You have just received the student role for joining the server! GLHF! Please look at this document for our online workshop procedures: https://docs.google.com/document/d/1BnzQFY0t5ezTR8af6WL-kB44q6k4CLHh8_rbLCLCH3A/edit')
            await channel.send("Hello {}, welcome to YCW! How did you hear about us? If you want a tour of our discord server, please watch https://youtu.be/v1M0Ruj_ghE. Feel free to explore our discord server and also check out https://ycwalameda.weebly.com".format(member.mention))
            try:
                for role in self.client.guilds[0].roles:
                    if(str(role) == "Student"):
                        await member.add_roles(role)
            except:
                print('add_role error')
            with open('cf/cfscores.txt') as f:
                lines = f.readlines()
            for line in lines:
                liner = line.split(' | ')
                if(int(liner[1]) == member.id):
                    registered = True
            if(registered == False):
                with open('cf/cfscores.txt', 'a') as f:
                    f.write('{} | {} | 0 | 0 | \n'.format(member.display_name, member.id))

        
            

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
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="some YCW vids"))
        print("Bot is ready")

         

def setup(client):
    client.add_cog(Events(client))
