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
   Last updated: 21.Nov.2020
   """
   def __init__(self, client):
      self.client = client

   @commands.command()
   async def Tping(self, ctx):
      await ctx.send("Pong times.py")

   @commands.command(aliases=["Timetable", "timetable", "time", "Time"])
   async def ttable(self, ctx, i_day=None):
      data = await Timetable.GetTable()
      day = await Timetable.GetDay(i_day)
      if data is not None:
         await ctx.send(data[day])
      else:
         await ctx.send("No timetable found")

   @staticmethod
   async def GetTable():
      """Read timetable file"""
      try:
         with open("cogs/.times.json", "r") as fd:
            return json.loads(fd.read())

      except FileNotFoundError:
         # Fail condition: None
         return None

   @staticmethod
   async def GetDay(i_day=None):
      """Get the current or requested day"""
      week = {
         "mon": "monday", "monday": "monday",
         "tues": "tuesday", "tue": "tuesday", "tuesday": "tuesday",
         "wed": "wednesday", "wednesday": "wednesday",
         "thurs": "thursday", "thursday": "thursday",
         "fri": "friday", "friday": "friday",
         "sat": "saturday", "saturday": "saturday",
         "sun": "sunday", "sunday": "sunday"
      }
      if i_day is not None and i_day in week:
         day = week[i_day.lower()]
      else:
         day = calendar.day_name[date.today().weekday()].lower()
      return day

def setup(client):
   client.add_cog(Timetable(client))

def main():
   """Local testing main()"""
   pass

async def amain():
   """Local testing amain()"""
   # table = Timetable()
   # code = await Timetable.GetTable()
   # print(code)
   day = await Timetable.GetDay("a")
   print(day)

if __name__ == "__main__":
   # main()
   import asyncio
   asyncio.run(amain())
