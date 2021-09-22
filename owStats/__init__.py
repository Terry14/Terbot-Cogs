from redbot.core.bot import Red

from .owStats import OWStats


async def setup(bot: Red) -> None:
    cog = OWStats(bot)
    bot.add_cog(cog)


__red_end_user_data_statement__ = "This cog does not store any image data."
