"""
Uno cog for bots
"""
import json
import logging
from typing import Any, Dict, Set

import discord
from discord import app_commands
from discord.ext import commands

from cogs.uno.constants import discord_messages, log_messages, paths

MAX_PLAYERS = 6

# TODO: make all strings constants
class UnoCog(commands.Cog):
    """
    Cog responsible with communication with the users on discord
    """
    
    def __init__(self, bot):
        self._log = logging.getLogger("cogs.uno.UnoCog")
        self._lobbies: Dict[int | None, LobbyView]
        self._games: Dict[int | None, Any]
        self.bot = bot
        self._log.info("Ready")

        with open(paths.EMBEDS_PATH, "r", encoding="utf-8") as file:
            self._embeds = json.load(file)

    def destroy_lobby(self, guild_id: int):
        """
        Called by the underlying LobbyView to destroy the lobby

        Args:
        ----
            guild_id (int): guild id of where to destroy the lobby
        """
        del self._lobbies[guild_id]
    
    def start_game(self):
        """
        Start game and unerlying logic
        """
        pass

    @app_commands.command()
    async def create_game(self, interaction: discord.Interaction) -> None:
        """
        Creates a lobby and sends the LobbyView for people to join

        Args:
        ----
            interaction (discord.Interaction): interaction the triggered this event
        """
        self._log.debug(log_messages.COMMAND_CALLED, log_messages.CREATE_GAME,
                        interaction.user.id, interaction.guild_id)
        if interaction.guild is None:
            self._log.debug(log_messages.CG_DM_ERROR, interaction.user.id)
            await interaction.response.send_message(discord_messages.CG_DM_ERROR, ephemeral=True)
        elif interaction.guild.id in self._lobbies:
            await interaction.response.send_message(discord_messages.CG_LOBBY_EXISTS, ephemeral=True)
        else:
            view = LobbyView(interaction.user, interaction.guild, self)
            self._lobbies[interaction.guild.id] = view
            await interaction.response.send_message(embed=discord.Embed.from_dict(self._embeds["create_lobby"]), view=view)
            self._log.debug(log_messages.CG_ADDED_PLAYER, interaction.user.id, interaction.guild_id, self._lobbies[interaction.guild_id], MAX_PLAYERS)

            
class LobbyView(discord.ui.View):
    """
    Discord view for the lobby including join, leave and start buttons
    """

    def __init__(self, user: discord.User | discord.Member, guild: discord.Guild, cog: UnoCog):
        super().__init__()
        self._log = logging.getLogger("cogs.uno.LobbyView")
        self._caller = user
        self._guild = guild
        self._players: Set[discord.User | discord.Member] = {user}
        self._cog = cog

    def __len__(self):
        return len(self._players)

    @discord.ui.button(style=discord.ButtonStyle.primary, label="Join")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Join button method that tries to join a player from the lobby

        Args:
        ----
            interaction (discord.Interaction): interaction the triggered this event
            button (discord.ui.Button): the button itself
        """
        if interaction.user in self._players:
            self._log.debug(log_messages.JB_PART_OF_LOBBY, interaction.user.id)
            await interaction.response.send_message(discord_messages.JB_PART_OF_LOBBY, ephemeral=True)
        else:
            self._players.add(interaction.user)
            self._log.debug(log_messages.JB_JOINED_LOBBY, interaction.user.id, interaction.guild_id, len(self), MAX_PLAYERS)
            await interaction.response.send_message(discord_messages.JB_JOINED_LOBBY, ephemeral=True)
            # Disabe join button after reachin MAX_PLAYERS
            if len(self._players) == MAX_PLAYERS:
                button.disabled = True
                if interaction.message is not None:
                    await interaction.message.edit(view=self)

    @discord.ui.button(style=discord.ButtonStyle.danger, label="Leave")
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Leave button method that tries to remove a player from the lobby

        Args:
        ----
            interaction (discord.Interaction): interaction the triggered this event
            button (discord.ui.Button): the button itself
        """
        if interaction.user not in self._players:
            self._log.debug(log_messages.LB_NOT_PART_OF_LOBBY, interaction.user.id)
            await interaction.response.send_message(discord_messages.LB_NOT_PART_OF_LOBBY, ephemeral=True)
        else:
            self._players.remove(interaction.user)
            self._log.debug(log_messages.LB_LEFT_LOBBY, interaction.user.id, interaction.guild_id, len(self), MAX_PLAYERS)
            await interaction.response.send_message(discord_messages.LB_LEFT_LOBBY, ephemeral=True)
            # Destroy lobby
            if len(self._players) == 0:
                if interaction.message is not None:
                    await interaction.message.delete()
                self._log.debug(log_messages.LB_NOBODY_LEFT)
                await interaction.followup.send(discord_messages.LB_NOBODY_LEFT)
                self._cog.destroy_lobby(self._guild.id)

    @discord.ui.button(style=discord.ButtonStyle.success, label="Start")
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Start button method that tries to start a game

        Args:
        ----
            interaction (discord.Interaction): interaction the triggered this event
            button (discord.ui.Button): the button itself
        """
        