import re
import random
import json
import discord
import asyncio


class Hangman:
    def word_to_emoji(self, word):
        newArray = []
        for i in word:
            if i != ' ':
                newArray.append('\U0001F535')
            else:
                newArray.append('\u25AA\uFE0F')

        return newArray

    def life_to_emoji(self, numLife):
        newString = ""
        for i in range(0, numLife):
            newString += '\u2764\uFE0F'
        return newString

    def convert(self, stringArr):
        str1 = " "
        return(str1.join(stringArr))

    def character_to_emoji(self, letter):
        switcher = {
            'a': '\U0001F1E6',
            'b': '\U0001F1E7',
            'c': '\U0001F1E8',
            'd': '\U0001F1E9',
            'e': '\U0001F1EA',
            'f': '\U0001F1EB',
            'g': '\U0001F1EC',
            'h': '\U0001F1ED',
            'i': '\U0001F1EE',
            'j': '\U0001F1EF',
            'k': '\U0001F1F0',
            'l': '\U0001F1F1',
            'm': '\U0001F1F2',
            'n': '\U0001F1F3',
            'o': '\U0001F1F4',
            'p': '\U0001F1F5',
            'q': '\U0001F1F6',
            'r': '\U0001F1F7',
            's': '\U0001F1F8',
            't': '\U0001F1F9',
            'u': '\U0001F1FA',
            'v': '\U0001F1FB',
            'w': '\U0001F1FC',
            'x': '\U0001F1FD',
            'y': '\U0001F1FE',
            'z': '\U0001F1FF',
        }
        return switcher.get(letter.lower(), '\u25AA\uFE0F')

    def checkWord(self, content, letterFound, wordArray, wordArraySecret, life):
        msg = ""
        numCorrect = 0
        for j in letterFound:
            if j == self.character_to_emoji(content.lower()):
                return f'`{content.upper()}` is already guessed.', life, False
        for i in range(len(wordArray)):
            if wordArray[i].lower() == content.lower():
                wordArraySecret[i] = self.character_to_emoji(
                    wordArray[i])
                if(msg == ""):
                    letterFound.append(self.character_to_emoji(content))
                msg = f'`{content.upper()}` Correct Guess!'
            elif i == len(wordArray)-1 and wordArray[i].lower() != content.lower() and msg == "":
                letterFound.append(self.character_to_emoji(content))
                msg = f'`{content.upper()}` Wrong Guess!'
                life -= 1
            if self.character_to_emoji(wordArray[i]) == wordArraySecret[i]:
                numCorrect += 1
                if numCorrect == len(wordArray):
                    return 'You Win!', life, True

        if life != 0:
            return msg, life, False
        else:
            return 'Game Over!', life, True

    async def startGame(self, ctx, bot):
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
                wordArraySecret = self.word_to_emoji(wordArray)

                embedGame = discord.Embed()
                embedGame.add_field(
                    name='User', value=f'{user.name}', inline=True)
                embedGame.add_field(
                    name='\u200B\n', value='\u200B\n', inline=True)
                embedGame.add_field(
                    name='Category', value='Countries', inline=True)
                embedGame.add_field(
                    name='Word', value=f'{self.convert(wordArraySecret)}', inline=False)
                embedGame.add_field(
                    name='Life', value=f'{self.life_to_emoji(life)}', inline=False)
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

                    msgBack, life, win = self.checkWord(res.content, letterFound,
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
                            name='Word', value=f'{self.convert(wordArraySecret)}', inline=False)
                        embedInGame.add_field(
                            name='Life', value=f'{self.life_to_emoji(life)}', inline=False)
                        embedInGame.add_field(
                            name='Word used', value=f'{self.convert(letterFound)}', inline=False)
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
                wordArraySecret = self.word_to_emoji(wordArray)

                embedGame = discord.Embed()
                embedGame.add_field(
                    name='User', value=f'{user.name}', inline=True)
                embedGame.add_field(
                    name='\u200B\n', value='\u200B\n', inline=True)
                embedGame.add_field(
                    name='Category', value='Animals', inline=True)
                embedGame.add_field(
                    name='Word', value=f'{self.convert(wordArraySecret)}', inline=False)
                embedGame.add_field(
                    name='Life', value=f'{self.life_to_emoji(life)}', inline=False)
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

                    msgBack, life, win = self.checkWord(res.content, letterFound,
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
                            name='Word', value=f'{self.convert(wordArraySecret)}', inline=False)
                        embedInGame.add_field(
                            name='Life', value=f'{self.life_to_emoji(life)}', inline=False)
                        embedInGame.add_field(
                            name='Word used', value=f'{self.convert(letterFound)}', inline=False)
                        embedInGame.add_field(
                            name='Info', value=f'{msgBack}\nType /stop to stop the game', inline=False)

                    await msgGame.edit(embed=embedInGame)
