import asyncio
import os
import io
import requests
import re
from selenium import webdriver

import aiohttp
import discord
from redbot.core import Config, checks, commands, data_manager
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.predicates import MessagePredicate

class OWStats(commands.Cog):
    """Overwatch Stats Searcher Cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=10, type=discord.ext.commands.cooldowns.BucketType.guild)
    async def owsearch(self, ctx, uname: str = None):
        """
        Searches for players matching the given username.
        """
        # Your code will go here
        if uname:
            async with ctx.typing():
                opts = webdriver.FirefoxOptions()
                opts.add_argument("--headless")
                driver = webdriver.Firefox(firefox_options=opts, service_log_path=data_manager.cog_data_path(self) / "geckodriver.log")
                driver.get("https://playoverwatch.com/en-us/search/?q=" + uname)
                names = re.findall(">(" + uname + "#[0-9]+)<", driver.page_source, flags=re.IGNORECASE)
                levels = re.findall("level-value\">([0-9]+)<", driver.page_source, flags=re.IGNORECASE)
                private = re.findall("lity-private=\"([falsetru]+)\"", driver.page_source)
                # Pad names, levels to be same length
                names = [x + (' ' * (20 - len(x))) for x in names]
                levels = [x + (' ' * (5 - len(x))) for x in levels]
                output = "```BattleTag               Level    Public?\n"
                for n, l, p in zip(names, levels, private):
                    output += n + "\t" + l + ("\tpublic" if p == "false" else "\tprivate") + "\n"
                output += "```"
                return await ctx.send(output)
        else:
            return await ctx.send("Please provide a username to search (without the BattleTag ID)")

    # TODO: Program to try multiple regions/platforms and show more stats
    @commands.command()
    async def owrank(self, ctx, btag: str = None):
        """
        Returns the player's competitive ranking.
        """
        if btag:
            btag = btag.replace("#", "-")
            response = requests.get("https://ow-api.com/v1/stats/pc/us/" + btag + "/profile")
            if response.status_code == requests.codes.ok:
                if response.json()["ratings"] is None:
                    btag = btag.replace("-", "#")
                    return await ctx.send(btag + " has not placed any competitive roles this season.")
                else:
                    for rank in response.json()["ratings"]:
                        return await ctx.send(str(rank["role"]) + ": " + str(rank["level"]) + "SR")
            else:
                return await ctx.send("User not found. Perhaps they are not on US region PC.")
        else:
            return await ctx.send("Please provide a BattleTag to search E.g. Banana-12345")
        return