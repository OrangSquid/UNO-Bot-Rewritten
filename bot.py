
import logging
import discord

class UnoBot(discord.Client):
    
    async def on_ready(self):
        # Setup logging on this class
        discord.utils.setup_logging()
        self._log = logging.getLogger("UnoBot")
        self._log.info("Ready")

if __name__ == "__main__":
    with open("key.txt") as file:
        key = file.readline()
    bot = UnoBot(intents=discord.Intents.default())
    bot.run(key)