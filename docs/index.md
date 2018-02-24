# Documentation
The project is under early development, so the documentation is heavily incomplete and maybe not accurate.

## Index
- [Events](#events)
- - [on_ready](#on_ready)
- - [on_guild_create](#on_guild_create)

## Events

### Event: on_ready
Called when:
- The client is ready and connected.

```python
@bot.event()
async def on_ready():
    logger.info("I got called and im connected :)")
    logger.info(f'My username is {bot.user}')
```

### Event: on_guild_create
Called when:
- After the `on_ready` event, to fullfill the guild information.
- When a Guild becomes available again to the client.
- When the current user joins a new Guild.

```python
@bot.event()
async def on_guild_create():
    logger.info("I got called and im connected :)")
    logger.info(f'My username is {bot.user}')
```