import importlib

config = importlib.import_module('config')
view = importlib.import_module('view')

executable = True


async def main(m):
    args = m.content.lower().split(' ')
    command = args[0] = args[0][len(config.prefix):]

    # await m.channel.send('pong')

    # await view.send(view.apply_template(view.Lang.get('embed.testEmbed')))
    # or an easier syntax...

    await view.send(m.channel, view.Lang.get('embed.ping'))
