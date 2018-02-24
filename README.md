# discord.aio
[![PyPI version](https://img.shields.io/pypi/v/discord.aio.svg)](https://pypi.python.org/pypi/discord.aio)
[![Python version](https://img.shields.io/pypi/pyversions/discord.aio.svg)](https://github.com/Ryozuki/discord.aio)
[![Module status](https://img.shields.io/pypi/status/discord.aio.svg)](https://github.com/Ryozuki/discord.aio)
[![License](https://img.shields.io/pypi/l/discord.aio.svg)](https://github.com/Ryozuki/discord.aio/blob/master/LICENSE.txt)

> discord.aio is an asynchronous Discord API wrapper

*Currently under very early development*

Python 3.6+ only.

Read this readme with a cool theme here: [ryozuki.github.io/discord.aio/](https://ryozuki.github.io/discord.aio/)

## Documentation
You can find the module documentation here: [documentation](https://ryozuki.github.io/discord.aio/docs)

## Installation

### With pip:
- `pip3 install discord.aio`

### From source:
- `git clone https://github.com/Ryozuki/discord.aio && cd discord.aio && pip3 install .`

## Local development
- `git clone https://github.com/Ryozuki/discord.aio`
- `cd discord.aio && pip3 install -e .`

## Example bot
```python
import os
import logging
from discordaio import DiscordBot

logging.basicConfig(
    level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger('my_lovely_bot')

if __name__ == '__main__':
    TOKEN = os.environ['PYDISCORD_TEST_TOKEN']

    bot = DiscordBot(TOKEN)

    @bot.event()
    async def on_ready():
        logger.info('Connected!')
        logger.info(f'My username is {bot.user}')
    
    @bot.event('on_message') # You can also use a custom function name.
    async def foo_bar(message):
        logger.info(f'{message.author}: {message.content}')
```

[Here](https://github.com/Ryozuki/discord.aio/blob/master/test/bot.py) you can find a more extensive example.

You can also check the [documentation](https://ryozuki.github.io/discord.aio/docs) for detailed explanation on how the module works.

## TODO
- [Add compression support](https://discordapp.com/developers/docs/topics/gateway#encoding-and-compression)
- [Add bot shards support](https://discordapp.com/developers/docs/topics/gateway#get-gateway-bot)
- [Handle all discord events](https://discordapp.com/developers/docs/topics/gateway#commands-and-events-gateway-events)
- Handle ISO8601 timestamp