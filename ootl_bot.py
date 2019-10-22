import os
import discord
from discord.ext.commands import Bot
from discord.ext import commands # imports a bunch of command things
import platform
import random
import copy

client = Bot(description="OOTL Bot by TacticalFruit", command_prefix="%", pm_help = False)

# Remove the normal help command. Our own will be added later
client.remove_command('help')

ootl_guild = None

tactical_fruit_id = 120317324141133829
tactical_fruit_user = None

ootl_guild_id = 327972891029143567
ootl_destiny_2_news_channel_id = 405790676416987136
ootl_destiny_2_channel_id = 328040568993349632

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
    global tactical_fruit_user
    global ootl_guild

    ootl_guild = client.get_guild(ootl_guild_id)

    if ootl_guild is None:
        print("couldn't grab guild")
    else:
        tactical_fruit_user = [mem for mem in ootl_guild.members if mem.id == tactical_fruit_id][0]

        print('Logged in as {} (ID: {}) | Connected to {} servers | Connected to {} users'.format(client.user.name, client.user.id, str(len(client.guilds)), str(len(set(client.get_all_members())))))
        print('--------')
        print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
        print('--------')
        print('Use this link to invite {}:'.format(client.user.name))
        print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))

@client.event
async def on_member_join(member):

    if tactical_fruit_user is not None:
        await tactical_fruit_user.send("New member joined! {}: {}".format(member.name, member.id))

@client.event
async def on_message(message):
    if not message.content.startswith('%'): return

    print("New Message:\n{}: {}".format(message.author.name, message.system_content))

    if message.channel.name == "destiny-2-news" and "maintenance" in message.content.lower():
        await tactical_fruit_user.send("New message from: {} saying \n\t".format(message.author, message.content))

    await client.process_commands(message)

##############################
###### Check Predicates ######
##############################

def is_tactical_fruit(ctx):
    return ctx.message.author.id == tactical_fruit_id

############################
###### Commands Block ######
############################

@client.command()
async def help(context):

    extra = context.message.content.split(context.prefix + str(context.command))
    """Replies with the help messages requested

    Parameters
    ----------
    args[0] : str, optional
        * 'ping' -- Replies with the help message for 'ping'
        * 'name' -- Replies with the help message for 'name'
        * 'underbelly' -- Replies with an image of the underbelly
        * 'memIds' -- Replies with the help message for 'memIds'
        * 'rr' -- Replies with the help message for 'rr'
    """

    if extra[1].strip() == "":
        help_message = \
"""
```
Commands:
  ping       -- Replies with the help message for 'ping'
  name       -- Replies with the help message for 'name'
  underbelly -- Replies with an image of the underbelly
  memIds     -- Replies with the help message for 'memIds'
  rr         -- Replies with the help message for 'rr'
  
Use '%help <command>' to find out more about
a specific command.

OOTL-Bot by TacticalFruit
```
"""
    elif extra[1].strip() == "ping":
        help_message = \
"""
```
ping -- Pings the bot

Params: None
Notes:
    * If the bot is up, it will reply with 'pong'
```
"""
    elif extra[1].strip() == "name":
        help_message = \
"""
```
name -- Returns the name of the bot

Params: None
```
"""
    elif extra[1].strip() == "memIds":
        help_message = \
"""
```
memIds -- Returns all server members' name & ID

Params: None
```
"""
    elif extra[1].strip() == "rr":
        help_message = \
"""
```
rr -- Returns a random Destiny raid

Params:
    * n (int) -- Number of raids to return. Default=1
    * list -- List the supported raids
```
"""
    else:
        help_message = "Command not supported"

    await context.send(help_message)

@client.command()
@commands.check(is_tactical_fruit)
async def get_channels(context):
    await context.send("```" + "\n".join(["{}: {}".format(channel.name, channel.id) for channel in context.guild.channels]) + "```")

@client.command()
@commands.check(is_tactical_fruit)
async def roles(context):
    await context.send("```" + "\n".join([role.name for role in context.guild.roles]) + "```")

@client.command()
@commands.check(is_tactical_fruit)
async def members(context):
    """Returns the members from the current server's names and IDs"""

    all_members = context.guild.members
    if len(context.args) > 0:
        filter_name = context.args[0]
        all_members = [mem for mem in all_members if filter_name.lower() in mem.name.lower()]

    longest_name_length = len(max([mem.name for mem in all_members], key=len))
    all_members_ids = ["{:{}} : {:10} : {}".format(mem.name, longest_name_length, mem.top_role.name, mem.id) for mem in all_members]
    all_members_string = "\n".join(all_members_ids)

    await context.send("```" + all_members_string + "```")

@client.command()
async def ping(context):
    """Pings the bot and replies with Pong"""

    await context.send("Pong!")

@client.command()
async def name(context):
    """Says back the bot's name"""

    await context.send("My name is {}!".format(context.user.name))

@client.command()
async def underbelly(context):
    """Replies with an image of the underbelly"""

    await context.send("Leviathen - underbelly", file="https://media.discordapp.net/attachments/403568301164462080/635681911808720917/image0.jpg")

@client.command()
async def rr(context):
    """Picks a random raid from the 'raids' list

    Parameters
    ----------
    args[0] : int, optional
        * '<number>' -- selects '<number>' of raids from supported list (Defaults to 1)
        * 'list' -- lists out the supported raids
    """

    if len(context.args) == 0:
        raids_copy = copy.deepcopy(raids)
        random.shuffle(raids_copy)

        await context.send("Random Raid(s): {}".format(raids_copy[0]))
    else:
        if context.args[0] == "list":
            # List out the supported raids
            await context.send("Supported Raids:\n{}".format("\n".join(raids)))
        else:
            number_raids = int(context.args[0])
            raids_copy = copy.deepcopy(raids)
            random.shuffle(raids_copy)

            await context.send("Random Raid(s): {}".format(", ".join(raids_copy[0:number_raids])))

# Run the bot with bot token
client.run(os.environ.get("DISCORD_BOT_TOKEN"))
