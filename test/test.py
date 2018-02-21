import unittest
import asyncio
import os
from pydiscord.client import DiscordBot

TOKEN = os.environ['PYDISCORD_TEST_TOKEN']


class TestMethods(unittest.TestCase):

    def test_bot(self):
        bot = DiscordBot(TOKEN)
        # loop = asyncio.get_event_loop()
        # guilds = loop.run_until_complete(bot.get_guilds())
        # guild = loop.run_until_complete(bot.get_guild('97740313094782976'))
        # print(guild.roles[0].name)
        
        # loop.run_until_complete(bot.get_guild_members(guild))
        # print(guild.members)
        # print(len(guild.members))
        # print(guild.members[0].user)
        print(bot.user.get_default_avatar_url())

        self.assertTrue(bot.user.bot)
        self.assertEqual(str(bot.user), 'RyoBot#8144')


if __name__ == '__main__':
    unittest.main()
