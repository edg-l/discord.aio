# Documentation
The project is under early development, so the documentation is heavily incomplete and maybe not accurate.

## Index
- [Events](#events)
- - [on_ready](#event-on_ready)
- - [on_guild_create](#event-on_guild_create)

## Events

### Event: on_ready
Called when:
- The client is ready and connected.

```python
@bot.event()
async def on_ready():
    print('Connected!')
    print(f'My username is {bot.user}')
```

### Event: on_guild_create
Called when:
- After the `on_ready` event, to fullfill the guild information.
- When a Guild becomes available again to the client.
- When the current user joins a new Guild.

Event Parameters:
- `guild_index`: The guild index to be used with `DiscordBot.guilds[index]`

```python
@bot.event()
async def on_guild_create(guild_index):
    print(f'I\'m connected to {bot.guilds[guild_index].name} guild, it got {len(bot.guilds[guild_index].channels)} channels.')
```

### Event: on_typing_start
Called when:
- A user starts typing in a channel

Event Parameters:
- `user_id`: The id of the user that started typing.
- `channel_id`: The id of the channel where the action happened.
- `timestamp`: The timestamp telling when it happened.

```python
@bot.event()
async def on_typing_start(user_id, channel_id, timestamp):
    print(f'User with id {user_id} started typing!')
```

### Event: on_message
Called when:
- A user starts typing in a channel

Event Parameters:
- `user_id`: The id of the user that started typing.
- `channel_id`: The id of the channel where the action happened.
- `timestamp`: The timestamp telling when it happened.

```python
@bot.event()
async def on_message(message):
    print(f'{message.author}: {message.content}')
```