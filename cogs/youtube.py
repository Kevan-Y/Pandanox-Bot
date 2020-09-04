from discord.ext import commands
from youtube_search import YoutubeSearch


class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['youtubeSearch'])
    async def youtube_search(self, ctx, *, search):
        results = YoutubeSearch(f'{search}', max_results=1).to_dict()
        await ctx.send(f'https://www.youtube.com/watch?v={results[0]["id"]}')


def setup(bot):
    bot.add_cog(Youtube(bot))
    print("Youtube is loaded")
