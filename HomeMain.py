#!/usr/bin/env python3

from os import getenv
from pathlib import Path

import discord
from discord.ext import commands

import settings


BASE_DIR_PATH = Path(__file__).parent
COGS_DIR = "cmds"
COGS_DIR_PATH = BASE_DIR_PATH.joinpath(COGS_DIR)


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")
logger = settings.logging.getLogger("bot")


@client.event
async def on_ready():
    """Reports when main bot is ready"""

    for file in COGS_DIR_PATH.iterdir():
        if str(file).endswith(".py"):
            await client.load_extension(f"{COGS_DIR}.{file.name[:-3]}")
    logger.info(f"User: {client.user} (ID: {client.user.id}). Startup")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Error. Command not found")


@client.command()
async def ping(ctx):
    """Returns latency between bot and server"""
    await ctx.send(f"Pong. {round(client.latency * 1000)}ms")


@client.group(invoke_without_command=True)
async def help(ctx):
    """Custom bot help command"""

    embed = discord.Embed(
        title="HomeBot Help Menu",
        description="Bot command prefix: !",
        colour=discord.Colour.blue()
    )

    # # aptWX.py
    # embed.add_field(name="!metar [airport_code]", value="> METAR report for a given airport", inline=True)
    # embed.add_field(name="!taf [airport_code]", value="> TAF report for a given airport", inline=True)
    # embed.add_field(name="!wx [airport_code]", value="> Full METAR/TAF report for a given airport", inline=True)

    # # times.py
    # embed.add_field(name="!time [day]", value="> Request class timetable", inline=True)
    
    # # covid19.py
    # embed.add_field(name="!covid", value="> Request Ireland COVID-19 Data", inline=True)

    # # f1.py
    # embed.add_field(name="!f1", value="> Request F1 (Full) Schedule", inline=True)
    # embed.add_field(name="!f1.next", value="> Request F1 (Next) Schedule", inline=True)
    # embed.add_field(name="!wdc", value="> Request F1 WDC Standings", inline=True)
    # embed.add_field(name="!wcc", value="> Request F1 WCC Standings", inline=True)

    embed.set_thumbnail(url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
    embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author}")
    embed.set_author(name="HomeBot", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/home.png")
    await ctx.send(embed=embed)


@client.command()
async def load(ctx, path):
    """Loads cogs"""

    try:
        await client.load_extension(f"{COGS_DIR}.{path}")
        logger.info(f"User: {client.user} (ID: {client.user.id}). Cog ({path}) loaded")
        await ctx.send(f"Cog ({path}) loaded")
    except Exception:
        logger.warning(f"User: {client.user} (ID: {client.user.id}). Failed to load Cog ({path})")
        await ctx.send(f"Failed to load Cog ({path})")


@load.error
async def loadError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument(s). Eg. !load [path]")


@client.command()
async def unload(ctx, path):
    """Unloads cogs"""

    try:
        await client.unload_extension(f"{COGS_DIR}.{path}")
        logger.info(f"User: {client.user} (ID: {client.user.id}). Cog ({path}) unloaded")
        await ctx.send(f"Cog ({path}) unloaded")
    except Exception:
        logger.warning(f"User: {client.user} (ID: {client.user.id}). Failed to unload Cog ({path})")
        await ctx.send(f"Failed to unload Cog ({path})")


@unload.error
async def unloadError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument(s). Eg. !unload [path]")


@client.command()
async def reload(ctx, path):
    """Reloads cog"""

    try:
        await client.unload_extension(f"{COGS_DIR}.{path}")
        await client.load_extension(f"{COGS_DIR}.{path}")
        logger.info(f"User: {client.user} (ID: {client.user.id}). Cog ({path}) reloaded")
        await ctx.send(f"Cog ({path}) reloaded")
    except Exception:
        logger.warning(f"User: {client.user} (ID: {client.user.id}). Failed to reload Cog ({path})")
        await ctx.send(f"Failed to reload Cog ({path})")


@reload.error
async def reloadError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument(s). Eg. !reload [path]")


@client.command()
async def freload(ctx):
    """Reload all cogs"""

    try:
        for file in COGS_DIR_PATH.iterdir():
            if str(file).endswith(".py"):
                await client.unload_extension(f"{COGS_DIR}.{file.name[:-3]}")
                await client.load_extension(f"{COGS_DIR}.{file.name[:-3]}")
        logger.info(f"User: {client.user} (ID: {client.user.id}). Reloaded all cogs")
        await ctx.send("Reloaded all cogs")
    except Exception:
        logger.warning(f"User: {client.user} (ID: {client.user.id}). Failed to reload Cogs")
        await ctx.send(f"Failed to reload Cogs")


if __name__ == "__main__":
    client.run(getenv("TOKEN"), root_logger=True)
