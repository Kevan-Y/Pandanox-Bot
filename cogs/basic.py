import discord
import re
import random
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['PING'])
    async def ping(self, ctx):
        embed = discord.Embed(
            title='Pong',
            description=f'{round (self.bot.latency * 1000)} ms!',
            color=0xff0000
        )
        embed.set_author(name="Pandanox Bot",
                         icon_url=self.bot.user.avatar_url)
        embed.set_footer(text="By Pandanox")

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Pandanox Bot Help", color=0x001eff)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(
            name="!help", value="Show every commands available.", inline=False)
        embed.add_field(name="!ping", value="Get the ping.", inline=False)
        embed.add_field(name="!hangman",
                        value="Start a hangman game.", inline=False)
        embed.add_field(
            name="!profile", value="`!profile @Tag`\nGet Tagged profile information.\n`!profile`\nGet current profile information.", inline=False)
        embed.add_field(
            name="!random", value="`!random <number> to <number>`\nGet random number from a range.\n`!random <number>`\nGet random number from 0 to number specified.", inline=True)
        embed.add_field(name="!youtubeSearch",
                        value='`!youtubeSearch <name>` Return the top video of the search.', inline=False)
        embed.add_field(
            name="!weather", value='`!weather <city>` Return forecast of the city mentioned.', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['random'])
    async def _random(self, ctx, *, num):
        descs = ""
        if re.match("^\d+$", num):
            descs = f'Your magic number is {str(random.randint(int(0), int(num)))}'
        elif(re.match("^(\d+\s+(to|TO){1}\s+\d+)$", num)):
            ranges = num.split('to')
            if (int(ranges[0]) > int(ranges[1])):
                descs = "Error Command syntax: number 2 should be greater than number 1."
            else:
                descs = f'Your magic number is {str(random.randint(int(ranges[0]), int(ranges[1])))}'
        else:
            descs = "Error Command syntax: !random <number 1> to <number 2>"

        embed = discord.Embed(
            title='Random',
            description=descs,
            color=0x00fbff
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text="By Pandanox")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Basic(bot))
    print("Basic is loaded")
