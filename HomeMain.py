#!/usr/bin/env python3

import os
import discord
from discord.ext import commands
import sys
from decouple import config

"""
Discord Home Bot in Python

By Joseph Libasora
Last updated: 01.Sept.2021
"""

client = commands.Bot(command_prefix="!")
client.remove_command("help")

@client.event
async def on_ready():
   """Reports when main bot is ready"""


@client.command()
async def ping(ctx):
   """Returns latency between bot and server"""
   await ctx.send(f"Pong main. {round(client.latency * 1000)}ms")


@client.group(invoke_without_command=True)
async def help(ctx):
   """Custom bot help command"""

   embed = discord.Embed(
      title="HomeBot Help Menu",
      description="Bot command prefix: !",
      colour=discord.Colour.blue()
   )
   # aptWX.py
   embed.add_field(name="!metar [airport_code]", value="> METAR report for a given airport", inline=True)
   embed.add_field(name="!taf [airport_code]", value="> TAF report for a given airport", inline=True)
   embed.add_field(name="!wx [airport_code]", value="> Full METAR/TAF report for a given airport", inline=True)

   # times.py
   embed.add_field(name="!time [day]", value="> Request class timetable", inline=True)
   
   # covid19.py
   embed.add_field(name="!covid", value="> Request Ireland COVID-19 Data", inline=True)

   # f1.py
   embed.add_field(name="!f1", value="> Request F1 (Full) Schedule", inline=True)
   embed.add_field(name="!f1.next", value="> Request F1 (Next) Schedule", inline=True)
   embed.add_field(name="!wdc", value="> Request F1 WDC Standings", inline=True)
   embed.add_field(name="!wcc", value="> Request F1 WCC Standings", inline=True)

   embed.set_thumbnail(url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
   embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
   embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
   await ctx.send(embed=embed)


@client.command()
async def load(ctx, path):
   """Loads cogs"""
   client.load_extension(f"cogs.{path}")
   await ctx.send(f"Cog: {path} loaded")


@client.command()
async def unload(ctx, path):
   """Unloads cogs"""
   client.unload_extension(f"cogs.{path}")
   await ctx.send(f"Cog: {path} unloaded")


@client.command()
async def reload(ctx, path):
   """Reloads cog"""
   client.unload_extension(f"cogs.{path}")
   client.load_extension(f"cogs.{path}")
   await ctx.send(f"Cog: {path} reloaded")


@client.command()
async def freload(ctx):
   """Reload all cogs"""
   for file_n in os.listdir("./cogs"):
      if file_n.endswith(".py"):
         client.unload_extension(f"cogs.{file_n[:-3]}")
         client.load_extension(f"cogs.{file_n[:-3]}")
   await ctx.send("Reloaded all cogs")

for file_n in os.listdir("./cogs"):
   if file_n.endswith(".py"):
      client.load_extension(f"cogs.{file_n[:-3]}")


if __name__ == "__main__":
   """
   Bot token management
   Bot token is handled through environment variables
   """
   client.run(config("TOKEN"))
