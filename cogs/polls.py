import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import json
import asyncio

class Polls(commands.Cog):
    """A Poll creator... Please don't spam this as this uses space. This idea was suggested by Haroon Syed."""
    
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cp'])
    async def create_poll(self, ctx, name_of_poll, type_of_poll, channel_name, *, question):
        """Creates a poll given a name and the type of poll. Types of polls are "yes/no". More will be implemented later. Please type the words exactly excluding quotes."""
        name = name_of_poll
        if(channel_name.startswith('<#') and channel_name.endswith('>')):
            channel = self.client.get_channel(int(channel_name[2:-1]))         
        else:
            channel = discord.utils.get(self.client.guilds[0].text_channels, name=channel_name)
        if(channel == None):
            await ctx.send('You have sent a wrong channel, or no channel. Please use .help to find parameters.')
        else:
            message = await channel.send('{}? Please react thumbs up for yes and thumbs down for no.'.format(question))
            with open('polls/polls.json', encoding='utf8') as f:
                polls = json.load(f)
            try:
                polls[str(ctx.author.id)]['name'] = ctx.author.display_name
                polls[str(ctx.author.id)]['current_polls'][name.lower()] = {'id' : message.id, 'channel_id' : message.channel.id}
            except KeyError:
                polls[str(ctx.author.id)] = {'name' : ctx.author.display_name, 'current_polls' : {name.lower() : {'id' : message.id, 'channel_id' : message.channel.id}}}
            with open('polls/polls.json', 'w', encoding='utf8') as f:
                json.dump(polls, f, indent=6)
            await message.add_reaction('\U0001f44d')
            await message.add_reaction('\U0001f44e')
    

    @commands.command(aliases=['spd'])
    async def send_poll_data(self, ctx, name_of_poll, channelsend:discord.TextChannel=None):
        name = name_of_poll
        """Sends the poll data through a pie chart"""
        account_created = True
        plt.clf()
        with open('polls/polls.json', encoding='utf8') as f:
            polls = json.load(f)
        try:
            messages_dict = polls[str(ctx.author.id)]['current_polls']
        except KeyError:
            await ctx.send("You haven't created a poll yet.")
            account_created = False
        if(account_created):
            if(name.lower() in messages_dict):
                channel = self.client.guilds[0].get_channel(int(messages_dict[name.lower()]['channel_id']))
                message = await channel.fetch_message(int(messages_dict[name.lower()]['id']))
                reactions = message.reactions
                my_data = []
                my_labels = ''
                for reaction in reactions:
                    if(str(reaction) == '\U0001f44d'):
                        value1 = reaction.count - 1
                    elif(str(reaction) == '\U0001f44e'):
                        value2 = reaction.count - 1
                    else:
                        my_data.append(reaction.count)
                        my_label += reaction.name
                my_data.append(value1)
                my_data.append(value2)
                my_labels = 'Yes','No'
                my_colors = ['lightblue','silver']
                my_explode = (0.1, 0)
                plt.pie(my_data,labels= my_labels, autopct='%1.1f%%', shadow=True, colors=my_colors, explode=my_explode, startangle=15)
                title = message.content.replace(' Please react thumbs up for yes and thumbs down for no.', '')
                plt.title(f'{title}')
                plt.axis('equal')
                plt.savefig('polls/{}_{}.png'.format(name, ctx.author.id))
                f = open('polls/{}_{}.png'.format(name, ctx.author.id), 'rb')
                file = discord.File(fp=f, filename='polls/{}_{}.png'.format(name, ctx.author.id))
                f.close()
                if(channelsend == None):
                    await ctx.send(file=file)
                else:
                    await channelsend.send(file=file)
            else:
                await ctx.send("You don't have that poll...If you want someone else's poll data do .spnd.")
                
    @commands.command(aliases=['spnyd', 'spnd'])
    async def send_notyou_poll_data(self, ctx, name_of_poll, member:discord.Member, channelsend:discord.TextChannel=None):
        """Sends the poll data through a pie chart. This command sends someone else's pie chart data not yours."""
        name = name_of_poll
        account_created = True
        plt.clf()
        with open('polls/polls.json', encoding='utf8') as f:
            polls = json.load(f)
        try:
            messages_dict = polls[str(member.id)]['current_polls']
        except KeyError:
            await ctx.send("He/She hasn't created a poll yet.")
            account_created = False
        if(account_created):
            if(name.lower() in messages_dict):
                channel = self.client.guilds[0].get_channel(int(messages_dict[name.lower()]['channel_id']))
                message = await channel.fetch_message(int(messages_dict[name.lower()]['id']))
                reactions = message.reactions
                for reaction in reactions:
                    if(str(reaction) == '\U0001f44d'):
                        value1 = reaction.count - 1
                    elif(str(reaction) == '\U0001f44e'):
                        value2 = reaction.count - 1
                my_data = [value1,value2]
                my_labels = 'Yes','No'
                my_colors = ['lightblue','silver']
                my_explode = (0.1, 0)
                plt.pie(my_data,labels= my_labels, autopct='%1.1f%%', shadow=True, colors=my_colors, explode=my_explode, startangle=15)
                title = message.content.replace(' Please react thumbs up for yes and thumbs down for no.', '')
                plt.title(f'{title}')
                plt.axis('equal')
                plt.savefig('polls/{}_{}.png'.format(name, member.id))
                f = open('polls/{}_{}.png'.format(name, member.id), 'rb')
                file = discord.File(fp=f, filename='polls/{}_{}.png'.format(name, member.id))
                f.close()
                if(channelsend == None):
                    await ctx.send(file=file)
                else:
                    await channelsend.send(file=file)
            else:
                await ctx.send("They don't have that poll...")

    @commands.command(aliases=['apd'])
    async def all_poll_data(self, ctx, member:discord.Member=None):
        """This sends all poll links and their respective names"""
        if(member == None):
            member = ctx.author
        with open('polls/polls.json', encoding='utf8') as f:
            polls = json.load(f)
        try:
            dict_info = polls[str(member.id)]
            account_found = True
        except KeyError:
            await ctx.send(f"{member.display_name} doesn't have any polls.")
            account_found = False
        if(account_found):
            embed = discord.Embed(title=f"{member.display_name}'s current polls", description="The Poll Names and their respective links are given in this embed")
            for element in dict_info['current_polls']:
                channel = self.client.guilds[0].get_channel(dict_info['current_polls'][element]['channel_id'])
                message = await channel.fetch_message(dict_info['current_polls'][element]['id'])
                embed.add_field(name=f'{element}'.capitalize(), value=message.jump_url, inline=False)
            await ctx.send('',embed=embed)

    @commands.command(aliases=['pdl'])
    async def poll_data_link(self, ctx, link):
        """Gives the yes/no poll data of a link"""
        link_li = link.split('/')
        channel = await self.client.fetch_channel(int(link_li[5]))
        message = await channel.fetch_message(link_li[6])
        member = message.author 
        name = "_".join(message.content.lstrip().rstrip().split(' ')) 
        name = name.replace('?', '')
        name = name.replace('.', '')
        reactions = message.reactions
        for reaction in reactions:
            if(str(reaction) == '\U0001f44d'):
                value1 = reaction.count - 1
            elif(str(reaction) == '\U0001f44e'):
                value2 = reaction.count - 1
        my_data = [value1,value2]
        my_labels = 'Yes','No'
        my_colors = ['lightblue','silver']
        my_explode = (0.1, 0)
        plt.pie(my_data,labels= my_labels, autopct='%1.1f%%', shadow=True, colors=my_colors, explode=my_explode, startangle=15)
        title = message.content.replace(' Please react thumbs up for yes and thumbs down for no.', '')
        plt.title(f'{title}')
        plt.axis('equal')
        plt.savefig('polls/{}_{}.png'.format(name, member.id))
        f = open('polls/{}_{}.png'.format(name, member.id), 'rb')
        file = discord.File(fp=f, filename='polls/{}_{}.png'.format(name, member.id))
        f.close()
        await ctx.send(file=file)        
            
            
                
                
                    

def setup(client):
    client.add_cog(Polls(client))
