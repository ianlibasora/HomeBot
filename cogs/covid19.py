#!/usr/bin/env python3

import discord
from discord.ext import commands
import aiohttp
import json

class Covid19(commands.Cog):
   """
   Ireland COVID-19 Data Request Library

   By Joseph Libasora
   Last updated: 10.Aug.2021
   """

   def __init__(self, client):
      self.client = client

   @commands.command()
   async def c19ping(self, ctx):
      await ctx.send("Pong covid19.py")

   @commands.command(aliases=["COVID", "covid19", "COVID19", "covid-19","COVID-19", "c19", "C19", "corona", "CORONA"])
   async def covid(self, ctx):
      """Returns Ireland New COVID-19 Cases Data"""

      data = await Covid19.getCovidData()
      embed = discord.Embed(
         colour=discord.Colour.gold()
      )

      embed.add_field(name="New COVID-19 Cases", value=f"> {data['ConfirmedCovidCases']}", inline=True)
      embed.add_field(name="New COVID-19 Deaths", value=f"> {data['ConfirmedCovidDeaths']}", inline=True)

      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from Ireland COVID-19 Data Hub")
      embed.set_author(name="Ireland COVID-19 Data", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/c19.png")
      await ctx.send(embed=embed)

   @staticmethod
   async def getCovidData():
      """Async data request Ireland COVID-19 data"""

      url = "https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Covid19StatisticsProfileHPSCIrelandView/FeatureServer/0/query?where=1%3D1&outFields=ConfirmedCovidCases,ConfirmedCovidDeaths&returnGeometry=false&outSR=4326&f=json"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(url) as web_resp:
            if web_resp.status == 200:
               dataJSON = json.loads(await web_resp.text())
               return dataJSON["features"][0]["attributes"]
            else:
               return "Warning, web error occured. Code: {web_resp.status}"
      return "Warning, request timeout"


def setup(client):
   client.add_cog(Covid19(client))


async def asyncTest():
   """Local async testing"""
   print("testing async local functions")
   # print(await Covid19.getCovidData())

if __name__ == "__main__":
   import asyncio
   asyncio.run(asyncTest())
