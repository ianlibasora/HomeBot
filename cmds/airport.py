#!/usr/bin/env python3

import discord
from aiohttp import ClientTimeout, ClientSession
from bs4 import BeautifulSoup
from discord.ext import commands

from settings import HTTP_TIMEOUT


class Airport(commands.Cog):
    """
    Aviation METAR/TAF Reporting Cog
    """

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def WXping(self, ctx):
        await ctx.send("Pong airport.py")


    @commands.command(aliases=["METAR"])
    async def metar(self, ctx, apt="EIDW"):
        """Returns METAR for airport passed as arguement"""

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name=f"{apt.upper()} METAR", value=f"> {await Airport.AsyncMETAR(apt)}", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar.url, text="Sourced from aviationweather.gov")
        embed.set_author(name="Airport Weather", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/plane.png")
        await ctx.send(embed=embed)


    @commands.command(aliases=["TAF"])
    async def taf(self, ctx, apt="EIDW"):
        """Returns TAF for airport passed as arguement"""
        

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name=f"{apt.upper()} TAF", value=f"> {await Airport.AsyncTAF(apt)}", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar.url, text="Sourced from aviationweather.gov")
        embed.set_author(name="Airport Weather", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/plane.png")
        await ctx.send(embed=embed)


    @commands.command(aliases=["WX", "wx"])
    async def report(self, ctx, apt="EIDW"):
        """Returns airport METAR/TAF passed as arguement"""

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name=f"{apt.upper()} METAR", value=f"> {await Airport.AsyncMETAR(apt)}", inline=False)
        embed.add_field(name=f"{apt.upper()} TAF", value=f"> {await Airport.AsyncTAF(apt)}", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar.url, text="Sourced from aviationweather.gov")
        embed.set_author(name="Airport Weather", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/plane.png")
        await ctx.send(embed=embed)


    @staticmethod
    async def AsyncMETAR(apt="EIDW"):
        """ASYNC Web request airport METAR data"""

        url = f"https://aviationweather.gov/metar/data?ids={apt}"
        async with ClientSession(timeout=ClientTimeout(total=HTTP_TIMEOUT)) as sesh:
            async with sesh.get(url) as web_resp:
                if web_resp.status == 200:
                    soup = BeautifulSoup(await web_resp.text(), "html.parser")
                    try:
                        return soup.code.text
                    except AttributeError:
                        return "Invalid airport Code"
                else:
                    return f"Warning, web error occured. Code: {web_resp.status}"
        return f"Warning, request timeout"


    @staticmethod
    async def AsyncTAF(apt="EIDW"):
        """ASYNC Web request airport TAF data"""

        url = f"https://aviationweather.gov/taf/data?ids={apt}"
        async with ClientSession(timeout=ClientTimeout(total=HTTP_TIMEOUT)) as sesh:
            async with sesh.get(url) as web_resp:
                if web_resp.status == 200:
                    soup = BeautifulSoup(await web_resp.text(), "html.parser")
                    try:
                        return soup.code.text
                    except AttributeError:
                        return "Invalid airport Code"
                else:
                    return f"Warning, web error occured. Code: {web_resp.status}"
        return f"Warning, request timeout"


async def setup(client):
    await client.add_cog(Airport(client))
