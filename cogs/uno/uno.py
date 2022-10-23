import logging
import json
import discord
import sys
import os
from discord.ext import commands
from discord import app_commands
from typing import Dict, List, Any

MAX_PLAYERS = 6

class UnoCog(commands.Cog):

    def __init__(self, bot):
        self._log = logging.getLogger("cogs.uno.UnoCog")
        self._lobbies: Dict[int | None, LobbyView] = {}
        self.bot = bot
        self._log.info("Ready")

        with open("cogs/uno/embeds/embeds.json", "r") as file:
            self._embeds = json.load(file)

    def destroy_lobby(self, guild_id: int):
        del self._lobbies[guild_id]

    @app_commands.command()
    async def create_game(self, interaction: discord.Interaction) -> None:
        self._log.debug(f"create_game: User ({interaction.user.id}) in guild ({interaction.guild_id})")
        view = self._lobbies.get(interaction.guild_id)
        if interaction.guild is None:
            self._log.debug(f"create_game: User ({interaction.user.id}) tried to make a lobby in DMs")
            await interaction.response.send_message("❌ You cannot make lobbies in DMs", ephemeral=True)
        elif view is None:
            view = LobbyView(interaction.user, interaction.guild, self)
            self._lobbies[interaction.guild.id] = view
            await interaction.response.send_message(embed=discord.Embed.from_dict(self._embeds["create_lobby"]), view=view)
            self._log.debug(f"create_game: Added new player ({interaction.user.id}) to lobby on guild ({interaction.guild_id}) ({len(self._lobbies[interaction.guild_id])}/{MAX_PLAYERS})")
        else:
            await interaction.response.send_message("❌ A lobby already exists in this server", ephemeral=True)


class LobbyView(discord.ui.View):

    def __init__(self, user: discord.User | discord.Member, guild: discord.Guild, cog: UnoCog):
        super().__init__()
        self._log = logging.getLogger("cogs.uno.LobbyView")
        self._caller = user
        self._guild = guild
        self._players: List[discord.User | discord.Member] = [user]
        self._cog = cog

    def __len__(self):
        return len(self._players)

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Join")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self._players:
            self._log.debug(f"join button: user ({interaction.user.id}) tried to join lobby while already being part of it")
            await interaction.response.send_message("❌ You're already part of this lobby", ephemeral=True)
        else:
            self._players.append(interaction.user)
            self._log.debug(f"join button: Added new player ({interaction.user.id}) to lobby on guild ({interaction.guild_id}) ({len(self._players)}/{MAX_PLAYERS})")
            await interaction.response.send_message("✅ You joined the lobby", ephemeral=True)
            # Disabe join button after reachin MAX_PLAYERS
            if len(self._players) == MAX_PLAYERS:
                button.disabled = True
                if interaction.message is not None:
                    await interaction.message.edit(view=self)

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Leave")
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self._players:
            self._log.debug(f"leave button: user ({interaction.user.id}) tried to leave lobby while not being part of it")
            await interaction.response.send_message("❌ You're not part of this lobby", ephemeral=True)
        else:
            self._players.remove(interaction.user)
            self._log.debug(f"leave button: Removed player ({interaction.user.id}) from lobby on guild ({interaction.guild_id}) ({len(self._players)}/{MAX_PLAYERS})")
            await interaction.response.send_message("✅ You left the lobby", ephemeral=True)
            # Destroy lobby
            if len(self._players) == 0:
                if interaction.message is not None:
                    await interaction.message.delete()
                self._log.debug(f"leave button: Noboyd left in lobby... calling UnoCog to close it...")
                await interaction.followup.send("Nobody left in lobby, closing it...")
                self._cog.destroy_lobby(self._guild.id)

    @discord.ui.button(style=discord.ButtonStyle.success, label="Start")
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass