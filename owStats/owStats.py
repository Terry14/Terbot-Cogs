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
    async def owsearch(self, ctx, uname: str = None):
        """
        Searches for players matching the given username.
        """
        # Your code will go here
        if uname:
            async with ctx.typing():
                
                driver = webdriver.Firefox(log_path=data_manager.cog_data_path(self))
                driver.get("https://playoverwatch.com/en-us/search/?q=" + uname)
                names = re.findall(">(" + uname + "#[0-9]+)<", driver.page_source, flags=re.IGNORECASE)
                levels = re.findall("level-value\">([0-9]+)<", driver.page_source, flags=re.IGNORECASE)
                private = re.findall("lity-private=\"(.+)\"", driver.page_source)
                output = "BattleTag\t\tLevel\tPublic\n"
                for n, l, p in zip(names, levels, private):
                    output += n + "\t\t" + l + ("\t:white_check_mark:" if p == "false" else "\t") + "\n"
                return await ctx.send(output)
        else:
            return await ctx.send("Please provide a username to search (without the BattleTag ID)")
