# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio # for async things inside discord.py
from discord.ext.commands import Bot
from discord.ext import commands # imports a bunch of command things
import platform
import random
import copy

client = Bot(description="OOTL Bot by TacticalFruit", command_prefix="%", pm_help = False)

# Remove the normal help command. Our own will be added later
client.remove_command('help')

raids = [
    "Vault of Glass",
    "Crota's End",
    "King's Fall",
    "Wrath of the Machine",
    "Leviathan",
    "Leviathan: Eater of Worlds"
]

############################
####### Events Block #######
############################

@client.event
async def on_ready():

    print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))

############################
###### Commands Block ######
############################

@client.command()
async def help(*args):
    if args[0] == "ping":
        help_message = \
"""
```
ping -- Pings the bot

Params: None
Notes:
    * If the bot is up, it will
      reply with 'pong'
```
"""
    elif args[0] == "name":
        help_message = \
"""
```
name -- Returns the name of the bot

Params: None
```
"""
    elif args[0] == "rr":
        help_message = \
"""
```
rr -- Returns a random Destiny raid

Params:
    * n (int) -- Number of raids to
      return. Default=1
    * list -- List the supported raids
```
"""
    else:
        help_message = \
"""
```
OOTL-Bot by TacticalFruit

Commands:
  help -- Shows this message.
  ping -- Pings the bot
  rr   -- Selects random Destiny raid(s)
  name -- Returns the name of the bot
```
"""

    await client.say(help_message)

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
        raids_copy = copy.deepcopy(raids)
        random.shuffle(raids_copy)

        await client.say("Random Raid(s): {}".format(raids_copy[0]))
    else:
        if args[0] == "list":
            # List out the supported raids
            await client.say("Supported Raids:\n{}".format("\n".join(raids)))
        else:
            number_raids = int(args[0])
            raids_copy = copy.deepcopy(raids)
            random.shuffle(raids_copy)

            await client.say("Random Raid(s): {}".format(", ".join(raids_copy[0:number_raids])))

# Run the bot with bot token
client.run('NDAzNTY0MzI0OTAxMjI0NDU4.DUJJug.VfYFg9rgSuaf5i9jdPrG0M41UYI')
