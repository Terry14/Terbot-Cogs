import asyncio
import os
import requests

import aiohttp
import discord
from redbot.core import Config, checks, commands
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.predicates import MessagePredicate

class RemoveBG(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # Free api key only allows for 50 uses Monthly.
    async def removebg(self, ctx, link: str = None):
        """
        Removes the background from an image.
        Upload the image as a file or use a link.

        Syntax:'[p]removebg' or '[p]removebg <link>'.
        """
        # Your code will go here
        removebg_key = await self.bot.get_shared_api_tokens("removebg")
        if removebg_key.get("api_key") is None:
            return await ctx.send("Set removebg api key with '[p]set api removebg api_key <api_key>' where a key can be obtained from: https://www.remove.bg/api")
        
        attachments = ctx.message.attachments
        """
        if len(attachments) > 1 or (attachments and link):
            await ctx.send("Please supply just one image at a time.")
            return
        """

        for attach in attachments:
            url = attach.url
            filename = "".join(url.split("/")[-1:]).replace("%20", "_")
            file_name, file_extension = os.path.splitext(filename)
            if file_extension not in [".png", ".PNG", ".jpg", ".JPG"]:
                return await ctx.send("Sorry, only png and jpg are currently supported.")

            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                data={
                    'image_url': url,
                    'size': 'auto'
                },
                headers={'X-Api-Key': removebg_key},
            )
            if response.status_code == requests.codes.ok:
                await ctx.send(response.content)
            else:
                await ctx.send("Error: " + response.status_code + response.text)

        if link:
            url = link
            filename = "".join(url.split("/")[-1:]).replace("%20", "_")
            file_name, file_extension = os.path.splitext(filename)
            if file_extension not in [".png", ".PNG", ".jpg", ".JPG"]:
                return await ctx.send("Sorry, only png and jpg are currently supported.")

            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                data={
                    'image_url': url,
                    'size': 'auto'
                },
                headers={'X-Api-Key': removebg_key},
            )
            if response.status_code == requests.codes.ok:
                await ctx.send(response.content)
            else:
                await ctx.send("Error: " + response.status_code + response.text)
                await ctx.send("Sorry, looks like my Free API has run out of uses for this month.")
