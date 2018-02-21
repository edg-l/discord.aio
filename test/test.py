import unittest
import asyncio
import os
from pydiscord.client import DiscordBot

TOKEN = os.environ['PYDISCORD_TEST_TOKEN']

TEST_CHANNEL_ID = 277108288925990912
TEST_GUILD_ID = 97740313094782976

class TestMethods(unittest.TestCase):
    bot = DiscordBot(TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.start())
    do_async = loop.run_until_complete

    def test_bot(self):
        self.assertTrue(self.bot.user.bot)

    def test_bot_name(self):
        self.assertEqual(str(self.bot.user), 'RyoBot#8144')

    def test_channel_name(self):
        self.assertEqual(self.do_async(
            self.bot.get_channel(TEST_CHANNEL_ID)).name, 'welcome')

    def test_get_guild(self):
        self.assertIsNotNone(self.do_async(self.bot.get_guild(TEST_GUILD_ID)))


if __name__ == '__main__':
    unittest.main()
