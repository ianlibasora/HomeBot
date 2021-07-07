#!/usr/bin/env python3

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp

class F1(commands.Cog):
   """
   F1 Data Library

   By Joseph Libasora
   Last updated: 07.Jul.2021, Python 3.8.5
   """

   def __init__(self, client):
      self.client = client

   @commands.command()
   async def F1ping(self, ctx):
      await ctx.send("Pong f1.py")

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

def setup(client):
   client.add_cog(F1(client))


async def asyncTest():
   """Local async testing"""
   print("testing async local functions")

   print(await F1.getWDC())

if __name__ == "__main__":
   import asyncio
   asyncio.run(asyncTest())
