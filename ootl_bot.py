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

tactical_fruit_id = "120317324141133829"
tactical_fruit_user = None
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

    members = list(client.get_all_members())
    tactical_fruit_user = [mem for mem in members if mem.id == tactical_fruit_id][0]

    print('Logged in as {} (ID: {}) | Connected to {} servers | Connected to {} users'.format(client.user.name, client.user.id, str(len(client.servers)), str(len(set(client.get_all_members())))))
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))

@client.event
async def on_member_join(member):

    if tactical_fruit_user is not None:
        await client.send_message(tactical_fruit_user, "New member joined! {}: {}".format(member.name, member.id))

##############################
###### Check Predicates ######
##############################

def is_tactical_fruit(ctx):
    return ctx.message.author.id == tactical_fruit_id

############################
###### Commands Block ######
############################

@client.command()
async def help(*args):
    """Replies with the help messages requested

    Parameters
    ----------
    args[0] : str, optional
        * 'ping' -- Replies with the help message for 'ping'
        * 'name' -- Replies with the help message for 'name'
        * 'rr' -- Replies with the help message for 'rr'
        * 'memIds' -- Replies with the help message for 'memIds'
    """

    if len(args) == 0:
        help_message = \
"""
```
OOTL-Bot by TacticalFruit

Commands:
  ping   -- Pings the bot
  rr     -- Selects random Destiny raid(s)
  name   -- Returns the name of the bot
  
Use '%help <command>' to find out more about
a specific command.
```
"""
    elif args[0] == "ping":
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
    elif args[0] == "memIds":
        help_message = \
"""
```
memIds -- Returns all server members' name & ID

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
        help_message = "Command not supported"

    await client.say(help_message)

@client.command()
@commands.check(is_tactical_fruit)
async def memIds(*args):
    """Returns the members from the current server's names and IDs"""



    all_members = list(client.get_all_members())
    if len(args) > 0:
        filter_name = args[0]
        all_members = [mem for mem in all_members if filter_name.lower() in mem.name.lower()]

    longest_name_length = len(max([mem.name for mem in all_members], key=len))
    all_members_ids = ["{:{}} : {}".format(mem.name, longest_name_length, mem.id) for mem in all_members]
    all_members_string = "\n".join(all_members_ids)

    await client.say("```" + all_members_string + "```")

@client.command()
async def ping(*args):
    """Pings the bot and replies with Pong"""

    await client.say("Pong!")

@client.command()
async def name(*args):
    """Says back the bot's name"""

    await client.say("My name is {}!".format(client.user.name))

@client.command()
async def rr(*args):
    """Picks a random raid from the 'raids' list

    Parameters
    ----------
    args[0] : int, optional
        * '<number>' -- selects '<number>' of raids from supported list (Defaults to 1)
        * 'list' -- lists out the supported raids
    """

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
