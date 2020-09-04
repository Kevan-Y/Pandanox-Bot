import Game.hangmanUtilities as hm
from discord.ext import commands


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['HANGMAN'])
    async def hangman(self, ctx):
        game = hm.Hangman()
        await game.startGame(ctx, self.bot)


def setup(bot):
    bot.add_cog(Hangman(bot))
    print("Hangman is loaded")
