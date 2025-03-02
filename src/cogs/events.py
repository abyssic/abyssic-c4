from asyncio import sleep
import os
from config.config import Config
from utils.utils import Utils

import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, kyrie):
        self.__kyrie = kyrie

    async def banner(self) -> None:
        BANNER: str = r"""
                        .. .  .         
                       . .  . ...       
             ..... ..........   .       
          ......   .. ....  ...         
        .......................         
       .. .. ...   ..............       
      ... .        .... ..    .         
      ... . .      .......              
      . . ....      ... ..              
       ...   ..     ..... ......        
        ....  . .  .   ...     ..       
     .    .. .. ........       .   ..   
 ..  .       ..  .. .  ... .    ..      
   .....    .    .. ..  . ....          
       . ...  ..       ..  .....        
            .. ...       ... ...        
              .....       ..  ..        
            .......       ......        
      ...... .......     ...  .         
      .. ..................   .         
         ..... ......... ....           
           ......... .... .             
                ........                

        
        """
        devs = [
            await self.__kyrie.fetch_user(id) for id in self.__kyrie.owner_ids
        ]
        os.system('cls || clear')
        Utils.colorize(BANNER, 'menu')
        Utils.colorize('--------developed by @owasp--------\n[group: .gg/e8nU2dH8rb] [exit: Ctrl+C]\n---------------------------------', 'menu')
        Utils.colorize(f'Logged in as {self.__kyrie.user}')
        Utils.colorize(f'prefix: {self.__kyrie.command_prefix}')
        Utils.colorize(
            f'Commands: {", ".join([cmd.name for cmd in self.__kyrie.commands])}',
        )
        Utils.colorize(
            f'Coded by {", ".join(dev.name for dev in devs)}\n')

    @commands.Cog.listener()
    async def on_ready(self):
        status = discord.Status.invisible
        try:
            await self.__kyrie.change_presence(status=status)
            await self.banner()

        except Exception as e:
            Utils.colorize(f'An error occurred while changing the status {e}', 'error')

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.guild.id in Config.restr_guilds:
            return

        if channel.position == 0:
            return

        for _ in range(100):
            try:
                await channel.send(Config.spam_message, embed=Config.spam_embed)
                Utils.colorize(f'Spammed channel {channel}')
                await sleep(0.5)

            except Exception as e:
                Utils.colorize(f'An error occurred while spamming the message {e}', 'error')

setup = lambda kyrie: kyrie.add_cog(Events(kyrie))