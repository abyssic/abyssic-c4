from datetime import datetime as dt
import json
import sys
import os
from utils.utils import Utils

from discord import Embed
from rgbprint import gradient_print

class Config:
    try:
        with open(os.path.join(sys.path[0], 'config/config.json'),
                  'r+',
                  encoding='utf8') as file:
            data = json.load(file)

            token = data['token']
            prefix = data['prefix']
            server_name = data['server_name']
            server_icon = data['server_icon']
            channels_name = data['channels_name']
            webhook_name = data['webhook_name']
            roles_name = data['roles_name']
            spam_message = data['spam_message']
            raid_cooldown = data['raid_cooldown']
            restr_guilds = data['restr_guilds']
            premium_users = data['premium_users']
            embed_config = data['embed_config']
            embed_title  = embed_config['title']
            embed_description = embed_config['description']
            embed_image_url = embed_config['image_url']
            embed_color = 0x000
            embed_url: str = embed_config['url']

            spam_embed = Embed(title=embed_title,
                  description=embed_description,
                  color=embed_color,
                  timestamp=dt.utcnow(),
                  url=embed_image_url)
            spam_embed.set_image(url=embed_image_url)
            spam_embed.set_thumbnail(url=server_icon)
            
    except Exception as e:
        Utils.colorize(f'Error loading config.json: {e}', 'error')

        