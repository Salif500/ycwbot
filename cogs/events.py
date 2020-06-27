import discord
from discord.ext import commands
import time

all_embed_settings = {}

def update_link_dict():
    with open("settings/embed_links.txt") as f:
        lines = f.readlines()
        for line in lines:
            line_split = line.split(" : ")
            key = line_split[0]
            value = line_split[1]
            all_embed_settings[key] = value

update_link_dict()

class Events(commands.Cog):
    """This category is only for events. No commands are in this category."""

    def __init__(self, client):
        self.client = client
        self.month = 0

    def number_to_month(self):
        """Converting a month number to a month name"""
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.month = months[int(self.month) - 1]

    @commands.Cog.listener()
    async def on_message(self,message):
        global month, pos
        user_id = message.author.id
        if(message.content.startswith('.')):
            if(message.author.id != 708745902692630560):
                message_copy = message.content
                message_author = message.author.display_name
                
                message_time_list = str(message.created_at).split(" ")
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
                await channel.send("{} command sent by {} at {} {}{}, {}".format(message_copy, message_author, self.month, day, day_suffix, year))
        elif(message.content.startswith('https://')):
            update_link_dict()
            try:
                if(all_embed_settings[user_id] == "True"):
                    embed1 = discord.Embed.from_data(message.embeds)
                    if not message.embeds:
                        pass
                    else:
                        await self.client.delete_message(message)
                        await message.channel.send('', embed=embed1)
            except:
                pass
            
                    
                

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.client.get_channel(648705311963611147)
        await channel.send("Hello {}, welcome to YCW! How did you hear about us? If you want a tour of our discord server, please watch https://youtu.be/v1M0Ruj_ghE. Feel free to explore our discord server and also check out https://ycwalameda.weebly.com!".format(member.mention))
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="some YCW vids"))    
        print("Bot is ready")

def setup(client):
    client.add_cog(Events(client))
