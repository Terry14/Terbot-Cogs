from redbot.core.bot import Red

from .RemoveBG import RemoveBG


async def setup(bot: Red) -> None:
    cog = RemoveBG(bot)
    bot.add_cog(cog)


__red_end_user_data_statement__ = "This cog does not store any image data."
