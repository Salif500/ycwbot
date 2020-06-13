import discord
from discord.ext import commands

class Voice(commands.Cog):
    """This is all commands relating to voice channels, including disconnecting and moving members."""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def move_all(self, ctx, *, channel: discord.VoiceChannel):
        """Moves all members to a certain voice channel given the channel. Admins Only"""
        for guild in self.client.guilds:
            for member in guild.members:
                if(member.status != discord.Status.offline):
                    try:
                        await member.move_to(channel)
                    except:
                        print("{} is not connected\n".format(member))

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def move_students(self, ctx):
        """Moves all students to designated voice channel"""
        for guild in self.client.guilds:
            for member in guild.members:
                if(member.status != discord.Status.offline):
                    try:
                        for role in member.roles:
                            if(str(role) == "Python G1"):
                                channel = discord.utils.get(guild.voice_channels, name='advanced')
                            elif(str(role) == "Python G2"):
                                channel = discord.utils.get(guild.voice_channels, name='intermediate')
                            elif(str(role) == "Python G3"):
                                channel = discord.utils.get(guild.voice_channels, name='beginning')
                            elif(str(role) == "HTML G2"):
                                channel = discord.utils.get(guild.voice_channels, name='beginning')
                            elif(str(role) == "HTML G1"):
                                channel = discord.utils.get(guild.voice_channels, name='intermediate')
                        await member.move_to(channel)
                    except:
                        print("{} is not connected\n".format(member))

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def disconnect_all(self, ctx):
        """Disconnects all members from current channel"""
        for guild in self.client.guilds:
            for member in guild.members:
                if(member.status != discord.Status.offline):
                    try:
                        await member.move_to(channel=None)
                    except:
                        print("{} is not connected\n".format(member))
            


    




def setup(client):
    client.add_cog(Voice(client))
