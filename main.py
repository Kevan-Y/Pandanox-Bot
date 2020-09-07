import discord
from discord.ext import commands
from decouple import config

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")

intial_extensions = ['cogs.basic', 'cogs.profile',
                     'cogs.hangman', 'cogs.youtube', 'cogs.weather', 'cogs.music', 'cogs.moderation']


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('!help'))
    print("Bot is ready.")
    for extension in intial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Error loading: {extension} {e}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Invalide commands, please type `!help` for the commands {error}')

bot.run(config('TOKEN'))
