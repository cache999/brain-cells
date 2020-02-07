import discord
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

if BOT_TOKEN is None:
    raise LookupError('BOT_TOKEN is not defined!')


'''
    Code architecture for this project:
    Model Controller Script architecture (this is something I invented.)
    This is the 'bot' file. It is solely used to communicate with whatever API we are using, in this case, discord.
    The 'controller' file will call the 'bot' file to instantiate a bot. Having complete control over the bot's
    properties, it overwrites (monkey patches) the necessary methods on the bot. The only purpose of the controller
    is to relay information meaningfully to any one of the 'scripts'. In a nutshell, the controller is the input side
    of the frontend.
    e.g. A person types a command, say !help. The controller, having implemented a method to handle processing commands
    in general, would relegate individual processing to the 'help' script file.
    The 'view' file is the output side of the frontend. Having complete control over the bot, it parses information
    coming from the scripts into a meaningful way to interact with the (discord) API.
    The scripts are meant for individual handling of commands, for example !help or !bc. They have the ability to
    recieve the necessary information from the controller, and send information that will be sent to the user through
    the view. They do not, however have control over the bot itself. Scripts can also freely access the 'model' files.
    Thus, scripts are a bridge between the frontend and the backend.
    The model files are the backend. They would involve common functions for scripts such as incrementing a player's
    brain cells, or saving and loading data. They are only accessible via scripts.
'''


class Client(discord.Client):
    # create our own subclass of discord.Client so we hopefully don't break stuff via monkey patching.
    pass


def init_bot():
    client = Client()
    client.run(BOT_TOKEN)

if __name__ == "__main__":
    raise NameError('Run controller.py instead!')