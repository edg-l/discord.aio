import unittest
import asyncio
import os
from pydiscord import DiscordBot

TOKEN = os.environ['PYDISCORD_TEST_TOKEN']


class TestMethods(unittest.TestCase):

    def test_bot(self):
        bot = DiscordBot(TOKEN)
        print(bot.user)
        print(repr(bot.user))
        self.assertTrue(bot.user.bot)
        self.assertEqual(str(bot.user), 'RyoBot#8144')


if __name__ == '__main__':
    unittest.main()
