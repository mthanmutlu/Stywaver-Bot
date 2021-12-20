import discord
from discord.ext import commands
import os
from muteTime import Mutes
from settings import load_requirements


config = load_requirements()

TOKEN = os.environ.get('TOKEN')
prefix = config['prefix']
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    mutes = Mutes(client)
    mutes.checkMuteTime.start()
    print('Bot is online....')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'**Loaded extension of {extension}**')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'**Unloaded extension of {extension}**')


if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.extensions
            client.load_extension(f'cogs.{filename[:-3]}')
            print(filename[:-3], 'Loaded')

client.run(TOKEN)
