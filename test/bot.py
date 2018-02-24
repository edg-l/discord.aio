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

    @bot.event()
    async def on_ready():
        logger.info("I got called and im connected :)")
        logger.info(f'My username is {bot.user}')
    
    @bot.event()
    async def on_guild_create(i):
        logger.info(f'I\'m connected to {bot.guilds[i].name} guild, it got {len(bot.guilds[i].channels)} channels.')

    bot.run()
