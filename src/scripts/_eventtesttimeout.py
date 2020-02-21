from importlib import import_module

view = import_module('.view', package='src')
executable = False


async def main(execution_instructions, context_message):
    await view.send(context_message.channel, view.Lang.get('embed.eventTestTimeout'))
