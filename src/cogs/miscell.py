from datetime import datetime as dt
import io
from config.config import Config
from core.db import DbMan

from discord import Embed, User, File
from discord.ext import commands
from httpx import AsyncClient
from PIL import Image, ImageDraw


class Miscell(commands.Cog):
    def __init__(self, kyrie):
        self.__kyrie = kyrie

    @commands.command(
      name='help',
      aliases=['h'],
      description=f'{Config.prefix}help',
    )
    async def help(self, ctx):
        for id in self.__kyrie.owner_ids:
            if id == 792977535264620546:
                dev = await self.__kyrie.fetch_user(id)

        embed = Embed(
            title=f'{self.__kyrie.user.name} | Commands',
            description=
            f'Below is a list of my available **commands**.\n> My prefix is: **{self.__kyrie.command_prefix}**',
            color=0x000,
            timestamp=dt.utcnow(),
        )

        embed.set_author(name=dev, icon_url=dev.avatar)
        embed.set_thumbnail(url=self.__kyrie.user.avatar)
        embed.set_footer(text=self.__kyrie.user.name, icon_url=self.__kyrie.user.avatar)

        for cmd in self.__kyrie.commands:
            embed.add_field(name=cmd.name,
                            value=f'`{cmd.description}`',
                            inline=False)

        await ctx.send(embed=embed)

    @commands.command(
        name='avatar',
        aliases=['av', 'tool'],
        description=f'{Config.prefix}avatar optional:<user>',
    )
    async def avatar(self, ctx, user: User = None):
        if user is None:
            avatar_url: str = ctx.author.avatar.url
        else:
            avatar_url: str = user.avatar.url

        async with AsyncClient() as client:
            response = await client.get(avatar_url)
            imagen_avatar = response.content

        img_avatar = Image.open(io.BytesIO(imagen_avatar))
        img_avatar = img_avatar.resize((520, 520))

        img_final = Image.new('RGBA', (520, 520), (0, 0, 0, 0))
        URL_PNG = 'https://i.ibb.co/4ZBjF6Gz/abyssic-new-logo.png'
        async with AsyncClient() as client:
            response = await client.get(URL_PNG)
            imagen_png: bytes = response.content

        img_png = Image.open(io.BytesIO(imagen_png))
        img_png = img_png.resize((500, 500))
        img_final.paste(img_avatar.convert('RGBA'), mask=img_avatar.convert('RGBA'))
        x = (img_final.size[0] - img_png.size[0]) // 2
        y = (img_final.size[1] - img_png.size[1]) // 2
        img_final.paste(img_png, (x, y), img_png)

        buffer_img = io.BytesIO()
        img_final.save(buffer_img, format='PNG')
        buffer_img.seek(0)
        await ctx.send(file=File(buffer_img, 'abyssic.png'))

    @commands.command(
        name='premium',
        aliases=['pm', 'addpremium'],
        description=f'{Config.prefix}premium <user>',
    )
    async def premium(self, ctx, user: User=None):
        if not ctx.author.id in self.__kyrie.owner_ids:
            await ctx.send('Este comando solo puede ser usado por devs.')
            return
            
        if user is None:
            await ctx.send('Debes mencionar a alguien.')
            return
        
        with DbMan('abyssic_premium.db', max_connections=5) as db_manager:
            if db_manager:
                db_manager.execute_query('''
                    CREATE TABLE IF NOT EXISTS abyssic_premium (
                        user_id INTEGER PRIMARY KEY
                    )
                ''')
            result = db_manager.read('abyssic_premium', f'user_id = {user.id}')
            if result:
                await ctx.send(f'{user.mention} ya es un usuario premium.')
            else:
                db_manager.create('abyssic_premium', {'user_id': user.id})
                await ctx.send(f'{user.mention} has sido agregado a la lista premium.')
        

setup = lambda kyrie: kyrie.add_cog(Miscell(kyrie))