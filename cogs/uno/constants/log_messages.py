"""
Module holding all the log messaes
"""

# command_name, user_id, guild_id
COMMAND_CALLED = "%s: User (%d) in guild (%d)"

# create_game messages
CREATE_GAME = "create_game"
# user_id
CG_DM_ERROR = "create_game: User (%d) tried to make a lobby in DMs"
# user_id, guild_id, current_number of players, max_players
CG_ADDED_PLAYER = "create_game: Added new player (%d) to lobby on guild (%d) (%d/%d)"


# LOBBY VIEW
# join button
# user_id
JB_PART_OF_LOBBY = "join button: user (%d) tried to join lobby while already being part of it"
# user_id, guild_id, current number of players on lobby, max_players
JB_JOINED_LOBBY = "join button: Added new player (%d) to lobby on guild (%d) (%d/%d)"

# leave button
# user_id
LB_NOT_PART_OF_LOBBY = "leave button: user (%d) tried to leave lobby while not being part of it"
# user_id, guild_id, current number of players on lobby, max_players
LB_LEFT_LOBBY = "leave button: Removed player (%d) from lobby on guild (%d) (%d/%d)"
LB_NOBODY_LEFT = "leave button: Noboyd left in lobby... calling UnoCog to close it..."
