#!/usr/bin/env python3

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp

class Weather(commands.Cog):
   """
   Aviation METAR/TAF Library
   Adapted for Discord

   By Joseph Libasora
   Last updated: 26.Jul.2021
   """

   def __init__(self, client):
      self.client = client

   @commands.command()
   async def WXping(self, ctx):
      await ctx.send("Pong aptWX.py")

   @commands.command(aliases=["METAR"])
   async def metar(self, ctx, apt="EIDW"):
      """Returns METAR for airport passed as arguement"""

      embed = discord.Embed(
         title="Airport Weather",
         description="Airport METAR report",
         colour=discord.Colour.blue()
      )
      embed.add_field(name=f"{apt.upper()} METAR", value=await Weather.AsyncMETAR(apt), inline=False)
      embed.set_thumbnail(url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/plane.png")
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from aviationweather.gov")
      embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
      await ctx.send(embed=embed)

   @commands.command(aliases=["TAF"])
   async def taf(self, ctx, apt="EIDW"):
      """Returns TAF for airport passed as arguement"""
      

      embed = discord.Embed(
         title="Airport Weather",
         description="Airport TAF report",
         colour=discord.Colour.blue()
      )
      embed.add_field(name=f"{apt.upper()} TAF", value=await Weather.AsyncTAF(apt), inline=False)
      embed.set_thumbnail(url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/plane.png")
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from aviationweather.gov")
      embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
      await ctx.send(embed=embed)

   @commands.command(aliases=["WX", "wx"])
   async def report(self, ctx, apt="EIDW"):
      """Returns airport METAR/TAF passed as arguement"""

      embed = discord.Embed(
         title="Airport Weather",
         description="Airport full weather report",
         colour=discord.Colour.blue()
      )
      embed.add_field(name=f"{apt.upper()} METAR", value=await Weather.AsyncMETAR(apt), inline=False)
      embed.add_field(name=f"{apt.upper()} TAF", value=await Weather.AsyncTAF(apt), inline=False)
      embed.set_thumbnail(url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/plane.png")
      embed.set_footer(icon_url=ctx.author.avatar_url, text="Sourced from aviationweather.gov")
      embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
      await ctx.send(embed=embed)

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

async def amain():
   """Local async main for testing"""
   a = await Weather.AsyncTAF()
   b = await Weather.AsyncTAF("EGLL")
   print(a)
   print(b)

if __name__ == "__main__":
   import asyncio
   asyncio.run(amain())
