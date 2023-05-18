#!/usr/bin/env python3

import datetime

import aiohttp
import discord
from discord.ext import commands


class F1(commands.Cog):
    """
    F1 Cog Library
    """
    TEAMS = {
        "Mercedes": "MER",
        "Red Bull": "RBR",
        "McLaren": "MCL",
        "Ferrari": "FER",
        "AlphaTauri": "ATH",
        "Aston Martin": "AMR",
        "Alpine F1 Team": "ALP",
        "Alfa Romeo": "AFR",
        "Williams": "WIL",
        "Haas F1 Team": "HAS"
    }

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def F1ping(self, ctx):
        await ctx.send("Pong f1.py")


    @commands.command(aliases=["WDC"])
    async def wdc(self, ctx):
        """Returns F1 World Drivers Championship Standings"""

        wdc = await F1.getNewWDC()
        embed = discord.Embed(
            colour=discord.Colour.red()
        )

        for driver in wdc:
            embed.add_field(
                name=f"#{driver['position']} {driver['Driver']['code']}",
                value=f"> {driver['Driver']['givenName']} {driver['Driver']['familyName']}\n> {driver['Constructors'][0]['name']}\n> {driver['points']}",
                inline=True
            )
        embed.set_footer(icon_url=ctx.author.avatar.url, text="Sourced from http://ergast.com/mrd/")
        embed.set_author(name="F1 World Drivers Championship Standings", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/f1.png")
        await ctx.send(embed=embed)


    @commands.command(aliases=["WCC"])
    async def wcc(self, ctx):
        """Returns F1 World Constructors Championship Standings"""

        wcc = await F1.getNewWCC()
        embed = discord.Embed(
            colour=discord.Colour.red()
        )

        for team in wcc:
            code = self.TEAMS[team['Constructor']['name']]
            embed.add_field(
                name=f"#{team['position']} {code}",
                value=f"> {team['Constructor']['name']}\n> {team['points']}",
                inline=True
            )
        embed.set_footer(icon_url=ctx.author.avatar.url, text="Sourced from http://ergast.com/mrd/")
        embed.set_author(name="F1 World Constructors Championship Standings", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/f1.png")
        await ctx.send(embed=embed)


    @commands.command(aliases=["F1"])
    async def f1(self, ctx):
        """Returns F1 Schedule (Full)"""

        schedule = await F1.getSchedule()
        embed = discord.Embed(
            colour=discord.Colour.red()
        )
        embed.set_footer(icon_url=ctx.author.avatar.url, text="Sourced from http://ergast.com/mrd/")
        embed.set_author(name="F1 Schedule", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/f1.png")

        for round in schedule:
            title = f"Round {round['round']} {round['raceName']}"
            GPTime = f"{round['date']} {round['time'].replace('Z', ' UTC')}"
            tmpPayload = [
                f"**{round['Circuit']['circuitName']}**",
                f"{round['Circuit']['Location']['locality']}, {round['Circuit']['Location']['country']}",
                "**Grand Prix**",
                GPTime
            ]
            payload = "\n> ".join(tmpPayload)
            msg = f"> {payload}"
            embed.add_field(name=title, value=msg)
        await ctx.send(embed=embed)


    @commands.command(aliases=["f1.next", "F1.next"])
    async def f1Next(self, ctx):
        """Returns F1 Schedule (Next Round)"""

        schedule = await F1.getSchedule()
        embed = discord.Embed(
            colour=discord.Colour.red()
        )
        embed.set_footer(icon_url=ctx.author.avatar.url, text="Sourced from http://ergast.com/mrd/")
        embed.set_author(name="F1 Schedule (Next Round)", icon_url="https://raw.githubusercontent.com/ianlibasora/HomeBot/master/images/f1.png")

        for round in schedule:
            if datetime.date.today() <= datetime.datetime.strptime(round["date"], "%Y-%m-%d").date():
                title = f"Round {round['round']} {round['raceName']}"
                payloadLst = [
                    f"**{round['Circuit']['circuitName']}**",
                    f"{round['Circuit']['Location']['locality']}, {round['Circuit']['Location']['country']}",
                    "**Free Practice 1 (FP1)**",
                    f"{round['FirstPractice']['date']} {round['FirstPractice']['time'].replace('Z', ' UTC')}",
                ]
                if "Sprint" in round:
                    # If Sprint Weekend
                    payloadLst.append("**Qualifying**")
                    payloadLst.append(f"{round['Qualifying']['date']} {round['Qualifying']['time'].replace('Z', ' UTC')}")
                    payloadLst.append("**Free Practice 2 (FP2)**")
                    payloadLst.append(f"{round['SecondPractice']['date']} {round['SecondPractice']['time'].replace('Z', ' UTC')}")
                    payloadLst.append("**Sprint**")
                    payloadLst.append(f"{round['Sprint']['date']} {round['Sprint']['time'].replace('Z', ' UTC')}")
                else:
                    # If Normal Weekend
                    payloadLst.append("**Free Practice 2 (FP2)**")
                    payloadLst.append(f"{round['SecondPractice']['date']} {round['SecondPractice']['time'].replace('Z', ' UTC')}")
                    payloadLst.append("**Free Practice 3 (FP3)**")
                    payloadLst.append(f"{round['ThirdPractice']['date']} {round['ThirdPractice']['time'].replace('Z', ' UTC')}")
                    payloadLst.append("**Qualifying**")
                    payloadLst.append(f"{round['Qualifying']['date']} {round['Qualifying']['time'].replace('Z', ' UTC')}")

                payloadLst.append("**Grand Prix**")
                payloadLst.append(f"{round['date']} {round['time'].replace('Z', ' UTC')}")
                payload = "\n> ".join(payloadLst)
                msg = f"> {payload}"
                embed.add_field(name=title, value=msg)
                return await ctx.send(embed=embed)

        embed.add_field(name="No New F1 Races", value="No new races for the F1 season")
        await ctx.send(embed=embed)


    @staticmethod
    async def getSchedule():
        """Async web request current F1 schedule"""

        url = "http://ergast.com/api/f1/current.json"
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as sesh:
            async with sesh.get(url) as web_resp:
                if web_resp.status == 200:
                    dataJSON = await web_resp.json()
                    return dataJSON["MRData"]["RaceTable"]["Races"]
                return f"Warning, web error occured. Code: {web_resp.status}"
        return "Warning, request timeout"


    @staticmethod
    async def getNewWDC():
        """Async web request F1 World Drivers Championship standings"""

        url = "http://ergast.com/api/f1/current/driverStandings.json"
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as sesh:
            async with sesh.get(url) as web_resp:
                if web_resp.status == 200:
                    dataJSON = await web_resp.json()
                    return dataJSON["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
                else:
                    return f"Warning, web error occured. Code: {web_resp.status}"
        return "Warning, request timeout"


    @staticmethod
    async def getNewWCC():
        """Async web request F1 World Constructors Championship standings"""

        url = "http://ergast.com/api/f1/current/constructorStandings.json"
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as sesh:
            async with sesh.get(url) as web_resp:
                if web_resp.status == 200:
                    dataJSON = await web_resp.json()
                    return dataJSON["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]
                else:
                    return f"Warning, web error occured. Code: {web_resp.status}"
        return "Warning, request timeout"


async def setup(client):
    await client.add_cog(F1(client))
