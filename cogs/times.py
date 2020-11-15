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
      await ctx.send("Pong times")

def setup(client):
   client.add_cog(Timetable(client))

def main():
   pass

if __name__ == "__main__":
   main()
