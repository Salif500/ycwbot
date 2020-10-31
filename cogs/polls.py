import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import json
import random
import unicodedata as uni

class Polls(commands.Cog):
    """A Poll creator... Please don't spam this as this uses space. This idea was suggested by Haroon Syed."""
    
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cp'])
    async def create_poll(self, ctx, name_of_poll, channel_name, *, question):
        """Creates a poll given a name and the type of poll. More will be implemented later. Please type the words exactly excluding quotes."""
        messagesend = await ctx.send('What emoji choices do you want with this poll? React to this message with the correct emojis and reply to this message with "done" or you can type presets, presets are "yes/no", "1-10", ')
        error = False
        reply = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=300.0)
        if('done' in reply.content.lower()):
          reactions = messagesend.reactions
        elif('yes/no' in reply.content.lower()):
          reactions = []
          reactions.append('\U0001f44d')
          reactions.append('\U0001f44e')
        elif('1-10' in reply.content.lower()):
          reactions = []
          for i in range(9):
            reactions.append('{}\N{variation selector-16}\N{combining enclosing keycap}'.format(i+1))
          reactions.append('\N{keycap ten}')
        else:
          error = True
          await ctx.send("You haven't sent a correct reply")
        if(not error):
          name = name_of_poll
          if(channel_name.startswith('<#') and channel_name.endswith('>')):
              channel = self.client.get_channel(int(channel_name[2:-1]))         
          else:
              channel = discord.utils.get(self.client.guilds[0].text_channels, name=channel_name)
          if(channel == None):
              await ctx.send('You have sent a wrong channel, or no channel. Please use .help to find parameters.')
          else:
              message = await channel.send('{}? Please react with the corresponding choices.'.format(question))
              with open('dynamic/{}/polls/polls.json'.format(ctx.message.guild.id), encoding='utf8') as f:
                  polls = json.load(f)
              try:
                  polls[str(ctx.author.id)]['name'] = ctx.author.display_name
                  polls[str(ctx.author.id)]['current_polls'][name.lower()] = {'id' : message.id, 'channel_id' : message.channel.id}
              except KeyError:
                  polls[str(ctx.author.id)] = {'name' : ctx.author.display_name, 'current_polls' : {name.lower() : {'id' : message.id, 'channel_id' : message.channel.id}}}
              with open('dynamic/{}/polls/polls.json'.format(ctx.message.guild.id), 'w', encoding='utf8') as f:
                  json.dump(polls, f, indent=6)
              for reaction in reactions:
                await message.add_reaction(reaction)
    

    

    @commands.command(aliases=['apd'])
    async def all_poll_data(self, ctx, member:discord.Member=None):
        """This sends all poll links and their respective names"""
        if(member == None):
            member = ctx.author
        with open('dynamic/{}/polls/polls.json'.format(ctx.message.guild.id), encoding='utf8') as f:
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
      my_data, my_labels, my_explode, my_colors, i = [], [], [], [], 1
      plt.close()
      link_li = link.split('/')
      channel = await self.client.fetch_channel(int(link_li[5]))
      message = await channel.fetch_message(link_li[6])
      member = message.author 
      name = "_".join(message.content.lstrip().rstrip().split(' '))
      name = 'Custom Poll Link'
      colors = clr.cnames
      for reaction in message.reactions:
        i *= -1
        bot_react = False
        async for member in reaction.users():
          if(member.id == 708745902692630560):
            bot_react = True
        if(bot_react):
          value1 = reaction.count - 1
        elif(not bot_react):
          value1 = reaction.count
        my_data.append(value1)
        if(reaction.custom_emoji):
          pass
        else:
          if(len(str(reaction.emoji).split('\\')) == 1):
            try:
              emoji_name = uni.name(str(reaction.emoji))
            except TypeError:
              emoji_name = str(reaction.emoji)

          else:
              str(reaction.emoji).split('\\')

        my_labels.append(emoji_name)
        if(i == 1):
          num = 0.1
        elif(i == -1):
          num = 1
        my_explode.append(num)
        my_colors.append(random.choice(list(colors)))
      plt.pie(my_data,labels= my_labels, autopct='%1.1f%%', shadow=True, colors=my_colors,startangle=15)
      title = message.content.replace(' Please react thumbs up for yes and thumbs down for no.', '')
      plt.title(f'{title}')
      plt.axis('equal')
      filesave = 'dynamic/{}/polls/{}_{}.png'.format(ctx.message.guild.id, name, member.id)
      plt.savefig(filesave)
      f = open(filesave, 'rb')
      file = discord.File(fp=f, filename=filesave)
      f.close()
      await ctx.send(file=file)        
            
            
                
                
                    

def setup(client):
    client.add_cog(Polls(client))


"""@commands.command(aliases=['spd'])
    async def send_poll_data(self, ctx, name_of_poll, channelsend:discord.TextChannel=None):
        name = name_of_poll
        \"""Sends the poll data through a pie chart\"""
        account_created = True
        plt.clf()
        with open('dynamic/{}/polls/polls.json'.format(ctx.message.guild.id), encoding='utf8') as f:
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
                        my_labels += reaction.name
                my_data.append(value1)
                my_data.append(value2)
                my_labels = 'Yes','No'
                my_colors = ['lightblue','silver']
                my_explode = (0.1, 0)
                plt.pie(my_data,labels= my_labels, autopct='%1.1f%%', shadow=True, colors=my_colors, explode=my_explode, startangle=15)
                title = message.content.replace(' Please react thumbs up for yes and thumbs down for no.', '')
                plt.title(f'{title}')
                plt.axis('equal')
                plt.savefig('dynamic/{}/polls/{}_{}.png'.format(ctx.message.guild.id).format(name, ctx.author.id))
                f = open('dynamic/{}/polls/{}_{}.png'.format(ctx.message.guild.id).format(name, ctx.author.id), 'rb')
                file = discord.File(fp=f, filename='dynamic/{}/polls/{}_{}.png'.format(ctx.message.guild.id).format(name, ctx.author.id))
                f.close()
                if(channelsend == None):
                    await ctx.send(file=file)
                else:
                    await channelsend.send(file=file)
            else:
                await ctx.send("You don't have that poll...If you want someone else's poll data do .spnd.")
                
    @commands.command(aliases=['spnyd', 'spnd'])
    async def send_notyou_poll_data(self, ctx, name_of_poll, member:discord.Member, channelsend:discord.TextChannel=None):
        \"""Sends the poll data through a pie chart. This command sends someone else's pie chart data not yours.\"""
        name = name_of_poll
        account_created = True
        plt.clf()
        with open('dynamic/{}/polls/polls.json'.format(ctx.message.guild.id), encoding='utf8') as f:
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
                plt.savefig('dynamic/{}/polls/{}_{}.png'.format(ctx.message.guild.id).format(name, member.id))
                f = open('dynamic/{}/polls/{}_{}.png'.format(ctx.message.guild.id).format(name, member.id), 'rb')
                file = discord.File(fp=f, filename='dynamic/{}/polls/{}_{}.png'.format(ctx.message.guild.id).format(name, member.id))
                f.close()
                if(channelsend == None):
                    await ctx.send(file=file)
                else:
                    await channelsend.send(file=file)
            else:
                await ctx.send("They don't have that poll...")"""