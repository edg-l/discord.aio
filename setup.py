from setuptools import setup

setup(name='pydiscord',
      version='0.1.0',
      description='Discord API wrapper',
      url='https://github.com/Ryozuki/pydiscord',
      author='Edgar Luque',
      author_email='contact@ryobyte.com',
      license='MIT',
      packages=['pydiscord'],
      install_requires=[
          'aiohttp',
      ],
      zip_safe=False)
