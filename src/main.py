from discord import Intents

from core.kyrie import Kyrie
from config.config import Config
from utils.utils import Utils

if __name__ == '__main__':
    kyrie = Kyrie(command_prefix=Config.prefix, intents=Intents.all(), help_command=None, owner_ids={792977535264620546, 1136302112364572732})
    try:
        kyrie.run(Config.token)
    except Exception as e:
        Utils.colorize(e, 'error')