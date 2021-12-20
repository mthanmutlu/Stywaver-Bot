import asyncio
from datetime import datetime, timedelta
import json
import os
import discord
from discord.ext import commands
from discord.channel import TextChannel, VoiceChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.member import Member, VoiceState
from discord.message import Message
from utils.randomColor import randColor


class Mute(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    @commands.has_permissions(kick_members=True)
    @commands.command(name='mute')
    async def mute(self, ctx: Context, member: Member, seconds: int):
        mutesPath = os.path.dirname(__file__) + '/../mutes.json'
        configPath = os.path.dirname(__file__) + '/../config.json'
        with open(mutesPath, encoding='UTF-8') as file:
            mutes = json.load(file)

        with open(configPath, encoding='UTF-8') as file:
            config = json.load(file)

        user_id = str(member.id)

        # if user_id not in mutes:
        createdAt = datetime.now()
        delta = timedelta(seconds=seconds)  # Seconds ~ Minutes
        endsAt = createdAt + delta
        mutes[user_id] = {
            'status': True,
            'createdAt': createdAt.isoformat(),
            'endsAt': endsAt.isoformat()
        }
        mutedRole = discord.utils.find(
            lambda r: r.id == config['mutedRole'], ctx.guild.roles)
        await member.add_roles(mutedRole)
        await ctx.reply(f'**{member.mention} Kullanıcısı {seconds} saniyeliğine susturuldu**')

        with open(mutesPath, 'w', encoding='UTF-8') as file:
            json.dump(mutes, file, indent=4)

    @commands.has_permissions(kick_members=True)
    @commands.command(name='unmute')
    async def unmute(self, ctx: Context, member: Member):
        mutesPath = os.path.dirname(__file__) + '/../mutes.json'
        configPath = os.path.dirname(__file__) + '/../config.json'
        with open(mutesPath, encoding='UTF-8') as file:
            mutes = json.load(file)

        with open(configPath, encoding='UTF-8') as file:
            config = json.load(file)

        user_id = str(member.id)
        if user_id in mutes:
            if mutes[user_id]['status']:
                mutes[user_id]['status'] = False
                mutedRole = discord.utils.find(
                    lambda r: r.id == config['mutedRole'], ctx.guild.roles)
                await member.remove_roles(mutedRole)
                await ctx.reply(f'**{member.mention} Kullanıcısının susturu kalktı.**')

        with open(mutesPath, 'w', encoding='UTF-8') as file:
            json.dump(mutes, file, indent=4)


def setup(client: Bot):
    client.add_cog(Mute(client))
