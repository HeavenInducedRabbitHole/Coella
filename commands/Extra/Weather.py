import discord
from discord.ext import commands
import aiohttp

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = 'b3d327703c9e05404977848278ea1d4c'
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather'

    @commands.Cog.listener()
    async def on_ready(self):
        print("Weather cog is ready")

    @commands.command()
    async def weather(self, ctx, *, city: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}?q={city}&appid={self.api_key}') as response:
                weather_data = await response.json()
                if weather_data['cod'] == 200:  # if request was successful
                    city = weather_data['name']
                    country = weather_data['sys']['country']
                    temperature = weather_data['main']['temp'] - 273.15  # convert from Kelvin to Celsius
                    humidity = weather_data['main']['humidity']
                    pressure = weather_data['main']['pressure']
                    wind_speed = weather_data['wind']['speed']
                    description = weather_data['weather'][0]['description']

                    embed = discord.Embed(
                        title=f"Weather in {city}, {country}",
                        description=description,
                        color=discord.Color.teal()
                    )

                    embed.add_field(name="Temperature", value=f"{temperature:.2f}°C")
                    embed.add_field(name="Humidity", value=f"{humidity}%")
                    embed.add_field(name="Pressure", value=f"{pressure} hPa")
                    embed.add_field(name="Wind Speed", value=f"{wind_speed} m/s")

                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"I couldn't get the weather for {city}. Please make sure it's spelled correctly.")

async def setup(client):
    await client.add_cog(Weather(client))
