import importlib

view = importlib.import_module('view')
executable = False


async def main(execution_instructions, context_message):
    await view.send(context_message.channel, view.Lang.get('embed.eventTestTimeout'))
