#!/usr/bin/env python3

import os
import logging
from pydiscord import DiscordBot

import logging
logging.basicConfig(level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger('test_bot')

if __name__ == '__main__':
    TOKEN = os.environ['PYDISCORD_TEST_TOKEN']

    bot = DiscordBot(TOKEN)

    @bot.event('on_ready')
    async def on_connect(data):
        logger.info("I got called and im connected :)")
        res = await bot.get_guild(97740313094782976)
        logger.info(res)
        logger.info(res.owner_id)
        logger.info(res.roles)

    bot.run()
