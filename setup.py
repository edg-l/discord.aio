from setuptools import setup

setup(name='discord.aio',
      version='0.1.4',
      description='discord.aio is a asynchronous Discord API wrapper for asyncio and python',
      url='https://github.com/Ryozuki/discord.aio',
      author='Ryozuki',
      author_email='contact@ryobyte.com',
      license='MIT',
      packages=['discordaio'],
      install_requires=[
          'aiohttp',
      ],
      zip_safe=False,
      keywords=['discord', 'wrapper', 'api', 'bot', 'asyncio'],
      python_requires='>=3.6',
      classifiers=[
          # How mature is this project? Common values are
          #   1 - Planning
          #   2 - Pre-Alpha
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 2 - Pre-Alpha',

          'Framework :: AsyncIO',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.6',
      ])
