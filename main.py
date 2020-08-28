import discord
import asyncio
import re
import json
import random
import datetime
import hangmanUtilities as hg
import requests

from youtube_search import YoutubeSearch
from discord.ext import commands
from decouple import config

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")


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


@bot.command(aliases=['HANGMAN'])
async def hangman(ctx):
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


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Pandanox Bot Help", color=0x001eff)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(
        name="!help", value="Show every commands available.", inline=False)
    embed.add_field(name="!ping", value="Get the ping.", inline=False)
    embed.add_field(name="!hangman",
                    value="Start a hangman game.", inline=False)
    embed.add_field(
        name="!profile", value="`!profile @Tag`\nGet Tagged profile information.\n`!profile`\nGet current profile information.", inline=False)
    embed.add_field(name="!random", value="`!random <number> to <number>`\nGet random number from a range.\n`!random <number>`\nGet random number from 0 to number specified.", inline=True)
    embed.add_field(name="!youtubeSearch",
                    value='`!youtubeSearch <name>` Return the top video of the search.', inline=False)
    embed.add_field(
        name="!weather", value='`!weather <city>` Return forecast of the city mentioned.', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def profile(ctx, user: discord.Member = None):
    user = ctx.author if not user else user
    roles = [role for role in user.roles]

    def status_to_emoji(status):
        switch = {
            'online': '🟢',
            'offline': '⚫',
            'idle': '🟡',
            'dnd': '⛔',
        }
        return switch.get(status.value.lower(), '⚫')

    def dateDiff(first, second):
        dayDiffInSecond = (first-second).total_seconds()
        year = divmod(dayDiffInSecond, 3.154e+7)
        months = divmod(year[1], 2.628e+6)
        days = divmod(months[1], 86400)
        return int(year[0]), int(months[0]), int(days[0])

    year, months, days = dateDiff(datetime.datetime.now(), user.created_at)

    embed = discord.Embed(title=f'{user}', color=user.color.value)
    embed.add_field(name="User Information",
                    value=f'Created: {year} years, {months}months, {days}days ago\nProfile<@{user.id}>\nID: {user.id}', inline=False)

    year, months, days = dateDiff(datetime.datetime.now(), user.joined_at)

    embed.add_field(name="Menber Information",
                    value=f'Joined: {year} years, {months}months, {days}days ago\nRoles{" ".join(role.mention for role in roles)}', inline=False)
    embed.add_field(name='Top Role', value=f'{user.top_role.mention}')
    embed.add_field(
        name='Type', value=f'{"🟢" if user.bot == False else "🔴"} User\n{"🟢" if user.bot else "🔴"} Bot', inline=False)
    embed.add_field(
        name="Status", value=f'{status_to_emoji(user.desktop_status)} Destop\n{status_to_emoji(user.web_status)} Web\n{status_to_emoji(user.mobile_status)} Mobile')

    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(
        text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command(aliases=['youtubeSearch'])
async def youtube_search(ctx, *, search):
    results = YoutubeSearch(f'{search}', max_results=1).to_dict()
    await ctx.send(f'https://www.youtube.com/watch?v={results[0]["id"]}')


@bot.command(aliases=['random'])
async def _random(ctx, *, num):
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
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="By Pandanox")

    await ctx.send(embed=embed)


@bot.command()
async def weather(ctx, *, city):
    url = "https://www.metaweather.com/api/"
    location_search_url = f'{url}location/search/'
    location_url = f'{url}location/'
    req = requests.get(location_search_url, params={'query': city})
    data_to_json = req.json()

    if not data_to_json:
        await ctx.send(f'"{city}" Location not found.')
    else:
        location_id = data_to_json[0]['woeid']
        r = requests.get(f'{location_url}{location_id}/')
        data = r.json()
        weather = data['consolidated_weather'][0]
        embed = discord.Embed(title=f'{data["title"]} Weather',
                              description=f'{datetime.datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%A %I:%M %p")}')
        embed.set_thumbnail(
            url=f'https://www.metaweather.com/static/img/weather/png/{weather["weather_state_abbr"]}.png')

        embed.add_field(
            name='Temperature', value=f'Current: {int(round((float(weather["the_temp"])),0))}°C\nMax: {int(round(float(weather["max_temp"]),0))}°C\nMin: {int(round(float(weather["min_temp"]),0))}°C', inline=False)
        embed.add_field(
            name='Wind', value=f'Wind speed: {round(float(weather["wind_speed"]),2)} mph\nDirection: {weather["wind_direction_compass"]}', inline=True)
        embed.add_field(name='More Info',
                        value=f'Air pressure: {weather["air_pressure"]}mb\nHumidity: {weather["humidity"]}%\nVisibility: {round(float(weather["visibility"]),2)} miles', inline=True)
        embed.add_field(
            name='Sun rise/Set', value=f'Sun rise: {datetime.datetime.strptime(data["sun_rise"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%I:%M %p")}\nSun set: {datetime.datetime.strptime(data["sun_set"], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%I:%M %p")}', inline=False)
        embed.add_field(
            name='Timezone', value=data["timezone"], inline=False)
        await ctx.send(embed=embed)

bot.run(config('TOKEN'))
