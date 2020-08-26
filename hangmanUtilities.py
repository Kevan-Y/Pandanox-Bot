import re
import random

def word_to_emoji(word):
    newArray = []
    for i in word:
        if i != ' ':
            newArray.append('\U0001F535')
        else:
            newArray.append('\u25AA\uFE0F')

    return newArray
            
def life_to_emoji(numLife):
    newString = ""
    for i in range(0, numLife):
        newString += '\u2764\uFE0F'
    return newString

def convert(s):
    str1 = " "
    return(str1.join(s))

def character_to_emoji(letter):
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
    return switcher.get(letter.lower(),'\u25AA\uFE0F')

def checkWord(content, letterFound, wordArray, wordArraySecret, life):
    msg = ""
    numCorrect = 0
    for j in letterFound:
        if j == character_to_emoji(content.lower()):
            return f'`{content.upper()}` is already guessed.', life, False
    for i in range(len(wordArray)):
        if wordArray[i].lower() == content.lower():
            wordArraySecret[i] = character_to_emoji(
                wordArray[i])
            if(msg == ""):
                letterFound.append(character_to_emoji(content))
            msg = f'`{content.upper()}` Correct Guess!'
        elif i == len(wordArray)-1 and wordArray[i].lower() != content.lower() and msg == "":
            letterFound.append(character_to_emoji(content))
            msg = f'`{content.upper()}` Wrong Guess!'
            life -= 1
        if character_to_emoji(wordArray[i]) == wordArraySecret[i]:
            numCorrect += 1
            if numCorrect == len(wordArray):
                return 'You Win!', life, True

    if life != 0:
        return msg, life, False
    else:
        return 'Game Over!', life, True
