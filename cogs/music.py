import discord
from discord.ext import commands
from discord import utils
import lavalink


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node(
            'localhost', 8080, 'testing', 'eu', 'music-node')
        self.bot.add_listener(
            self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command()
    async def join(self, ctx):
        member = utils.find(lambda mb: mb.id ==
                            ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            voice_channel = member.voice.channel
            player = self.bot.music.player_manager.create(
                ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, voice_channel.id)
            else:
                embed = discord.Embed()
                embed.description = 'Music already connected to a channel!'
                await ctx.channel.send(embed=embed)

    @commands.command()
    async def out(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        embed = discord.Embed()
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed.description = 'Not connected.'
            return await ctx.send(embed=embed)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed.description = 'You\'re not in my voicechannel!'
            return await ctx.send(embed=embed)

        await self.connect_to(ctx.guild.id, None)

    @commands.command()
    async def skip(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        embed = discord.Embed()
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed.description = 'You\'re not in my voicechannel!'
            return await ctx.send(embed=embed)
        await player.skip()

    @commands.command()
    async def play(self, ctx, *, query):
        member = utils.find(lambda mb: mb.id ==
                            ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            voice_channel = member.voice.channel
            player = self.bot.music.player_manager.create(
                ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, voice_channel.id)

            try:
                player = self.bot.music.player_manager.get(ctx.guild.id)
                if(player.channel_id == str(member.voice.channel.id) or not player.is_connected):
                    query = f'ytsearch:{query}'
                    results = await player.node.get_tracks(query)
                    songs = results['tracks'][0:5]
                    i = 0
                    query_results = ''
                    for song in songs:
                        i = i + 1
                        query_results = query_results + \
                            f'{i}. [{song["info"]["title"]}]({song["info"]["uri"]})\n'
                    embed = discord.Embed()
                    embed.description = query_results
                    await ctx.channel.send(embed=embed)

                    def check(m):
                        return m.author.id == ctx.author.id

                    response = await self.bot.wait_for('message', check=check)
                    song = songs[int(response.content)-1]

                    player.add(requester=ctx.author.id, track=song)
                    if not player.is_playing:
                        await player.play()
                else:
                    embed = discord.Embed()
                    embed.description = 'Music already playing in a channel!'
                    await ctx.channel.send(embed=embed)
            except Exception as e:
                print(e)

    @commands.command()
    async def queue(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        queue = player.queue
        queur_list = ''
        i = 0
        for song in queue:
            i = i + 1
            queur_list = queur_list + \
                f'{i}. [{song["title"]}]({song["uri"]})\n'

        embed = discord.Embed()
        if i == 0:
            embed.description = f'[{player.current["title"]}]({player.current["uri"]})\n'
            embed.title = 'Playing'
        else:
            embed.description = queur_list + f'\nSong in queue: {i}'
            embed.title = 'Queue'
        await ctx.channel.send(embed=embed)

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @ commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        embed = discord.Embed()
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            embed.description = 'Not connected.'
            return await ctx.send(embed=embed)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            embed.description = 'You\'re not in my voicechannel!'
            return await ctx.send(embed=embed)

        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        embed.description = '*⃣ | Disconnected.'
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
    print("Music is loaded")
