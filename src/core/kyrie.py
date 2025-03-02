from os import listdir
from utils.utils import Utils

from discord.ext import commands


class Kyrie(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        for file in listdir('src/cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    Utils.colorize(f'Loaded cog {file}', 'ok')

                except Exception as e:
                    Utils.colorize(e, 'error')
