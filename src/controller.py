import importlib
import discord
import json

with open('src/arch-config.json') as file:
    cfg = json.loads(file.read())
    file.close()
print("Architecture level config loaded from arch-config.json...")
bot = importlib.import_module(cfg['bot_filename'])
# bot prefix doesn't really belong here, but here it is before I create another config.
prefix = cfg['prefix']
info = importlib.import_module('Info')


# create functions to be patched
async def on_ready(self: bot.Client):
    print(f'{self.user} has connected to Discord.')


async def on_message(self: bot.Client, message: discord.message):
    if message.author == self.user:
        return

    if message.content.startswith(prefix):
        # gib an Info object to the appropriate script for further handling.
        i = info.Info(
            message=message,
            args=message.content.split(' ')
        )
        try:
            script = importlib.import_module('scripts.' + i.command)
            try:
                await script.main(i)
            except (NotImplementedError, AttributeError):
                await i.send(i.command + ' is not implemented. Try again at a later date!')
        except ModuleNotFoundError:
            await i.send(i.command + ' is not a valid command. Type ' + prefix + 'help for more info.')


# patch the functions into the bot
bot.Client.on_ready = on_ready
bot.Client.on_message = on_message
# start the bot
print('Starting the bot...')
bot.init_bot()
