Changelog
=========

Version 0.3.0 (Dev)
-------------------
* Fixed async error when closing bot using ctrl-c

* Added Channel#send_message
* Added Channel#mention
* Added Channel#typing
* Added Channel#delete
* Added Channel#update
* Added Channel#refresh
* Added Channel#get_message
* Added ChannelMessage#delete_own_reaction
* Added ChannelMessage#delete_user_reaction
* Added ChannelMessage#delete_all_reactions
* Added ChannelMessage#get_reactions
* Added ChannelMessage#update
* Added ChannelMessage#delete
* Added ChannelMessage#bulk_delete_messages
* Added ChannelMessage#get_invites
* Added ChannelMessage#create_invite
* Added ChannelMessage#delete_permission
* Added ChannelMessage#get_pinned_messages
* Added ChannelMessage#pin_message
* Added ChannelMessage#delete_pinned_message

* Moved DiscordBot#get_messages to Channel#get_messages
* Moved DiscordBot#leave_guild to Guild#leave
* Moved DiscordBot#get_guild_member to Guild#get_member
* Moved DiscordBot#get_guild_members to Guild#get_members
* Moved DiscordBot#create_guild_channel to Guild#create_channel
* Moved DiscordBot#delete_guild to Guild#delete
* Moved DiscordBot#get_guild_channels to Guild#get_channels
* Moved DiscordBot#modify_channel to Channel#update


Version 0.2.2
-------------

* Added DiscordBot.get_guild_channels method
* Added DiscordBot.create_guild_channel method
* Added DiscordBot.delete_guild method
* Added DiscordBot.move_channels method
* Added NotFoundError exception
* Added GatewayUnavailable exception
* Added BadRequestError exception
* Added AuthorizationError exception
* Fixed a bug in websocket

Version 0.2.0
-------------

* All discord events can be used now.

Version 0.1.0
-------------


* Initial development version
