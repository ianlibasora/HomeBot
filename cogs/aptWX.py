#!/usr/bin/env python3

import discord
from discord.ext import commands

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

def setup(client):
   client.add_cog(Weather(client))
