from discord import Embed
import json


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
    with open('src/arch-config.json') as f:
        ac = json.loads(f.read())
        f.close()
    with open('languages/' + ac['lang_file']) as f:
        langfile = json.loads(f.read())
        f.close()

    @staticmethod
    def get(name):
        return Lang.langfile[name]
