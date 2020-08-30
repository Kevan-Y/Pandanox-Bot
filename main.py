import discord
from discord.ext import commands
from decouple import config

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

intial_extensions = ['cogs.basic', 'cogs.profile',
                     'cogs.hangman', 'cogs.youtube', 'cogs.weather', ]


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('!help'))
    print("Bot is ready.")

if __name__ == '__main__':
    for extension in intial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Error loading: {extension}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalide commands, please type `!help` for the commands')

bot.run(config('TOKEN'))
