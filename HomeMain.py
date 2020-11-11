#!/usr/bin/env python3

import os
import discord
from discord.ext import commands
import sys

"""
Discord Home Bot in Python

By Joseph Libasora
Last updated: --.--.2020, Python 3.8.5
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
   embed.add_field(name="Commands Available:", value="Airport weather commands", inline=False)
   embed.add_field(name="!metar [airport_code]", value="METAR report for a given airport", inline=True)
   embed.add_field(name="!taf [airport_code]", value="TAF report for a given airport", inline=True)
   embed.add_field(name="!wx [airport_code]", value="Full METAR/TAF report for a given airport", inline=True)
   embed.set_thumbnail(url="https://raw.githubusercontent.com/ianlibasora/HomeBot/working/images/home.png")
   embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
   embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/working/images/home.png")
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

for file_n in os.listdir("./cogs"):
   if file_n.endswith(".py"):
      client.load_extension(f"cogs.{file_n[:-3]}")

def main():
   """
   Bot token management
   
   Note: 
    - Bot token is kept in the '.token.txt' file
    - This is to avoid the sharing of bot tokens
   """
   global token
   try:
      with open("./.token.txt") as fd:
         token = fd.read().strip()
   except FileNotFoundError:
      sys.exit("Warning, Error occured. No '.token.txt' file found!")

if __name__ == "__main__":
   main()
   client.run(token)
