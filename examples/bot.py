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
    async def on_guild_create(guild):
        logger.info(
            f'I\'m connected to {guild.name} guild, it got {len(guild.channels)} channels.')

    @bot.event()
    async def on_message(message):
        logger.info(f'{message.author}: {message.content}')
        if message.content.startswith('!exit'):
            await bot.exit()

    @bot.event()
    async def on_message_reaction_add(user_id, channel_id, message_id, emoji):
        user = await bot.get_user(user_id)
        logger.info(f'{user} reacted to a message with {emoji.name}')

    @bot.event()
    async def on_ban(guild_id, user):
        logger.info(f'{user} has been banned')

    bot.run()
