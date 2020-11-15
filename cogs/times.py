#!/usr/bin/env python3

from datetime import date
import calendar
import json
import discord
from discord.ext import commands

class Timetable(commands.Cog):
   """
   Timetable Script in Python
   
   Adapted for discord
   
   By Joseph Libasora
   Last updated: 15.Nov.2020
   """
   def __init__(self, client):
      self.client = client

   @commands.command()
   async def Tping(self, ctx):
      await ctx.send("Pong times.py")

   @staticmethod
   async def GetTable():
      """Read timetable file"""
      try:
         with open("cogs/.times.json", "r") as fd:
            return json.loads(fd.read())

      except FileNotFoundError:
         # Fail condition: False
         return False

def setup(client):
   client.add_cog(Timetable(client))

def main():
   """Local testing main()"""
   pass

async def amain():
   """Local testing amain()"""
   # table = Timetable()
   code = await Timetable.GetTable()
   print(code)

if __name__ == "__main__":
   # main()
   import asyncio
   asyncio.run(amain())
