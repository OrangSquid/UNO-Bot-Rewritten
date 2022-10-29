"""
    Setup and start the bot
"""
import logging

import discord
from discord.ext import commands

from cogs.uno import uno


class UnoBot(commands.Bot):
    """
    commands.Bot subclass that handles adding the cog
    """

    # Setup logging on this class
    discord.utils.setup_logging(level=logging.DEBUG)
    log = logging.getLogger("UnoBot")

    async def on_ready(self) -> None:
        """
        Sends log message and adds all the cogs
        """
        await self.add_cog(uno.UnoCog(self))
        # Uncomment to sync all commands
        #await self.tree.sync()
        self.log.info("Ready")


def main() -> None:
    """
    Reads the token from key.txt and starts bot
    """
    with open("key.txt", "r", encoding="utf-8") as file:
        key = file.readline()
    bot = UnoBot(command_prefix=".", intents=discord.Intents.default())
    bot.run(key)


if __name__ == "__main__":
    main()
