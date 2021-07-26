#!/usr/bin/env python3

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp

class F1(commands.Cog):
   """
   F1 Data Standings Library

   By Joseph Libasora
   Last updated: 26.Jul.2021, Python 3.8.10
   """
   teams = {
      "Mercedes": "MER",
      "Red Bull": "RBR",
      "McLaren": "MCL",
      "Ferrari": "FER",
      "AlphaTauri": "APT",
      "Aston Martin": "ASM",
      "Alpine": "ALP",
      "Alfa Romeo": "AFR",
      "Williams": "WIL",
      "Haas": "HAS"
   }

   def __init__(self, client):
      self.client = client

   @commands.command()
   async def F1ping(self, ctx):
      await ctx.send("Pong f1.py")

   @commands.command(aliases=["WDC"])
   async def wdc(self, ctx):
      """Returns F1 World Driver's Championship Standings"""

      wdc = await F1.getWDC()
      embed = discord.Embed(
         title="F1 World Driver's Championship Standings",
         colour=discord.Colour.red()
      )

      for driver in wdc:
         code = driver[1].split()[1][:3].upper()
         if code == "SCH":
            code = "MSC"
         embed.add_field(name=f"#{driver[0]} {code}", value=f"> {driver[1]}\n> {driver[3]}\n> {driver[4]}", inline=True)
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from skysports.com/f1/standings")
      embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
      await ctx.send(embed=embed)

   @commands.command(aliases=["WCC"])
   async def wcc(self, ctx):
      """Returns F1 World Constructor's Championship Standings"""

      wcc = await F1.getWCC()
      embed = discord.Embed(
         title="F1 World Constructor's Championship Standings",
         colour=discord.Colour.red()
      )

      for team in wcc:
         code = self.teams[team[1]]
         embed.add_field(name=f"#{team[0]} {code}", value=f"> {team[1]}\n> {team[2]}", inline=True)
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from skysports.com/f1/standings")
      embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
      await ctx.send(embed=embed)

   @staticmethod
   async def getWDC():
      """Async web request F1 World Driver's Championship standings"""

      url = "https://www.skysports.com/f1/standings"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(url) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               wdc = []
               
               for driver in soup.find_all("table")[0].find_all("tr")[1:]:
                  wdc.append([driverdata.text.strip() for driverdata in driver.find_all("td")])
               return wdc
            else:
               return "Warning, web error occured. Code: {web_resp.status}"
      return "Warning, request timeout"

   @staticmethod
   async def getWCC():
      """Async web request F1 World Constructor's Championship standings"""

      url = "https://www.skysports.com/f1/standings"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(url) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               wcc = []
               
               for team in soup.find_all("table")[1].find_all("tr")[1:]:
                  wcc.append([teamdata.text.strip() for teamdata in team.find_all("td")])
               return wcc
            else:
               return "Warning, web error occured. Code: {web_resp.status}"
      return "Warning, request timeout"


def setup(client):
   client.add_cog(F1(client))


async def asyncTest():
   """Local async testing"""
   print("testing async local functions")

   # print(await F1.getWDC())
   # print(await F1.getWCC())

if __name__ == "__main__":
   import asyncio
   asyncio.run(asyncTest())
