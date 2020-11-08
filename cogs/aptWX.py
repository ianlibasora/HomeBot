#!/usr/bin/env python3

import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests

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

def setup(client):
   client.add_cog(Weather(client))

def main():
   """Local main() for testing"""
   a = Weather.SyncTAF("EGLL")
   b = Weather.SyncTAF()
   print(a)
   print(b)

if __name__ == "__main__":
   main()
