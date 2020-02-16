import importlib

config = importlib.import_module('config')

executable = True


async def main(m):
    args = m.content.lower().split(' ')
    command = args[0] = args[0][len(config.prefix):]

    await m.channel.send('pong')
