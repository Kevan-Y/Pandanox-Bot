import discord
import asyncio
from discord.ext import commands
import re
import json
import hangmanUtilities as hg
import random
from decouple import config

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('!help'))
    print("Bot is ready.")

@bot.command(aliases=['PING'])
async def ping(ctx):
    embed = discord.Embed(
        title='Pong',
        description=f'{round (bot.latency * 1000)} ms!',
        color=0xff0000
    )
    embed.set_author(name="Pandanox Bot", icon_url=bot.user.avatar_url)
    embed.set_footer(text="By Pandanox")

    await ctx.send(embed=embed)

@bot.command(aliases=['hangman'])
async def play_hangman(ctx):
    with open('./data.json') as f:
        data = json.load(f)
    embed = discord.Embed(
        title='Hangman',
        color=0x8000ff
    )
    embed.add_field(name='Category',
                    value='1\ufe0f\u20e3 Countries\n 2\ufe0f\u20e3 Foods')
    embed.set_thumbnail(url=bot.user.avatar_url)

    embed.set_footer(text="By Pandanox")

    msg = await ctx.message.channel.send(embed=embed)

    await msg.add_reaction(emoji="1\ufe0f\u20e3")
    await msg.add_reaction(emoji="2\ufe0f\u20e3")

    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in ['1\ufe0f\u20e3', '2\ufe0f\u20e3']

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title='Hangman',
            description='Game timed out.',
            color=0x8000ff
        )
        await ctx.send(embed=embed)
    else:
        if reaction.emoji == '1\ufe0f\u20e3':
            wordList = data['countries']
            num = random.randint(0, len(wordList))
            wordArray = list(wordList[num])
            life = 6
            letterFound = []
            win = False
            wordArraySecret = hg.word_to_emoji(wordArray)

            embedGame = discord.Embed()
            embedGame.add_field(name='User', value=f'{user.name}', inline=True)
            embedGame.add_field(name='\u200B\n', value='\u200B\n', inline=True)
            embedGame.add_field(
                name='Category', value='Countries', inline=True)
            embedGame.add_field(
                name='Word', value=f'{hg.convert(wordArraySecret)}', inline=False)
            embedGame.add_field(
                name='Life', value=f'{hg.life_to_emoji(life)}', inline=False)
            embedGame.add_field(
                name='How To Play', value='Type any letter `"A"`to guess', inline=False)
            embedGame.add_field(
                name='Info', value='Type /stop to stop the game', inline=False)

            msgGame = await ctx.send(embed=embedGame)

            while win != True:
                def checkmsg(msg):
                    if(msg.content == "/stop"):
                        return True
                    else:
                        return re.match("^[A-Za-z]$", msg.content) and msg.channel == ctx.channel
                res = await bot.wait_for('message', check=checkmsg)

                if(res.content == "/stop"):

                    embedEnd = discord.Embed(
                        title='Game Ended!', description=f'By{res.author.name}#{res.author.discriminator}', color=0xff0000)
                    await msgGame.edit(embed=embedEnd)
                    break

                msgBack, life, win = hg.checkWord(res.content, letterFound,
                                                  wordArray, wordArraySecret, life)

                if(life == 0):
                    embedInGame = discord.Embed(
                        title='Game Over', description=f'Word: {"".join(wordArray)}.', color=0xfc0303)
                    embedInGame.add_field(
                        name='User', value=f'{res.author.name}#{res.author.discriminator}', inline=True)
                    embedInGame.add_field(
                        name='\u200B\n', value='\u200B\n', inline=True)
                    embedInGame.add_field(
                        name='Category', value='Countries', inline=True)
                    embedInGame.set_image(
                        url="https://thumbs.gfycat.com/PhonyLikelyCatfish-size_restricted.gif")
                elif(win == True):
                    embedInGame = discord.Embed(
                        title='Winner', description=f'Word: {"".join(wordArray)}.', color=0xfcf003)
                    embedInGame.add_field(
                        name='User', value=f'{res.author.name}#{res.author.discriminator}', inline=True)
                    embedInGame.add_field(
                        name='\u200B\n', value='\u200B\n', inline=True)
                    embedInGame.add_field(
                        name='Category', value='Countries', inline=True)
                    embedInGame.set_image(
                        url="https://pa1.narvii.com/6342/20d93a11439634f60d3e8088f4ecbf78c21dc164_hq.gif")
                else:
                    embedInGame = discord.Embed()
                    embedInGame.add_field(
                        name='User', value=f'{res.author.name}#{res.author.discriminator}', inline=True)
                    embedInGame.add_field(
                        name='\u200B\n', value='\u200B\n', inline=True)
                    embedInGame.add_field(
                        name='Category', value='Countries', inline=True)
                    embedInGame.add_field(
                        name='Word', value=f'{hg.convert(wordArraySecret)}', inline=False)
                    embedInGame.add_field(
                        name='Life', value=f'{hg.life_to_emoji(life)}', inline=False)
                    embedInGame.add_field(
                        name='Word used', value=f'{hg.convert(letterFound)}', inline=False)
                    embedInGame.add_field(
                        name='Info', value=f'{msgBack}\nType /stop to stop the game', inline=False)
                await msgGame.edit(embed=embedInGame)

        else:
            wordList = data['animals']
            num = random.randint(0, len(wordList))
            wordArray = list(wordList[num])
            life = 6
            letterFound = []
            win = False
            wordArraySecret = hg.word_to_emoji(wordArray)

            embedGame = discord.Embed()
            embedGame.add_field(name='User', value=f'{user.name}', inline=True)
            embedGame.add_field(name='\u200B\n', value='\u200B\n', inline=True)
            embedGame.add_field(
                name='Category', value='Animals', inline=True)
            embedGame.add_field(
                name='Word', value=f'{hg.convert(wordArraySecret)}', inline=False)
            embedGame.add_field(
                name='Life', value=f'{hg.life_to_emoji(life)}', inline=False)
            embedGame.add_field(
                name='How To Play', value='Type any letter `"A"`to guess', inline=False)
            embedGame.add_field(
                name='Info', value='Type /stop to stop the game', inline=False)

            msgGame = await ctx.send(embed=embedGame)

            while win != True:
                def checkmsg(msg):
                    if(msg.content == "/stop"):
                        return True
                    else:
                        return re.match("^[A-Za-z]$", msg.content) and msg.channel == ctx.channel
                res = await bot.wait_for('message', check=checkmsg)

                if(res.content == "/stop"):

                    embedEnd = discord.Embed(
                        title='Game Ended!', description=f'By{res.author.name}#{res.author.discriminator}', color=0xff0000)
                    await msgGame.edit(embed=embedEnd)
                    break

                msgBack, life, win = hg.checkWord(res.content, letterFound,
                                                  wordArray, wordArraySecret, life)

                if(life == 0):
                    embedInGame = discord.Embed(
                        title='Game Over', description=f'Word: {"".join(wordArray)}.', color=0xfc0303)
                    embedInGame.add_field(
                        name='User', value=f'{res.author.name}#{res.author.discriminator}', inline=True)
                    embedInGame.add_field(
                        name='\u200B\n', value='\u200B\n', inline=True)
                    embedInGame.add_field(
                        name='Category', value='Countries', inline=True)
                    embedInGame.set_image(
                        url="https://thumbs.gfycat.com/PhonyLikelyCatfish-size_restricted.gif")
                elif(win == True):
                    embedInGame = discord.Embed(
                        title='Winner', description=f'Word: {"".join(wordArray)}.', color=0xfcf003)
                    embedInGame.add_field(
                        name='User', value=f'{res.author.name}#{res.author.discriminator}', inline=True)
                    embedInGame.add_field(
                        name='\u200B\n', value='\u200B\n', inline=True)
                    embedInGame.add_field(
                        name='Category', value='Countries', inline=True)
                    embedInGame.set_image(
                        url="https://pa1.narvii.com/6342/20d93a11439634f60d3e8088f4ecbf78c21dc164_hq.gif")
                else:
                    embedInGame = discord.Embed()
                    embedInGame.add_field(
                        name='User', value=f'{res.author.name}#{res.author.discriminator}', inline=True)
                    embedInGame.add_field(
                        name='\u200B\n', value='\u200B\n', inline=True)
                    embedInGame.add_field(
                        name='Category', value='Countries', inline=True)
                    embedInGame.add_field(
                        name='Word', value=f'{hg.convert(wordArraySecret)}', inline=False)
                    embedInGame.add_field(
                        name='Life', value=f'{hg.life_to_emoji(life)}', inline=False)
                    embedInGame.add_field(
                        name='Word used', value=f'{hg.convert(letterFound)}', inline=False)
                    embedInGame.add_field(
                        name='Info', value=f'{msgBack}\nType /stop to stop the game', inline=False)
                await msgGame.edit(embed=embedInGame)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalide commands, please type `!help` for the commands')

bot.run(config('TOKEN'))
