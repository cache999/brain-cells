from discord import Embed
import json
import importlib
config = importlib.import_module('config')


async def send_raw(info, message):
    await info.send(message)


def default_embed():
    """
    Generate a default embed for sending messages.
    :return: RichEmbed
    """
    embed = Embed(
        title='test embed title',
        color=0xff0000,
        description='test embed description',
    )
    embed.add_field(name='field name', value='field value')
    return embed


# wrapper for language
class Lang:

    with open('languages/' + config.lang_file) as f:
        lang_file = json.loads(f.read())
        f.close()

    @staticmethod
    def get(name):
        return Lang.lang_file[name]
