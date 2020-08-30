import discord
import requests
import datetime
from discord.ext import commands


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, city):
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


def setup(bot):
    bot.add_cog(Weather(bot))
    print("Weather is loaded")
