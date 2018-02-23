#!/usr/bin/env python3

import os
import logging
from discordaio import DiscordBot

logging.basicConfig(
    level='DEBUG', format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
logger = logging.getLogger('test_bot')

if __name__ == '__main__':
    TOKEN = os.environ['PYDISCORD_TEST_TOKEN']

    bot = DiscordBot(TOKEN)

    @bot.event('on_ready')
    async def on_connect():
        logger.info("I got called and im connected :)")
        logger.info(f'My username is {bot.user}')
        res = await bot.get_guild(97740313094782976)
        logger.info(res)
        #logger.info(res.roles)
        await bot.get_guild_members(res)
        print(res.members)
        print(res.members[0].user.id)

    bot.run()
