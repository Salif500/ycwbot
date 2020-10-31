import discord, json, datetime, asyncio, calendar
from discord.ext import commands, tasks


class Challengefest(commands.Cog):
    """All ChallengeFest commands located here"""
    #Change docstring to link to our challengefest page
    def __init__(self, client):
      self.client = client
      self.qotd_loop.start()
      self.cfbackupscores.start()

     
    


    @commands.command(aliases=['cfd'])
    async def cfdisplay(self, ctx, member:discord.Member=None):
        """Displays ChallengeFest data for a student"""
        file = 'dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id)
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
              await ctx.invoke(self.client.get_command('cfaddaccount'), member)
              await ctx.invoke(self.client.get_command('cfdisplay'), member)
                
    
      
    

    @commands.command(aliases=['cft'])
    async def cftop(self, ctx, numofpeople="3", category=None):
        """Displays the top certain amount of people"""
        file = 'dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id)
        with open(file, encoding='utf8') as f:
          scores = json.load(f)
        if(str(numofpeople).lower() == 'all'):
          numofpeople = len(scores)
        else:
          numofpeople = int(numofpeople)
        if(category == None or category.lower() == 'current points' or category.lower() == 'current_points' or category.lower() == 'current'):
            category = 'current_points'
        elif(category.lower() == 'total points' or category.lower() == 'total_points' or category.lower() == 'total'):
            category = 'total_points'
        elif(category.lower() == 'qotd' or category.lower() == 'qotds' or category.lower() == 'question of the day' or category.lower() == 'question of the days'):
            category = 'QOTD'
        embed = discord.Embed(title='Top {} People'.format(numofpeople), description='The Top People Given By A Certain Amount that Shows their Seasonal Points', color=discord.Color.green())
            
        topscores = {}
        for key, diction in scores.items():
            topscores[key] = diction[category]
        sort_dict = sorted(topscores.items(), key=lambda x: x[1], reverse=True)
        string = ''
        count = 0
        for i in sort_dict:
            count += 1
            try:
              member = await ctx.message.guild.fetch_member(int(i[0]))
            except:
              continue
            if(member != None):   
                string += '{} - {}\n'.format(member.display_name.title(), i[1]) 
            if(count == numofpeople):
                break
        embed.add_field(name='Top Scorers:', value=string, inline=False)
        await ctx.send('',embed=embed)
        
    @commands.command(aliases=['cfallchal', 'cfa'])
    async def cfall(self, ctx, code_lang):
        """Lists all challenges for a given language"""
        file = 'dynamic/{}/cf/cfchal.json'.format(ctx.message.guild.id)
        check = False
        with open(file, encoding='utf8') as f:
            chal = json.load(f)
        allchal = []
        for key, value in chal.items():
            if(key.lower().startswith(code_lang.lower())):
                allchal.append('{}, Points: {}'.format(key, value))
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

    
    @commands.command(aliases=['cfqm', 'cfqotdm'])
    @commands.has_any_role('Admin', 'Moderator', 'Tutor')
    async def cfqotdmark(self, ctx, member: discord.Member, if_first):
      """Marks qotd points as well as normal points"""
      qotdpoints = 1
      if('w' in if_first.lower()):
        points = 10
      else:
        points = 5
      try:
        file = 'dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id)
        with open(file, encoding='utf8') as f:
            scores = json.load(f)
            scores[str(member.id)]['name'] = member.display_name
            scores[str(member.id)]['current_points'] += int(points)
            scores[str(member.id)]['total_points'] += int(points)
            if(qotdpoints != 0):
                scores[str(member.id)]['QOTD'] += qotdpoints
        with open(file, 'w', encoding='utf8') as f:
            json.dump(scores, f, indent=6)
        await ctx.send('Points have been added!')
        await member.send('You have obtained {} points.'.format(points))
      except KeyError:
        await ctx.invoke(self.client.get_command('cfaddaccount'), member)
        await ctx.invoke(self.client.get_command('cfaddpoints'), member, points, qotdpoints)
    
    

    @commands.command(aliases=['cfm', 'cfverify', 'cfv'])
    @commands.has_any_role('Admin', 'Moderator', 'Tutor')
    async def cfmark(self, ctx, member:discord.Member, *, challenge_name):
        """Adds points to user by verifying challenges(ADMIN ONLY)"""
        filec = 'dynamic/{}/cf/cfchal.json'.format(ctx.message.guild.id)
        files = 'dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id)
        with open(filec, encoding='utf8') as f:
          chal = json.load(f)
        chal_names = [x for x in chal]
        for x in chal_names:
            if(challenge_name.lower() == x.lower()):
                with open(files, encoding='utf8') as f:
                    scores = json.load(f)
                try:
                  diction = scores[str(member.id)]
                except KeyError:
                  await ctx.invoke(self.client.get_command('cfaddaccount'), member)
                  await ctx.invoke(self.client.get_command('cfmark'), member, challenge_name)
                if(x in diction['completed_challenges']):
                    await ctx.send('That challenge has already been added to {}, please use .cfaddpoints if you want to add points directly.'.format(member.display_name))
                else:
                    diction['completed_challenges'].append(x)
                    diction['total_points'] += chal[x]
                    diction['current_points'] += chal[x]
                    diction['name'] = member.display_name
                    with open(files, 'w', encoding='utf8') as f:
                        json.dump(scores, f, indent=6)
                    await ctx.send(f"{member.display_name}'s points have been added!")
                    await member.send('The {} challenge has been marked. You have recieved {} points.'.format(x, chal[x]))
                break
        else:
            await ctx.send("That isn't a challenge. The challenges are listed in .cfall")
            
                     
    @commands.command(aliases=['cfaddp'])
    @commands.has_any_role('Admin', 'Moderator', 'Tutor')
    async def cfaddpoints(self, ctx, member:discord.Member, points, qotdpoints:int=0):
        """Adds points to user directly(ADMIN ONLY)"""
        try:
            file = 'dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id)
            with open(file, encoding='utf8') as f:
                scores = json.load(f)
                scores[str(member.id)]['name'] = member.display_name
                scores[str(member.id)]['current_points'] += int(points)
                scores[str(member.id)]['total_points'] += int(points)
                if(qotdpoints != 0):
                    scores[str(member.id)]['QOTD'] += qotdpoints
            with open(file, 'w', encoding='utf8') as f:
                json.dump(scores, f, indent=6)
            await ctx.send('Points have been added!')
            await member.send('You have obtained {} points.'.format(points))
        except KeyError:
          await ctx.invoke(self.client.get_command('cfaddaccount'), member)
          await ctx.invoke(self.client.get_command('cfaddpoints'), member, points, qotdpoints)

    @commands.command(aliases=['cfaa'])
    @commands.has_any_role('Admin', 'Moderator', 'Tutor')
    async def cfaddaccount(self, ctx, student:discord.Member):
      """This command adds a Challengefest account if it was not added in the waiting room. This also resets the current points of the user so be WARNED.(ADMIN ONLY)"""
      fin = open('dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id), encoding='utf8')
      scores = json.load(fin)
      fin.close()
      scores[student.id] = {'name' : f'{student.display_name}', 'current_points' : 0, 'total_points' : 0, 'QOTD' : 0, 'completed_challenges' : []}
      f = open('dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id), 'w', encoding='utf8')
      json.dump(scores, f, indent=6)
      f.close()
        
    @commands.command(aliases=['pruneall', 'paa'])
    @commands.has_any_role("Moderator", "Admin")
    async def pruneallaccounts(self, ctx): 
      file = 'dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id)
      with open(file, encoding='utf8') as f:
        scores = json.load(f)
      scores_copy = scores.copy() 
      for key, value in scores_copy.items():  
        if(scores[key]['current_points'] == 0):
          del scores[key]
      with open(file,'w', encoding='utf8') as f:
        json.dump(scores, f, indent=6)
      await ctx.send('All inactive accounts have been deleted.')

    @commands.command(aliases=['cfda', 'cfremoveaccount'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfdeleteaccount(self, ctx, student:discord.Member):
        """This command deletes a Challengefest account(ADMIN ONLY)"""
        fin = open('dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id), encoding='utf8')
        scores = json.load(fin)
        fin.close()
        del scores[str(student.id)]
        f = open('dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id), 'w', encoding='utf8')
        json.dump(scores, f, indent=6)
        f.close()
        await ctx.send(f"{student.display_name}'s account was deleted.")
    @commands.command(aliases=['cfac'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfaddchal(self, ctx, chal_name, code_lang, points:int):
        """Creates a new Challenge(ADMIN ONLY)"""
        file = 'dynamic/{}/cf/cfchal.json'.format(ctx.message.guild.id)
        with open(file, encoding='utf8') as f:
            diction = json.load(f)
            diction['{}: {}'.format(code_lang.capitalize(),chal_name)] = points
        with open(file, 'w', encoding='utf8') as f:
            json.dump(diction, f, indent=6)
        await ctx.send('Challenge has been Added!')

    @commands.command(aliases=['cfremovechal', 'cfrc', 'cfdc'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfdeletechal(self, ctx, *, full_chal_name):
        """Removes a challenge(ADMIN ONLY)"""
        file = 'dynamic/{}/cf/cfchal.json'.format(ctx.message.guild.id)
        with open(file, encoding='utf8') as f:
            chal = json.load(f)
        try:
            del chal[full_chal_name]
            with open(file, 'w', encoding='utf8') as f:
                json.dump(chal, f, indent=6)
            await ctx.send('Challenge has been removed.')
        except:
            await ctx.send("That isn't a challenge. Please check all capitalization and spelling")

    

        
    

    @commands.command(aliases=['cfr'])
    @commands.has_any_role('Admin', 'Moderator')
    async def cfreset(self, ctx, name:discord.Member=None):
        """Resets temporary points given during a workshop(ADMIN ONLY)"""
        file = 'dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id)
        if(name == None):
            await ctx.send('Do you want to reset everything?')
            reply = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
            if(reply.content.lower() == 'yes'):
                with open(file, encoding='utf8') as f:
                    scores = json.load(f)
                guild = ctx.message.guild
                for role in guild.roles:
                    if(role.name == 'Student'):
                        break
                for student in role.members:
                    try:
                        scores[str(student.id)]['current_points'] = 0
                    except KeyError:
                      pass                
                with open(file, 'w', encoding='utf8') as f:
                  json.dump(scores, f, indent=6)
        else:
            with open(file, encoding='utf8') as f:
                scores = json.load(f)
            scores[str(name.id)]['current_points'] = 0
            with open(file, encoding='utf8') as f:
                json.dump(scores, f, indent=6)
        
    @commands.command()
    @commands.has_any_role('Admin', 'Moderator')
    async def cfreseteverything(self, ctx):
        """Resets everything. DO NOT USE. Just DONT(ADMIN ONLY)(OBVIOUSLY)"""
        await ctx.send('Do you want to reset everything?')
        reply = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60.0)
        if(reply.content.lower() == 'yes'):
            scores = {}
            for student in ctx.message.guild.get_role(665958098627985450).members:
              scores[student.id] = {'name' : f'{student.display_name}', 'current_points' : 0, 'total_points' : 0, 'QOTD' : 0, 'completed_challenges' : []}      
            f = open('dynamic/{}/cf/cfscores.json'.format(ctx.message.guild.id), 'w', encoding='utf8')
            json.dump(scores, f, indent=6)
            f.close()
        await ctx.send('Everything has been reset')

    async def fake_cftop(self):
      guild = await self.client.fetch_guild(648702233537413120)
      file = 'dynamic/{}/cf/cfscores.json'.format(guild.id)
      with open(file, encoding='utf8') as f:
        scores = json.load(f)
      topscores = {}
      embed = discord.Embed(title='Top {} People'.format(len(scores)), description='The Top People Given By A Certain Amount that Shows their Seasonal Points', color=discord.Color.green())
      for key, diction in scores.items():
          topscores[key] = diction['current_points']
      sort_dict = sorted(topscores.items(), key=lambda x: x[1], reverse=True)
      string = ''
      count = 0
      for i in sort_dict:
          count += 1
          try:
            member = await guild.fetch_member(int(i[0]))
          except:
            continue
          if(member != None):   
              string += '{} - {}\n'.format(member.display_name.title(), i[1]) 
          if(count == len(scores)):
              break
      embed.add_field(name='Top Scorers:', value=string, inline=False)
      return embed

    @tasks.loop(hours=24)
    async def cfbackupscores(self):
      embed = await self.fake_cftop() 
      channel = await self.client.fetch_channel(772155790936768552)
      await channel.send(embed)




    @tasks.loop(seconds=15)
    async def qotd_loop(self):
      date_date = datetime.datetime.utcnow()
      li = str(date_date).split(' ')[1].split(':') 
      if(li[0] == '23' and li[1] == '00'):
        dates = str(date_date).split(' ')[0].split('-')
        datec = f'{dates[2]} {dates[1]} {dates[0]}'
        if(calendar.day_name[datetime.datetime.strptime(datec, '%d %m %Y').weekday()].lower() == 'saturday' or calendar.day_name[datetime.datetime.strptime(datec, '%d %m %Y'.weekday)].lower() == 'sunday'):
          await asyncio.sleep(85560)
        else: 
          channel = await self.client.fetch_channel(754480574634393710)
          guild = await self.client.fetch_guild(648702233537413120)
          role = discord.utils.get(guild.roles, name='Student')
          with open('dynamic/dailyqotd.json') as f:
            link_dict = json.load(f)
          await channel.send('{} QOTD of {}/{}/{}. The category is **{}**\n{}'.format(role.mention, dates[1], dates[2], dates[0], link_dict['category'], link_dict['link']))
          await asyncio.sleep(85500)

                
    @commands.command(aliases=['cql'])
    @commands.has_any_role('Admin', 'Moderator')
    async def change_qotdlink(self, ctx, link, *, message):
      with open('dynamic/dailyqotd.json', 'w') as f:
        json.dump({'link' : link, 'message' : message}, f, indent=6)

      
                

                            
            
    
            

def setup(client):
    client.add_cog(Challengefest(client))
