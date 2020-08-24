import discord
from discord.ext import commands

class Voice(commands.Cog):
    """All commands relating to voice channels(ADMINS ONLY)"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def move_all(self, ctx, *, channel: discord.VoiceChannel):
        """Moves all members to a certain voice channel(ADMINS ONLY)"""
        for guild in self.client.guilds:
            for member in guild.members:
                if(member.status != discord.Status.offline):
                    try:
                        await member.move_to(channel)
                    except:
                        pass

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def move_students(self, ctx):
        """Moves all students to designated voice channels(ADMINS ONLY)(DEPRECATED)"""
        await self.client.wait_until_ready()
        moved = False
        for guild in self.client.guilds:
            for member in guild.members:
                if(member.status != discord.Status.offline):
                    try:
                        for role in member.roles:
                            if(str(role) == "Python"):
                                channel = discord.utils.get(guild.voice_channels, name='python')
                                moved = True
                            elif(str(role) == "Scratch"):
                                channel = discord.utils.get(guild.voice_channels, name='scratch')
                                moved = True
                            elif(str(role) == "HTML"):
                                channel = discord.utils.get(guild.voice_channels, name='html')
                                moved = True
                            if(moved == False):
                                channel = discord.utils.get(guild.voice_channels, name='living-room')
                        await member.move_to(channel)
                    except:
                        pass

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def disconnect_all(self, ctx):
        """Disconnects all members from all channels(ADMINS ONLY)"""
        for guild in self.client.guilds:
            for member in guild.members:
                if(member.status != discord.Status.offline):
                    try:
                        await member.move_to(channel=None)
                    except:
                        pass
            


    




def setup(client):
    client.add_cog(Voice(client))
