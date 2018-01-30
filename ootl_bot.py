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

tactical_fruit_id = "120317324141133829"
tactical_fruit_user = None

ootl_server_id = "327972891029143567"
ootl_destiny_2_news_channel_id = "405790676416987136"

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

# @client.event
# async def on_message(message):
#
#     print("New Message:\n{}: {}".format(message.author.name, message.system_content))

    # if message.channel.name == "destiny-2-news":
    #     await client.send_message(tactical_fruit_user, "New message from: {} saying \n\t".format(message.author, message.content))

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
Commands:
  ping   -- Pings the bot
  rr     -- Selects random Destiny raid(s)
  name   -- Returns the name of the bot
  
Use '%help <command>' to find out more about
a specific command.

OOTL-Bot by TacticalFruit
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
async def dump_messages(*args):

    all_messages = client.messages
    if len(all_messages) == 0:
        await client.say("No messages found")
        return
    all_messages = list(all_messages)[-10:]
    messages_dump = "\n".join(["{}: {} | {}/{} --- {}".format(msg.author.name, msg.channel.name, len(msg.attachments), len(msg.embeds), msg.system_content) for msg in all_messages])
    await client.say("```" + messages_dump + "```")

@client.command()
@commands.check(is_tactical_fruit)
async def roles(*args):

    roles = client.get_server(ootl_server_id).role_hierarchy
    await client.say("```" + "\n".join([role.name for role in roles]) + "```")

@client.command()
@commands.check(is_tactical_fruit)
async def members(*args):
    """Returns the members from the current server's names and IDs"""

    all_members = list(client.get_all_members())
    if len(args) > 0:
        filter_name = args[0]
        all_members = [mem for mem in all_members if filter_name.lower() in mem.name.lower()]

    longest_name_length = len(max([mem.name for mem in all_members], key=len))
    all_members_ids = ["{:{}} : {:10} : {}".format(mem.name, longest_name_length, mem.top_role.name, mem.id) for mem in all_members]
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
client.run(os.environ.get("DISCORD_BOT_TOKEN"))
