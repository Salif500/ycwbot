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
        guild = ctx.message.guild
        voice_channel_cur = []
        for voice_channel in guild.voice_channels:
          if(voice_channel.members):
            voice_channel_cur.append(voice_channel)
        for voice_channel in voice_channel_cur:
            for member in voice_channel.members:
              await member.move_to(channel)

    @commands.command(aliases=['move_students', 'startClass'])
    @commands.has_any_role("Admin", "Moderator")
    async def start_class(self, ctx):
        """Moves all students to designated voice channels(ADMINS ONLY)(DEPRECATED)"""
        await self.client.wait_until_ready()
        moved = False
        voice_channel_cur = []
        guild = ctx.message.guild
        for voice_channel in guild.voice_channels:
          if(voice_channel.members):
            voice_channel_cur.append(voice_channel)
        for voice_channel in voice_channel_cur:
          for member in voice_channel.members:
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
                    

    @commands.command()
    @commands.has_any_role("Admin", "Moderator")
    async def disconnect_all(self, ctx):
        """Disconnects all members from all channels(ADMINS ONLY)"""
        guild = ctx.message.guild
        channel = None
        voice_channel_cur = []
        for voice_channel in guild.voice_channels:
          if(voice_channel.members):
            voice_channel_cur.append(voice_channel)
        for voice_channel in voice_channel_cur:
            for member in voice_channel.members:
              await member.move_to(channel)
            


    




def setup(client):
    client.add_cog(Voice(client))
