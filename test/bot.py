#!/usr/bin/env python3

import os
import logging
from pydiscord import DiscordBot

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.environ['PYDISCORD_TEST_TOKEN']

bot = DiscordBot(TOKEN)

@bot.event('on_ready')
async def on_connect(data):
    print("I got called and im connected :)")
    # print(data)

# define event methods here

bot.run()
