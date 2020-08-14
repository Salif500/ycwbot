import discord
from discord.ext import commands
from operator import itemgetter

class Challengefest(commands.Cog):
    """Challenges are in this category"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cfverify', 'cfm'])
    @commands.has_any_role("Admin", "Moderator")
    async def cfmark(self, ctx, name : discord.Member, *, challenge):
        """A command that adds points to a person"""
        with open('cf/cfscores.txt') as f:
            lines = f.readlines()
        with open('cf/cfchal.txt') as f:
            chaline = f.readline()
        if(challenge.lower() in chaline.lower()):
            found = False
            chale = chaline.split(',')
            for element in chale:
                num = chale.index('(')
                if(element.lower()[0:num] == challenge.lower()):
                    found = True
                    points = int(element[-2])
            if(found == True):
                with open('cf/cfscores.txt', 'w') as f:
                    for line in lines:
                        if(line.split(' | ')[1] == str(name.id)):
                            split = line.split(' | ')
                            f.write('{} | {} | {} | {} | {}'.format(split[0], split[1], str(int(split[2])+points), str(int(split[3])+points), ' ' + split[4].rstrip()+'{},\n'.format(challenge.title())))
                        else:
                            f.write(line)
                await ctx.send('Points Added!')
            else:
                await ctx.send("That challenge isn't a challenge. Probably you misspelled it")

        else:
            await ctx.send("That challenge isn't a challenge. Probably you misspelled it")

    

    @commands.command(aliases=['cfd'])
    async def cfdisplay(self, ctx, name:discord.Member=None):
        """A command that will display the table of challenges for a given student"""
        if(name == None):
            user = ctx.author
            user_def = 'Your'
        else:
            user = name
            user_def = user.display_name + "'s"
        string = ''
        with open('cf/cfscores.txt') as f:
            lines = f.readlines()
        for line in lines:
            liner = line.split(' | ')
            user_id = liner[1]
            if(int(user_id) == user.id):
                break
        for element in liner[4].split(','):
            string += element + '\n'
        if(string.rstrip() == '|' or None or liner[4] == '\n' or string.startswith('\n')):
            string = 'None'
        strings = []
        strings.append(string)
        embed1 = discord.Embed(title='{} Scoreboard'.format(user_def))
        embed1.set_author(name=user.display_name, icon_url=user.avatar_url)
        embed1.add_field(name="Current Points:", value=liner[2], inline=False)
        embed1.add_field(name="Total Points:", value=liner[3], inline=False)
        embed1.add_field(name="Completed Challenges:", value=string, inline=False)
        await ctx.send('', embed=embed1)
            

    @commands.command(aliases=['cft'])
    async def cftop(self, ctx):
        """A command that will display the top three students with the most points."""
        with open('cf/cfscores.txt') as f:
            lines = f.readlines()
        scores = {}
        for line in lines:
            try:
                split = line.split(' | ')
                score = split[3]
                scores[int(split[1])] = score
            except:
                pass
        score_list = sorted(scores.items(), key=itemgetter(1), reverse=True)
        sc1, sc2, sc3 = score_list[0][1], score_list[1][1], score_list[2][1]
        top1, top2, top3 = score_list[0][0], score_list[1][0], score_list[2][0]
        top1, top2, top3, = self.client.get_user(top1), self.client.get_user(top2), self.client.get_user(top3)
        embed1 = discord.Embed(title="Top Scores", color=discord.Color.dark_red())
        for member in self.client.guilds[0].members:
            if(member == top1):
                top1 = member.display_name
            elif(member == top2):
                top2 = member.display_name
            elif(member == top3):
                top3 = member.display_name
        embed1.add_field(name='Top Scorers:', value='{} - {}\n{} - {}\n{} - {}'.format(top1, sc1.rstrip(), top2, sc2.rstrip(), top3, sc3.rstrip()), inline=False)
        await ctx.send('',embed=embed1)
        
    @commands.command(aliases=['cfa'])
    @commands.has_any_role("Admin", "Moderator")
    async def cfadd(self, ctx, category, points, *, challenge):
        """Adds a challenge to the list"""
        chal = 0
        if(category.lower == 'python'):
            chal = 'Python'
        elif(category.lower == 'html'):
            chal = 'HTML'
        elif(category.lower == 'scratch'):
            chal = 'Scratch' 
        with open('cf/cfchal.txt') as f:
            line = f.readline()
        with open('cf/cfchal.txt', 'w') as f:
            f.write(line + ',{}: {}({})'.format(category, challenge, points))
        await ctx.send('Challenge added!')

    @commands.command(aliases=['cfr'])
    @commands.has_any_role("Admin", "Moderator")
    async def cfreset(self, ctx, name:discord.Member=None):
        """Resets the points of everyone, if given a name, resets the score"""
        conf = None
        if(name == None):
            await ctx.send('Are you sure?')
            conf = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
            if(conf.content.lower() == "yes"):
                await ctx.send('Challengefest reset')
                with open('cf/cfscores.txt') as f:
                    lines = f.readlines()
                open('cf/cfscores.txt', 'w').close()  
                for member in self.client.guilds[0].members:
                    for role in member.roles:
                        if(role.name == "Student"):
                            found = False
                            for line in lines:
                                liner = line.split(' | ')
                                if(str(member.id) == liner[1]):
                                    found = True
                                    break
                            if(found == False):
                                with open('cf/cfscores.txt', 'a', encoding='utf-8') as f:
                                    f.write('{} | {} | 0 | 0 | |\n'.format(member.display_name, member.id))
                            else:
                                with open('cf/cfscores.txt', 'a', encoding='utf-8') as f:
                                    f.write('{} | {} | 0 | {} | {} \n'.format(member.display_name, member.id, liner[3], liner[4].rstrip()))
            else:
                await ctx.send('Reset Stopped')
        else:
            await ctx.send('Are you sure you want to reset {}?'.format(name.display_name) )
            conf = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
            if(conf.content.lower() == "yes"):
                with open('cf/cfscores.txt') as f:
                    lines = f.readlines()
                for line in lines:
                    if(line.split(' | ')[1] == str(name.id)):
                        remchal = line.split(' | ')[4]
                        tot = line.split(' | ')[3]
                        break
                with open('cf/cfscores.txt', 'w') as f:
                    for line in lines:
                        if(line.split(' | ')[1] == str(name.id)):
                            f.write('{} | {} | {} | {} | {}'.format(name.display_name, name.id, 0, tot, remchal))
                        else:
                            f.write(line)

    """@commands.command()
    @commands.has_any_role('Moderator')
    async def cfreseteverything(self, ctx):
        \"""This command resets literally every total score and every total challenge completed. DO NOT USE\"""
        await ctx.send('Are you sure?')
        conf = await self.client.wait_for('message', timeout=60.0, check=lambda message: message.author == ctx.author)
        if(conf.content.lower() == "yes"):
            for member in self.client.guilds[0].members:
                for role in member.roles:
                    if(role.name == "Student"):
                        with open('cf/cfscores.txt', 'a') as f:
                            f.write('{} | {} | {} | {} | \n'.format(member.display_name, member.id, 0, 0))"""

    @commands.command()
    async def cfall(self, ctx, group, remain=None):
        """This command lists all challenges per a given group"""
        if(remain == None):
            with open('cf/cfchal.txt') as f:
                line = f.readline()
            split = line.split(',')
            if(group.lower() == 'python'):
                python = []
                for element in split:
                    if(element.lower().startswith('python')):
                        python.append(element)
                embed1 = discord.Embed(title='All Python Challenges', description='For More Info: ', color=discord.Color.gold())
                embed1.add_field(name='Challenges:', value=('\n'.join(python)), inline=False)
                await ctx.send('', embed=embed1)
            elif(group.lower() == 'html'):
                html = []
                for element in split:
                    if(element.lower().startswith('html')):
                        html.append(element)
                embed1 = discord.Embed(title='All HTML Challenges', description='For More Info: ', color=discord.Color.red())
                embed1.add_field(name='Challenges:', value=('\n'.join(html)), inline=False)
                await ctx.send('', embed=embed1)
            elif(group.lower() == 'scratch'):
                scratch = []
                for element in split:
                    if(element.lower().startswith('scratch')):
                        scratch.append(element)
                embed1 = discord.Embed(title='All Scratch Challenges', description='For More Info: ', color=discord.Color.orange())
                embed1.add_field(name='Challenges:', value=('\n'.join(scratch)), inline=False)
                await ctx.send('', embed=embed1)
            else:
                await ctx.send('You have entered a wrong group. Please try again.')
        else:
            found_r = False
            line_r = None
            with open('cf/cfchal.txt') as f:
                line = f.readline()
            split = line.split(',')
            if(group.lower() == 'python'):
                python = []
                pythonr = []
                with open('cf/cfscores.txt') as f:
                    lines = f.readlines()
                    for line in lines:
                        if(line.split(' | ')[1] == ctx.author.id):
                            found_r = True
                            line_r = line.split(' | ')
                            break
                    if(found_r == True):
                        chalr = line_r[4].rstrip().split(',')
                        for element in chalr:
                            if(element.lower().startswith('python')):
                                pythonr.append(element)
                for element in split:
                    if(element.lower().startswith('python')):
                        if(element in pythonr):
                            pass
                        else:
                            python.append(element)
                embed1 = discord.Embed(title='All Python Challenges', description='For More Info: ', color=discord.Color.gold())
                embed1.add_field(name='Challenges:', value=('\n'.join(python)), inline=False)
                await ctx.send('', embed=embed1)
            elif(group.lower() == 'html'):
                html = []
                htmlr = []
                with open('cf/cfscores.txt') as f:
                    lines = f.readlines()
                    for line in lines:
                        if(line.split(' | ')[1] == ctx.author.id):
                            found_r = True
                            line_r = line.split(' | ')
                            break
                    if(found_r == True):
                        chalr = line_r[4].rstrip().split(',')
                        for element in chalr:
                            if(element.lower().startswith('html')):
                                htmlr.append(element)
                for element in split:
                    if(element.lower().startswith('html')):
                        if(element in htmlr):
                            pass
                        else:
                            html.append(element)
                embed1 = discord.Embed(title='All HTML Challenges', description='For More Info: ', color=discord.Color.red())
                embed1.add_field(name='Challenges:', value=('\n'.join(html)), inline=False)
                await ctx.send('', embed=embed1)
            elif(group.lower() == 'scratch'):
                scratch = []
                scratchr = []
                with open('cf/cfscores.txt') as f:
                    lines = f.readlines()
                    for line in lines:
                        if(line.split(' | ')[1] == ctx.author.id):
                            found_r = True
                            line_r = line.split(' | ')
                            break
                    if(found_r == True):
                        chalr = line_r[4].rstrip().split(',')
                        for element in chalr:
                            if(element.lower().startswith('scratch')):
                                scratchr.append(element)
                for element in split:
                    if(element.lower().startswith('scratch')):
                        if(element in scratchr):
                            pass
                        else:
                            scratch.append(element)
                embed1 = discord.Embed(title='All Scratch Challenges', description='For More Info: ', color=discord.Color.orange())
                embed1.add_field(name='Challenges:', value=('\n'.join(scratch)), inline=False)
                await ctx.send('', embed=embed1)
            else:
                await ctx.send('You have entered a wrong group. Please try again.')    
                                    
                            
            
    
            

def setup(client):
    client.add_cog(Challengefest(client))
