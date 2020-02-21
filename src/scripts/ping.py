from importlib import import_module

config = import_module('.config', package='src')
view = import_module('.view', package='src')

executable = True


async def main(m):
    args = m.content.lower().split(' ')
    command = args[0] = args[0][len(config.prefix):]

    # await m.channel.send('pong')

    # await view.send(view.apply_template(view.Lang.get('embed.testEmbed')))
    # or an easier syntax...

    await view.send(m.channel, view.Lang.get('embed.ping'))
