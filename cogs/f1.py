#!/usr/bin/env python3

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp
import datetime

class F1(commands.Cog):
   """
   F1 Data Standings Library

   By Joseph Libasora
   Last updated: 26.Jul.2021
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
      """Returns F1 World Drivers Championship Standings"""

      wdc = await F1.getWDC()
      embed = discord.Embed(
         colour=discord.Colour.red()
      )

      for driver in wdc:
         code = driver[1].split()[1][:3].upper()
         if code == "SCH":
            code = "MSC"
         embed.add_field(name=f"#{driver[0]} {code}", value=f"> {driver[1]}\n> {driver[3]}\n> {driver[4]}", inline=True)
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from skysports.com/f1/standings")
      embed.set_author(name="F1 World Drivers Championship Standings", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/working/images/f1.png")
      await ctx.send(embed=embed)

   @commands.command(aliases=["WCC"])
   async def wcc(self, ctx):
      """Returns F1 World Constructors Championship Standings"""

      wcc = await F1.getWCC()
      embed = discord.Embed(
         colour=discord.Colour.red()
      )

      for team in wcc:
         code = self.teams[team[1]]
         embed.add_field(name=f"#{team[0]} {code}", value=f"> {team[1]}\n> {team[2]}", inline=True)
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from skysports.com/f1/standings")
      embed.set_author(name="F1 World Constructors Championship Standings", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/working/images/f1.png")
      await ctx.send(embed=embed)

   @commands.command(aliases=["F1"])
   async def f1(self, ctx, type=None):
      """Returns F1 Schedule"""

      schedule = await F1.getSchedule()
      embed = discord.Embed(
         colour=discord.Colour.red()
      )
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from http://ergast.com/mrd/")

      if type is None:
         # Return next F1 race
         embed.set_author(name="F1 Schedule (Next Round)", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/working/images/f1.png")
         today = datetime.date.today()

         for round in schedule:
            if today <= datetime.datetime.strptime(round["date"], "%Y-%m-%d").date():
               title = f"Round {round['round']} {round['raceName']}"
               dateTime = f"{round['date']} {round['time'].replace('Z', 'UTC')}"
               msg = f"> {round['Circuit']['circuitName']}\n> {round['Circuit']['Location']['locality']}, {round['Circuit']['Location']['country']}\n> {dateTime}"
               embed.add_field(name=title, value=msg)
               return await ctx.send(embed=embed)
         embed.add_field(name="No New F1 Races", value="No new races for the F1 season")
      else:
         # Return full schedule
         embed.set_author(name="F1 Schedule (Full)", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/working/images/f1.png")

         for round in schedule:
            title = f"Round {round['round']} {round['raceName']}"
            dateTime = f"{round['date']} {round['time'].replace('Z', 'UTC')}"
            msg = f"> {round['Circuit']['circuitName']}\n> {round['Circuit']['Location']['locality']}, {round['Circuit']['Location']['country']}\n> {dateTime}"
            embed.add_field(name=title, value=msg)
      await ctx.send(embed=embed)

   @staticmethod
   async def getWDC():
      """Async web request F1 World Drivers Championship standings"""

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
      """Async web request F1 World Constructors Championship standings"""

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

   @staticmethod
   async def getSchedule():
      """Async web request current F1 schedule"""

      url = "http://ergast.com/api/f1/current.json"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(url) as web_resp:
            if web_resp.status == 200:
               dataJSON = await web_resp.json()
               return dataJSON["MRData"]["RaceTable"]["Races"]
            return "Warning, web error occured. Code: {web_resp.status}"
      return "Warning, request timeout"


def setup(client):
   client.add_cog(F1(client))


async def asyncTest():
   """Local async testing"""
   print("testing async local functions")

   # print(await F1.getWDC())
   # print(await F1.getWCC())
   # print(await F1.getSchedule())

if __name__ == "__main__":
   import asyncio
   asyncio.run(asyncTest())
