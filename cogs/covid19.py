#!/usr/bin/env python3

import discord
from discord.ext import commands
import aiohttp

class Covid19(commands.Cog):
   """
   Ireland Covid-19 Data Request Library

   By Joseph Libasora
   Last updated: 26.Jul.2021
   """

   def __init__(self, client):
      self.client = client

   @commands.command()
   async def c19ping(self, ctx):
      await ctx.send("Pong covid19.py")


def setup(client):
   client.add_cog(Covid19(client))


async def asyncTest():
   """Local async testing"""
   print("testing async local functions")


if __name__ == "__main__":
   import asyncio
   asyncio.run(asyncTest())
