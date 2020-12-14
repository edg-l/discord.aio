from setuptools import setup

long_description = open('README.rst').read()


def find_version(filename):
    """
    Find package version in file.
    """
    import re
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    content = open(os.path.join(here, filename)).read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(name='discord.aio',
      version=find_version('discordaio/version.py'),
      description='discord.aio is an asynchronous Discord API wrapper for asyncio and python',
      long_description=long_description,
      url='https://github.com/edg-l/discord.aio',
      author='Edgar',
      author_email='git@edgarluque.com',
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

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.6',
      ])
