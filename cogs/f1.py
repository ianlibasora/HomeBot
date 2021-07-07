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


def setup(client):
   client.add_cog(F1(client))
