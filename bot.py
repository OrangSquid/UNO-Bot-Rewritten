import logging
from typing import Dict, List
import discord
from discord.ext import commands
from cogs.uno import uno

class UnoBot(commands.Bot):
    
    async def on_ready(self):
        # Setup logging on this class
        discord.utils.setup_logging(level=logging.DEBUG)
        self._log = logging.getLogger("UnoBot")
        self._lobbies: Dict[str, List[discord.User]] = {}
        
        await self.add_cog(uno.UnoCog(self))
        
        #await self.tree.sync()
        
        self._log.info("Ready")
        

def main():
    with open("key.txt") as file:
        key = file.readline()
    bot = UnoBot(command_prefix=".", intents=discord.Intents.default())
    bot.run(key)

if __name__ == "__main__":
    main()