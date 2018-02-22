import os
from pydiscord import DiscordBot

TOKEN = os.environ['PYDISCORD_TEST_TOKEN']

bot = DiscordBot(TOKEN)

# define event methods here

bot.run()
