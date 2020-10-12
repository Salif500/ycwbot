import discord
from discord.ext import commands
import json

class Challengefest(commands.Cog):
    """All ChallengeFest commands located here"""
    #Change docstring to link to our challengefest page
    def __init__(self, client):
        self.client = client

    

    @commands.command(aliases=['cfd'])
    async def cfdisplay(self, ctx, member:discord.Member=None):
        """Displays ChallengeFest data for a student"""
        file = 'cf/cfscores.json'
        if(member is not None):
            username = member.display_name + "'s"
        else:
            username = 'Your'
            member = ctx.author
        with open(file, encoding='utf8') as f:
            scores = json.load(f)
            try:
                info = scores[str(member.id)]
                embed = discord.Embed(title="{} Scoreboard".format(username), color=discord.Color.teal())
                embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                embed.add_field(name='Current Points:', value=info['current_points'], inline=False)
                embed.add_field(name='Total Points:', value=info['total_points'], inline=False)
                embed.add_field(name="Number of QOTD's Completed", value=info['QOTD'], inline=False)
                if(info['completed_challenges']):
                   comp = ('\n'.join(info['completed_challenges']))
                else:
                    comp = 'No Completed Challenges'
                embed.add_field(name='Completed Challenges:', value=comp, inline=False)
                await ctx.send('', embed=embed)
            except KeyError:
                await ctx.send("Your account wasn't created. Please ask an Admin, Moderator, or Tutor to add your account.")
                
            

    

    @commands.command(aliases=['cft'])
    async def cftop(self, ctx, numofpeople:int=3, category=None):
        """Displays the top certain amount of people"""
        if(category == None or category.lower() == 'current points' or category.lower() == 'current_points' or category.lower() == 'current'):
            category = 'current_points'
        elif(category.lower() == 'total points' or category.lower() == 'total_points' or category.lower() == 'total'):
            category = 'total_points'
        elif(category.lower() == 'qotd' or category.lower() == 'qotds' or category.lower() == 'question of the day' or category.lower() == 'question of the days'):
            category = 'QOTD'
        file = 'cf/cfscores.json'
        embed = discord.Embed(title='Top {} People'.format(numofpeople), description='The Top People Given By A Certain Amount that Shows their Seasonal Points', color=discord.Color.green())
        with open(file, encoding='utf8') as f:
            scores = json.load(f)
            topscores = {}
            for key, diction in scores.items():
                topscores[key] = diction[category]
            sort_dict = sorted(topscores.items(), key=lambda x: x[1], reverse=True)
        string = ''
        count = 0
        for i in sort_dict:
            count += 1
            member = await self.client.guilds[0].fetch_member(int(i[0]))
            if(member != None):   
                string += '{} - {}\n'.format(member.display_name.title(), i[1]) 
            if(count == numofpeople):
                break
        embed.add_field(name='Top Scorers:', value=string, inline=False)
        await ctx.send('',embed=embed)
        
    @commands.command(aliases=['cfallchal'])
    async def cfall(self, ctx, code_lang):
        """Lists all challenges for a given language"""
        file = 'cf/cfchal.json'
        check = False
        with open(file, encoding='utf8') as f:
            chal = json.load(f)
        allchal = []
        for key in chal:
            if(key.lower().startswith(code_lang.lower())):
                allchal.append(key)
        if(code_lang.lower() == 'python'):
            color = discord.Color.gold()
            check = True
        elif(code_lang.lower() == 'html'):
            color = discord.Color.red()
            check = True
        elif(code_lang.lower() == 'scratch'):
            color = discord.Color.orange()
            check = True
        else:
            if(code_lang.lower() == 'c++' or code_lang.lower() == 'c#' or code_lang.lower() == 'javascript' or code_lang.lower() == 'java' or code_lang.lower() == 'js'):
                check = True
            color = discord.Color.blurple()
        if(check == True):
            if(allchal):
                pass
            else:
                allchal.append('No Challenges Yet')
            embed = discord.Embed(title='All {} Challenges'.format(code_lang.capitalize()), descripiton='For More Info: <insert_challenges_link>', color=color)
            embed.add_field(name='Challenges:', value=('\n'.join(allchal)), inline=False)
            await ctx.send('',embed=embed)
        else:
            await ctx.send('Not sure if thats a programming language')
            
    @commands.command(aliases=['cfr'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfreset(self, ctx, name:discord.Member=None):
        """Resets temporary points given during a workshop(ADMIN ONLY)"""
        file = 'cf/cfscores.json'
        if(name == None):
            await ctx.send('Do you want to reset everything?')
            reply = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
            if(reply.content.lower() == 'yes'):
                with open(file, encoding='utf8') as f:
                    scores = json.load(f)
                guild = self.client.guilds[0]
                for role in guild.roles:
                    if(role.name == 'Student'):
                        break
                for student in role.members:
                    try:
                        scores[str(student.id)]['current_points'] = 0
                    except KeyError:
                        print('No Account')
                with open(file, 'w', encoding='utf8') as f:
                    json.dump(scores, f, indent=6)
        else:
            with open(file, encoding='utf8') as f:
                scores = json.load(f)
            scores[str(name.id)]['current_points'] = 0
            with open(file, encoding='utf8') as f:
                json.dump(scores, f, indent=6)

    @commands.command(aliases=['cfm', 'cfverify', 'cfv'])
    @commands.has_any_role('Admin', 'Moderator', 'Tutor')
    async def cfmark(self, ctx, member:discord.Member, *, challenge_name):
        """Adds points to user by verifying challenges(ADMIN ONLY)"""
        filec = 'cf/cfchal.json'
        files = 'cf/cfscores.json'
        with open(filec, encoding='utf8') as f:
            chal = json.load(f)
        chal_names = [x for x in chal]
        for x in chal_names:
            if(challenge_name.lower() == x.lower()):
                with open(files, encoding='utf8') as f:
                    scores = json.load(f)
                if(x in scores[str(member.id)]['completed_challenges']):
                    await ctx.send('That challenge has already been added to {}, please use .cfaddpoints if you want to add points directly.'.format(member.display_name))
                else:
                    scores[str(member.id)]['completed_challenges'].append(x)
                    scores[str(member.id)]['total_points'] += chal[x]
                    scores[str(member.id)]['current_points'] += chal[x]
                    scores[str(member.id)]['name'] = member.display_name
                    with open(files, 'w', encoding='utf8') as f:
                        json.dump(scores, f, indent=6)
                    await ctx.send(f"{member.display_name}'s points have been added!")
                break
        else:
            await ctx.send("That isn't a challenge. The challenges are listed in .cfall")
            
                     
    @commands.command(aliases=['cfaddp'])
    @commands.has_any_role('Admin', 'Moderator', 'Tutor')
    async def cfaddpoints(self, ctx, member:discord.Member, points, qotdpoints:int=None):
        """Adds points to user directly(ADMIN ONLY)"""
        try:
            file = 'cf/cfscores.json'
            with open(file, encoding='utf8') as f:
                scores = json.load(f)
                previnfo = scores[str(member.id)]
                scores[str(member.id)]['name'] = member.display_name
                scores[str(member.id)]['current_points'] += int(points)
                scores[str(member.id)]['total_points'] += int(points)
                if(qotdpoints is not None):
                    scores[str(member.id)]['QOTD'] += qotdpoints
            with open(file, 'w', encoding='utf8') as f:
                json.dump(scores, f, indent=6)
            await ctx.send('Points have been added!')
        except KeyError:
            await ctx.send("{}'s account wasn't created.".format(member.display_name))
    @commands.command(aliases=['cfac'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfaddchal(self, ctx, code_lang, points:int, *, chal_name):
        """Creates a new Challenge(ADMIN ONLY)"""
        file = 'cf/cfchal.json'
        with open(file, encoding='utf8') as f:
            diction = json.load(f)
            diction['{}: {}'.format(code_lang.capitalize(),chal_name)] = points
        with open(file, 'w', encoding='utf8') as f:
            json.dump(diction, f, indent=6)
        await ctx.send('Challenge has been Added!')

    @commands.command(aliases=['cfremovechal', 'cfrc', 'cfdc'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfdeletechal(self, ctx, full_chal_name):
        """Removes a challenge(ADMIN ONLY)"""
        file = 'cf/cfchal.json'
        with open(file, encoding='utf8') as f:
            chal = json.load(f)
        try:
            del chal[full_chal_name]
            with open(file, 'w', encoding='utf8') as f:
                json.dump(chal, f, indent=6)
            await ctx.send('Challenge has been removed.')
        except:
            await ctx.send("That isn't a challenge. Please check all capitalization and spelling")

    

        
    @commands.command(aliases=['cfaa'])
    @commands.has_any_role('Admin', 'Moderator', 'Tutor')
    async def cfaddaccount(self, ctx, student:discord.Member):
        """This command adds a Challengefest account if it was not added in the waiting room. This also resets the current points of the user so be WARNED.(ADMIN ONLY)"""
        fin = open('cf/cfscores.json', encoding='utf8')
        scores = json.load(fin)
        fin.close()
        scores[student.id] = {'name' : f'{student.display_name}', 'current_points' : 0, 'total_points' : 0, 'QOTD' : 0, 'completed_challenges' : []}
        f = open('cf/cfscores.json', 'w', encoding='utf8')
        json.dump(scores, f, indent=6)
        f.close()
        await ctx.send(f"{student.display_name}'s account was added!")
        

    @commands.command(aliases=['cfda', 'cfremoveaccount'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfdeleteaccount(self, ctx, student:discord.Member):
        """This command deletes a Challengefest account(ADMIN ONLY)"""
        fin = open('cf/cfscores.json', encoding='utf8')
        scores = json.load(fin)
        fin.close()
        del scores[str(student.id)]
        f = open('cf/cfscores.json', 'w', encoding='utf8')
        json.dump(scores, f, indent=6)
        f.close()
        await ctx.send(f"{student.display_name}'s account was deleted.")


        
    @commands.command()
    @commands.has_any_role('Admin', 'Moderator')
    async def cfreseteverything(self, ctx):
        """Resets everything. DO NOT USE. Just DONT(ADMIN ONLY)(OBVIOUSLY)"""
        await ctx.send('Do you want to reset everything?')
        reply = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
        if(reply.content.lower() == 'yes'):
            scores = {}
            for student in self.client.guilds[0].get_role(665958098627985450).members:
              scores[student.id] = {'name' : f'{student.display_name}', 'current_points' : 0, 'total_points' : 0, 'QOTD' : 0, 'completed_challenges' : []}      
            f = open('cf/cfscores.json', 'w', encoding='utf8')
            json.dump(scores, f, indent=6)
            f.close()
        await ctx.send('Everything has been reset')
            
                
    

    
                

                            
            
    
            

def setup(client):
    client.add_cog(Challengefest(client))
