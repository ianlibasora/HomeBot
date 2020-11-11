#!/usr/bin/env python3

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import aiohttp

class Weather(commands.Cog):
   """
   Aviation METAR/TAF Library

   Sync / Async
   Adapted for Discord
   """

   def __init__(self, client):
      self.client = client

   @commands.command()
   async def WXping(self, ctx):
      await ctx.send("Pong aptWX")

   @commands.command(aliases=["METAR"])
   async def metar(self, ctx, apt="EIDW"):
      """Returns METAR for airport passed as arguement"""
      embed = discord.Embed(
         title=f"{apt.upper()} METAR",
         colour=discord.Colour.blue(),
         description=await Weather.AsyncMETAR(apt)
      )
      await ctx.send(embed=embed)

   @staticmethod
   def SyncMETAR(apt="EIDW"):
      """SYNC Web request airport METAR data"""

      url = f"https://aviationweather.gov/metar/data?ids={apt}"
      web = requests.get(url, timeout=10)
      if web.ok:
         soup = BeautifulSoup(web.text, "html.parser")
         try:
            return soup.code.text
         except AttributeError:
            return "Invalid Airport Code"
      else:
         return f"Warning, web error occured. Code: {web.status_code}"

   @staticmethod
   def SyncTAF(apt="EIDW"):
      """SYNC Web request airport TAF data"""

      url = f"https://aviationweather.gov/taf/data?ids={apt}"
      web = requests.get(url, timeout=10)
      if web.ok:
         soup = BeautifulSoup(web.text, "html.parser")
         try:
            return soup.code.text
         except AttributeError:
            return "Invalid Airport Code"
      else:
         return f"Warning, web error occured. Code: {web.status_code}"

   @staticmethod
   async def AsyncMETAR(apt="EIDW"):
      """ASYNC Web request airport METAR data"""

      url = f"https://aviationweather.gov/metar/data?ids={apt}"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(url) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               try:
                  return soup.code.text
               except AttributeError:
                  return "Invalid airport Code"
            else:
               return "Warning, web error occured. Code: {web_resp.status}"
      return "Warning, request timeout"

   @staticmethod
   async def AsyncTAF(apt="EIDW"):
      """ASYNC Web request airport TAF data"""

      url = f"https://aviationweather.gov/taf/data?ids={apt}"
      timeout = aiohttp.ClientTimeout(total=10)
      async with aiohttp.ClientSession(timeout=timeout) as sesh:
         async with sesh.get(url) as web_resp:
            if web_resp.status == 200:
               web = await web_resp.text()
               soup = BeautifulSoup(web, "html.parser")
               try:
                  return soup.code.text
               except AttributeError:
                  return "Invalid airport Code"
            else:
               return "Warning, web error occured. Code: {web_resp.status}"
      return "Warning, request timeout"

def setup(client):
   client.add_cog(Weather(client))

def main():
   """Local main() for testing"""
   a = Weather.SyncTAF("EGLL")
   b = Weather.SyncTAF()
   print(a)
   print(b)

async def amain():
   """Local async main for testing"""
   a = await Weather.AsyncTAF()
   b = await Weather.AsyncTAF("EGLL")
   print(a)
   print(b)

if __name__ == "__main__":
   # main()
   import asyncio
   asyncio.run(amain())
