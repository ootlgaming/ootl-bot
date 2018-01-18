# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform
import random
import copy

client = Bot(description="OOTL Bot by TacticalFruit", command_prefix="%", pm_help = True)
raids = [
    "Vault of Glass",
    "Crota's End",
    "King's Fall",
    "Wrath of the Machine",
    "Leviathan",
    "Leviathan: Eater of Worlds"
]

"""
    Client events block
"""

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))

"""
    Client commands block
"""

@client.command()
async def ping(*args):
    await client.say("Pong!")

@client.command()
async def name(*args):
    await client.say("My name is {}!".format(client.user.name))

# Picks a random raid from the list above.
# args[0] - Number of raids wanted (Optional, Default=1)
@client.command()
async def rr(*args):
    if len(args) == 0:
        number_raids = 1
    else:
        number_raids = int(args[0])

    raids_copy = copy.deepcopy(raids)
    random.shuffle(raids_copy)
    await client.say("Random Raid(s): {}".format(", ".join(raids_copy[0:number_raids])))

# Run the bot with bot token
client.run('NDAzNTY0MzI0OTAxMjI0NDU4.DUJJug.VfYFg9rgSuaf5i9jdPrG0M41UYI')

