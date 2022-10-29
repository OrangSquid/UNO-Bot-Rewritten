"""
Module holding all the log messaes
"""

# command_name, user_id, guild_id
COMMAND_CALLED = "%s: User (%d) in guild (%d)"

# create_game messages
# user_id
CG_DM_ERROR = "create_game: User (%d) tried to make a lobby in DMs"
# user_id, guild_id, current_number of players, max_players
CG_ADDED_PLAYER = "create_game: Added new player (%d) to lobby on guild (%d) (%d/%d)"
