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
        logger.info('Connected!')
        logger.info(f'My username is {bot.user}')
    
    @bot.event()
    async def on_guild_create(guild_index):
        logger.info(f'I\'m connected to {bot.guilds[guild_index].name} guild, it got {len(bot.guilds[guild_index].channels)} channels.')
    
    @bot.event()
    async def on_message(message):
        logger.info(f'{message.author}: {message.content}')

    @bot.event()
    async def on_typing_start(user_id, channel_id, timestamp):
        logger.info(f'User with id {user_id} started typing!')
    bot.run()
