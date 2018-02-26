
discord.aio
===========


.. image:: https://img.shields.io/pypi/v/discord.aio.svg
   :target: https://pypi.python.org/pypi/discord.aio
   :alt: PyPI version


.. image:: https://img.shields.io/pypi/pyversions/discord.aio.svg
   :target: https://github.com/Ryozuki/discord.aio
   :alt: Python version


.. image:: https://img.shields.io/pypi/status/discord.aio.svg
   :target: https://github.com/Ryozuki/discord.aio
   :alt: Module status


.. image:: https://img.shields.io/pypi/l/discord.aio.svg
   :target: https://github.com/Ryozuki/discord.aio/blob/master/LICENSE.txt
   :alt: License


.. image:: https://img.shields.io/discord/416878158436892672.svg
   :target: https://discord.gg/hJ7ewAT
   :alt: Discord

.. image:: https://readthedocs.org/projects/discordaio/badge/?version=latest
   :target: http://discordaio.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

..

   discord.aio is an asynchronous Discord API wrapper


*Currently under very early development*

Python 3.6+ only.

Documentation
-------------

You can find the module documentation here: `documentation <http://discordaio.rtfd.io>`_

Installation
------------

With pip:
^^^^^^^^^


* ``pip3 install discord.aio``

From source:
^^^^^^^^^^^^


* ``git clone https://github.com/Ryozuki/discord.aio && cd discord.aio && pip3 install .``

Local development
-----------------


* ``git clone https://github.com/Ryozuki/discord.aio``
* ``cd discord.aio && pip3 install -e .``

Example bot
-----------

.. code-block:: python
   
    import asyncio
    import os
    import logging
    from discordaio import DiscordBot

    logging.basicConfig(
        level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    logger = logging.getLogger('my_lovely_bot')

    if __name__ == '__main__':
        TOKEN = os.environ['DISCORD_TOKEN']

        bot = DiscordBot(TOKEN)

        @bot.event()
        async def on_ready():
            logger.info('Connected!')
            logger.info(f'My username is {bot.user}')

        @bot.event('on_message') # You can also use a custom function name.
        async def foo_bar(message):
            logger.info(f'{message.author}: {message.content}')
        
        bot.run()

`Here <https://github.com/Ryozuki/discord.aio/blob/master/examples/bot.py>`_ you can find a more extensive example.


TODO
----


* `Add compression support <https://discordapp.com/developers/docs/topics/gateway#encoding-and-compression>`_
* `Add bot shards support <https://discordapp.com/developers/docs/topics/gateway#get-gateway-bot>`_
* Handle ISO8601 timestamp
* Make the DiscordBot methods better.