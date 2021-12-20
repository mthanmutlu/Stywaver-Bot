from discord.ext import tasks
import discord
import json
from datetime import datetime

from discord.member import Member

with open('config.json', encoding='UTF-8') as file:
    config = json.load(file)


class Mutes():
    def __init__(self, client: discord.Client) -> None:
        self.client = client

    @tasks.loop(seconds=1)
    async def checkMuteTime(self):
        with open('mutes.json', encoding='UTF-8') as file:
            mutes = json.load(file)

        if mutes != {}:
            for memberId, data in mutes.items():
                memberId = int(memberId)
                if data['status']:
                    endsAt = datetime.fromisoformat(data['endsAt'])
                    now = datetime.now()
                    if endsAt <= now:
                        data['status'] = False
                        guild = self.client.get_guild(config['guildID'])
                        mutedRole = discord.utils.find(
                            lambda r: r.id == config['mutedRole'], guild.roles)
                        member: Member = discord.utils.find(
                            lambda m: m.id == memberId, guild.members)
                        await member.remove_roles(mutedRole)
                        print('Time is up!')
                    else:
                        pass

        with open('mutes.json', 'w', encoding='UTF-8') as file:
            json.dump(mutes, file, indent=4)
